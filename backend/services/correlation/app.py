"""Correlation service — sliding zone windows → incident chain (01 layer ⑤, BP0 stub).

BP0: co-occurrence chain (≥2 related events in a zone within the window).
BP1 upgrades this to graph traversal + causal templates (10 §1) — same interface.
"""
from __future__ import annotations

import asyncio
import json
from datetime import UTC, datetime, timedelta

from fastapi import FastAPI

from services.common import bus
from services.common.auth_routes import router as auth_router
from services.common.config import settings
from services.common.envelope import EventEnvelope
from services.common.logging import get_logger, log_event

log = get_logger("correlation")

app = FastAPI(title="CityOS Correlation", version="0.1.0")
app.include_router(auth_router)

# zone_id → buffered events
_buffers: dict[str, list[EventEnvelope]] = {}
_chains: list[dict] = []


@app.get("/healthz")
def healthz() -> dict:
    return {"service": "correlation", "status": "ok", "zones_buffered": len(_buffers)}


@app.get("/api/v1/chains")
def list_chains(limit: int = 20) -> dict:
    return {"items": _chains[-limit:]}


def _build_chain(zone_id: str, events: list[EventEnvelope]) -> dict:
    events = sorted(events, key=lambda e: e.occurred_at)
    primary = events[0]
    nodes = [
        {"ref": e.event_id, "kind": e.type, "at": e.occurred_at.isoformat()}
        for e in events
    ]
    # BP0 stub: confidence grows with corroborating events (BP1: per-link product — 10 §1)
    confidence = min(0.5 + 0.15 * (len(nodes) - 1), 0.95)
    chain = {
        "chain_id": f"chn_{primary.event_id[-8:]}",
        "incident_id": f"inc_{primary.event_id[-8:]}",
        "zone_id": zone_id,
        "label": "correlation",  # becomes causal-grade only via 10 §1 gates (BP1)
        "nodes": nodes,
        "confidence": round(confidence, 2),
        "primary_type": primary.type,
        "built_at": datetime.now(UTC).isoformat(),
    }
    return chain


def _flush_expired(now: datetime) -> list[dict]:
    window = timedelta(seconds=settings.window_seconds)
    built: list[dict] = []
    for zone_id, events in list(_buffers.items()):
        oldest = min(e.occurred_at for e in events)
        if now - oldest >= window:
            if len(events) >= 2:
                chain = _build_chain(zone_id, events)
                built.append(chain)
                _chains.append(chain)
                with open(settings.chains_log, "a", encoding="utf-8") as f:
                    f.write(json.dumps(chain) + "\n")
                env = EventEnvelope(
                    type="incident.chain.updated",
                    source="correlation-svc",
                    zone_id=zone_id,
                    geo=events[0].geo,
                    payload=chain,
                )
                bus.publish(env)
                log_event(log, "chain.built", chain_id=chain["chain_id"], nodes=len(chain["nodes"]))
            else:
                log_event(log, "window.single_event_dropped", zone_id=zone_id)
            del _buffers[zone_id]
    return built


def _process(envelopes: list[EventEnvelope]) -> None:
    for env in envelopes:
        try:
            _buffers.setdefault(env.zone_id, []).append(env)
            bus.ack(env.event_id)
        except Exception as exc:
            bus.dead_letter(env.event_id, str(exc))
    _flush_expired(datetime.now(UTC))


async def _loop() -> None:
    log_event(log, "correlation.loop_started", window=settings.window_seconds)
    while True:
        try:
            envelopes = bus.poll("sensor.readings", limit=50) + bus.poll("dept.alerts", limit=50)
            if envelopes:
                _process(envelopes)
            elif _buffers:
                _flush_expired(datetime.now(UTC))  # windows expire even with no new events
        except Exception as exc:
            log_event(log, "correlation.loop_error", error=str(exc))
        await asyncio.sleep(settings.poll_interval_ms / 1000)


@app.on_event("startup")
async def startup() -> None:
    asyncio.create_task(_loop())
