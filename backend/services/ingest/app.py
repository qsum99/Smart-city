"""Ingest service — validates events and publishes to the bus (01 layer ①)."""
from __future__ import annotations

from fastapi import Depends, FastAPI, HTTPException

from services.common.auth import require_role
from services.common.bus import publish
from services.common.envelope import EventEnvelope
from services.common.logging import get_logger

log = get_logger("ingest")

app = FastAPI(title="CityOS Ingest", version="0.1.0")


@app.get("/healthz")
def healthz() -> dict:
    return {"service": "ingest", "status": "ok"}


@app.post("/api/v1/events", status_code=202)
def ingest_event(envelope: EventEnvelope, _user=Depends(require_role("operator"))) -> dict:
    try:
        created = publish(envelope)
    except Exception as exc:  # validation or store failure → client error
        raise HTTPException(422, detail=str(exc)) from exc
    return {
        "event_id": envelope.event_id,
        "topic": envelope.topic,
        "accepted": created,
        "duplicate": not created,
    }
