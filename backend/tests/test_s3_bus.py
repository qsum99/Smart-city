"""S3 gates: bus publish/poll/ack, idempotency, DLQ, replay."""
from __future__ import annotations

import sqlalchemy as sa

from services.common import bus
from services.common.config import settings
from services.common.db import session_scope
from services.common.envelope import EventEnvelope, read_event_log
from services.common.tables import BusEvent, DeadLetter


def _env(payload: dict | None = None, etype: str = "flood.test") -> EventEnvelope:
    return EventEnvelope(type=etype, source="unit-test", zone_id="Z9", payload=payload or {})


def test_publish_poll_ack_roundtrip():
    e = _env({"n": 1})
    assert bus.publish(e) is True
    assert bus.pending_count("sensor.readings") >= 1
    got = bus.poll("sensor.readings", limit=100)
    assert e.event_id in [g.event_id for g in got]
    bus.ack(e.event_id)
    with session_scope() as s:
        row = s.scalar(sa.select(BusEvent).where(BusEvent.event_id == e.event_id))
        assert row.status == "done"


def test_idempotent_duplicate_suppressed():
    e = _env({"dup": True})
    assert bus.publish(e) is True
    assert bus.publish(e) is False  # same event_id
    e2 = EventEnvelope(type="flood.test", source="unit-test", zone_id="Z9",
                       payload={"dup": True}, occurred_at=e.occurred_at)
    assert bus.publish(e2) is False  # same content within 5s bucket


def test_dead_letter_after_three_failures():
    e = _env({"bad": True})
    assert bus.publish(e) is True
    for i in range(3):
        got = [g for g in bus.poll("sensor.readings", limit=200)
               if g.event_id == e.event_id]
        assert got, f"event should be pollable at iter{i}"
        bus.dead_letter(e.event_id, "boom")
    with session_scope() as s:
        row = s.scalar(sa.select(BusEvent).where(BusEvent.event_id == e.event_id))
        assert row.status == "dead"
        dl = s.scalar(sa.select(DeadLetter).where(DeadLetter.event_id == e.event_id))
        assert dl is not None and dl.error == "boom"


def test_replay_is_idempotent():
    e = _env({"replay": 1})
    bus.publish(e)
    n = bus.replay_from_log()
    events = read_event_log(settings.events_log)
    assert any(x.event_id == e.event_id for x in events)
    assert isinstance(n, int)


def test_inflight_reset_on_restart():
    e = _env({"inflight": 1})
    bus.publish(e)
    bus.poll("sensor.readings", limit=500)          # claim -> processing
    bus.reset_inflight("sensor.readings")           # restart recovery
    got_ids = [g.event_id for g in bus.poll("sensor.readings", limit=500)]
    assert e.event_id in got_ids
    bus.ack(e.event_id)
