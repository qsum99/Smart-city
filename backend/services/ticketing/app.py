"""Ticketing service — auto-route + status API (01 layer ⑦, BP0 walking skeleton)."""
from __future__ import annotations

import asyncio
import uuid
from datetime import UTC, datetime, timedelta

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy import select

from services.common import bus
from services.common.auth import TokenPayload, require_role
from services.common.auth_routes import router as auth_router
from services.common.config import settings
from services.common.db import session_scope
from services.common.envelope import EventEnvelope
from services.common.logging import get_logger, log_event
from services.common.tables import AuditLog, Ticket, TimelineEntry

log = get_logger("ticketing")

app = FastAPI(title="CityOS Ticketing", version="0.1.0")
app.include_router(auth_router)


# --- routing rules (BP0 hardcoded; BP2 moves to rules-engine) ---------------
ROUTING = [
    (("flood", "water", "pipe", "sewage"), "WATER", 2),
    (("pothole", "road", "streetlight"), "PWD", 3),
    (("traffic", "signal", "ambulance"), "TRAFFIC", 2),
    (("garbage", "waste", "bin"), "SOLID_WASTE", 3),
    (("hospital", "health"), "HEALTH", 2),
]
DEFAULT_DEPT = "OCC"
SLA_HOURS = {"WATER": 4, "PWD": 48, "TRAFFIC": 2, "SOLID_WASTE": 24, "HEALTH": 2, "OCC": 8}


def route_event_type(event_type: str) -> tuple[str, int]:
    for keywords, dept, priority in ROUTING:
        if any(k in event_type for k in keywords):
            return dept, priority
    return DEFAULT_DEPT, 3


def _new_ticket_id() -> str:
    return f"TCK-{datetime.now(UTC):%Y}-{uuid.uuid4().hex[:6].upper()}"


def _add_timeline(session, ticket_id: str, state: str, actor: str, note: str = "") -> None:
    session.add(TimelineEntry(ticket_id=ticket_id, state=state, actor=actor, note=note))


def _create_ticket(session, envelope: EventEnvelope, description: str,
                   severity: float | None, route_hint: str | None = None) -> Ticket:
    dept, priority = route_event_type(route_hint or envelope.type)
    ticket = Ticket(
        id=_new_ticket_id(),
        type=envelope.type,
        description=description,
        zone_id=envelope.zone_id,
        geo_lat=envelope.geo.lat if envelope.geo else None,
        geo_lon=envelope.geo.lon if envelope.geo else None,
        status="ASSIGNED",
        dept_id=dept,
        priority=priority if severity is None else max(1, priority - 1),
        severity=severity,
        sla_due_at=datetime.now(UTC).replace(tzinfo=None)
        + timedelta(hours=SLA_HOURS.get(dept, 8)),
        incident_id=envelope.payload.get("incident_id"),
        confidence=envelope.payload.get("confidence"),
        source_channel="auto",
    )
    _add_timeline(session, ticket.id, "RECEIVED", "system", "event ingested")
    _add_timeline(session, ticket.id, "ASSIGNED", "rules-engine", f"routed to {dept}")
    log_event(log, "ticket.created", ticket=ticket.id, dept=dept, type=envelope.type)
    return ticket


def _handle(envelope: EventEnvelope) -> None:
    with session_scope() as s:
        incident_id = envelope.payload.get("incident_id")
        if envelope.type == "incident.chain.updated" and incident_id:
            exists = s.scalar(select(Ticket).where(Ticket.incident_id == incident_id))
            if exists:
                return  # idempotent per incident
            chain = envelope.payload
            chain_types = " ".join(n.get("kind", "") for n in chain.get("nodes", []))
            ticket = _create_ticket(
                s, envelope,
                "Connected incident chain: "
                + " -> ".join(n["kind"] for n in chain.get("nodes", [])),
                chain.get("confidence"),
                route_hint=chain_types,
            )
        elif envelope.type.startswith("citizen."):
            ticket = _create_ticket(
                s, envelope, envelope.payload.get("description", ""), None,
                route_hint=f"{envelope.type} {envelope.payload.get('description', '')}",
            )
            ticket.source_channel = envelope.payload.get("channel", "api")
            ticket.anonymous = bool(envelope.payload.get("anonymous"))
        else:
            ticket = _create_ticket(s, envelope, envelope.payload.get("summary", ""), None)
        s.add(ticket)
        ticket_id = ticket.id
    # mock citizen notification (BP3 -> real channels)
    log_event(log, "notification.sent", ticket=ticket_id, channel="inapp",
              text="your report was routed - track status")


