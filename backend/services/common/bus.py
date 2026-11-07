"""In-proc/local event bus backed by SQLite (topics + envelope from 02 §2).

- publish: insert bus_events row (+ append events.jsonl replay log)
- poll: claim pending events for a topic (per-consumer, idempotent by event_id)
- ack/fail: mark done or dead-letter (10 §5)
Same interface can be re-implemented over Kafka later (12 §0 swappability).
"""
from __future__ import annotations

import hashlib
import json

from sqlalchemy import select

from services.common.config import settings
from services.common.db import session_scope
from services.common.envelope import EventEnvelope, append_event_log, read_event_log
from services.common.logging import get_logger
from services.common.tables import BusEvent, DeadLetter

log = get_logger("bus")


def idem_key_for(envelope: EventEnvelope) -> str:
    """source + content-hash + 5s time bucket (10 §5 duplicate rule)."""
    bucket = int(envelope.occurred_at.timestamp()) // 5
    payload = json.dumps(envelope.payload, sort_keys=True)
    content = f"{envelope.source}|{envelope.type}|{payload}|{bucket}"
    return hashlib.sha256(content.encode()).hexdigest()


def publish(envelope: EventEnvelope) -> bool:
    """Returns True if newly stored, False if duplicate (idempotent)."""
    settings.ensure_dirs()
    key = idem_key_for(envelope)
    with session_scope() as s:
        dup = s.scalar(
            select(BusEvent).where(
                (BusEvent.event_id == envelope.event_id) | (BusEvent.idem_key == key)
            )
        )
        if dup:
            log.info("bus.duplicate_suppressed", extra={"event_id": envelope.event_id})
            return False
        s.add(
            BusEvent(
                event_id=envelope.event_id,
                topic=envelope.topic,
                type=envelope.type,
                zone_id=envelope.zone_id,
                payload=envelope.model_dump(mode="json"),
                occurred_at=envelope.occurred_at.replace(tzinfo=None),
                status="pending",
                idem_key=key,
            )
        )
    append_event_log(settings.events_log, envelope)
    log.info("bus.published", extra={"topic": envelope.topic, "type": envelope.type})
    return True


def poll(topic: str, limit: int = 20) -> list[EventEnvelope]:
    """Claim pending events for a topic (mark processing→returned as envelopes)."""
    with session_scope() as s:
        rows = (
            s.execute(
                select(BusEvent)
                .where(BusEvent.topic == topic, BusEvent.status == "pending")
                .order_by(BusEvent.id)
                .limit(limit)
            )
            .scalars()
            .all()
        )
        envelopes = []
        for row in rows:
            row.status = "processing"
            row.attempts += 1
            envelopes.append(EventEnvelope.model_validate(row.payload))
        return envelopes


def _by_event_id(session, event_id: str) -> BusEvent | None:
    return session.scalar(select(BusEvent).where(BusEvent.event_id == event_id))


def ack(event_id: str) -> None:
    with session_scope() as s:
        row = _by_event_id(s, event_id)
        if row:
            row.status = "done"


def dead_letter(event_id: str, error: str) -> None:
    with session_scope() as s:
        row = _by_event_id(s, event_id)
        if row is None:
            return
        if row.attempts >= 3:
            row.status = "dead"
            s.add(
                DeadLetter(
                    event_id=row.event_id, topic=row.topic, payload=row.payload, error=error
                )
            )
            log.error("bus.dead_lettered", extra={"event_id": event_id, "error": error})
        else:
            row.status = "pending"  # retry


def reset_inflight(topic: str) -> int:
    """On consumer startup, requeue events stuck in 'processing' (LOCAL profile)."""
    with session_scope() as s:
        stmt = (
            select(BusEvent)
            .where(BusEvent.topic == topic, BusEvent.status == "processing")
        )
        rows = s.execute(stmt).scalars().all()
        for row in rows:
            row.status = "pending"
        if rows:
            log.info("bus.inflight_requeued", extra={"topic": topic, "count": len(rows)})
        return len(rows)


def pending_count(topic: str | None = None) -> int:
    with session_scope() as s:
        stmt = select(BusEvent).where(BusEvent.status == "pending")
        if topic:
            stmt = stmt.where(BusEvent.topic == topic)
        return len(s.execute(stmt).scalars().all())


def replay_from_log() -> int:
    """Re-publish everything from events.jsonl (Time Machine source); idempotent."""
    count = 0
    for env in read_event_log(settings.events_log):
        if publish(env):
            count += 1
    log.info("bus.replay_done", extra={"republished": count})
    return count