async def _loop() -> None:
    log_event(log, "ticketing.loop_started")
    while True:
        envelopes = bus.poll("citizen.reports", limit=25) + bus.poll("incident.commands", limit=25)
        for env in envelopes:
            try:
                _handle(env)
                bus.ack(env.event_id)
            except Exception as exc:
                bus.dead_letter(env.event_id, str(exc))
                log_event(log, "ticketing.handler_error", event_id=env.event_id, error=str(exc))
        await asyncio.sleep(settings.poll_interval_ms / 1000)


@app.on_event("startup")
async def startup() -> None:
    asyncio.create_task(_loop())


# --- API -------------------------------------------------------------------
@app.get("/healthz")
def healthz() -> dict:
    return {"service": "ticketing", "status": "ok"}


def _ticket_dict(t: Ticket) -> dict:
    return {
        "ticket_id": t.id,
        "type": t.type,
        "status": t.status,
        "dept": t.dept_id,
        "priority": t.priority,
        "severity": t.severity,
        "zone_id": t.zone_id,
        "incident_id": t.incident_id,
        "sla_due_at": t.sla_due_at.isoformat() if t.sla_due_at else None,
        "description": t.description,
    }


@app.get("/api/v1/tickets")
def list_tickets(status: str | None = None, dept: str | None = None, limit: int = 50,
                 _user: TokenPayload = Depends(require_role("operator"))) -> dict:
    with session_scope() as s:
        stmt = select(Ticket).order_by(Ticket.created_at.desc()).limit(limit)
        if status:
            stmt = stmt.where(Ticket.status == status)
        if dept:
            stmt = stmt.where(Ticket.dept_id == dept)
        return {"items": [_ticket_dict(t) for t in s.execute(stmt).scalars().all()]}


@app.get("/api/v1/tickets/{ticket_id}")
def get_ticket(ticket_id: str,
               _user: TokenPayload = Depends(require_role("operator"))) -> dict:
    with session_scope() as s:
        t = s.get(Ticket, ticket_id)
        if t is None:
            raise HTTPException(404, detail="ticket not found")
        entries = s.execute(
            select(TimelineEntry).where(TimelineEntry.ticket_id == ticket_id)
            .order_by(TimelineEntry.at)
        ).scalars().all()
        data = _ticket_dict(t)
        data["timeline"] = [
            {"at": e.at.isoformat(), "state": e.state, "actor": e.actor, "note": e.note}
            for e in entries
        ]
        return data


@app.post("/api/v1/tickets/{ticket_id}/approve")
def approve_ticket(ticket_id: str,
                   user: TokenPayload = Depends(require_role("approver"))) -> dict:
    """Human approval on the recommended action (walks RECEIVED→ASSIGNED→IN_PROGRESS)."""
    with session_scope() as s:
        t = s.get(Ticket, ticket_id)
        if t is None:
            raise HTTPException(404, detail="ticket not found")
        if t.status in ("IN_PROGRESS", "RESOLVED", "CLOSED"):
            raise HTTPException(409, detail=f"already {t.status}")
        t.status = "IN_PROGRESS"
        _add_timeline(s, ticket_id, "IN_PROGRESS", user.sub, "recommendation approved")
        prev = s.execute(select(AuditLog).order_by(AuditLog.id.desc()).limit(1)).scalar()
        s.add(AuditLog(
            actor=user.sub, role=user.role, action="approve",
            entity=f"ticket:{ticket_id}",
            after_hash="IN_PROGRESS",
            prev_hash=str(prev.id) if prev else None,
        ))
    log_event(log, "ticket.approved", ticket=ticket_id, by=user.sub)
    return {"ticket_id": ticket_id, "status": "IN_PROGRESS", "approved_by": user.sub}
