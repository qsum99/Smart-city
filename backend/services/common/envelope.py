"""Event envelope (doc 02 §2) — Pydantic model + JSONL append (replay source)."""
from __future__ import annotations

import json
import uuid
from datetime import UTC, datetime
from enum import IntEnum
from typing import Any

from pydantic import BaseModel, Field, field_validator

TOPICS = ("sensor.readings", "citizen.reports", "dept.alerts", "incident.commands")

TOPIC_BY_PREFIX = {
    "sensor.": "sensor.readings",
    "vision.": "sensor.readings",
    "citizen.": "citizen.reports",
    "dept.": "dept.alerts",
    "incident.": "incident.commands",
    "flood.": "sensor.readings",
    "road.": "dept.alerts",
    "traffic.": "sensor.readings",
    "ambulance.": "sensor.readings",
    "hospital.": "dept.alerts",
}


class PIILevel(IntEnum):
    NONE = 0
    PSEUDONYMOUS = 1
    RAW = 2


def new_event_id() -> str:
    return f"evt_{uuid.uuid4().hex}"


def new_trace_id() -> str:
    return f"trc_{uuid.uuid4().hex[:16]}"


class Geo(BaseModel):
    lat: float = Field(ge=-90, le=90)
    lon: float = Field(ge=-180, le=180)


class EventEnvelope(BaseModel):
    event_id: str = Field(default_factory=new_event_id)
    type: str
    source: str
    occurred_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    zone_id: str
    geo: Geo | None = None
    payload: dict[str, Any] = Field(default_factory=dict)
    pii_level: PIILevel = PIILevel.NONE
    trace_id: str = Field(default_factory=new_trace_id)

    @field_validator("type")
    @classmethod
    def type_must_have_dot(cls, v: str) -> str:
        if "." not in v:
            raise ValueError("event type must be namespaced, e.g. 'flood.threshold_exceeded'")
        return v

    @property
    def topic(self) -> str:
        for prefix, topic in TOPIC_BY_PREFIX.items():
            if self.type.startswith(prefix):
                return topic
        return "sensor.readings"


def append_event_log(path, envelope: EventEnvelope) -> None:
    """Append-only JSONL — Time Machine replay source (works both profiles)."""
    with open(path, "a", encoding="utf-8") as f:
        f.write(envelope.model_dump_json() + "\n")


def read_event_log(path) -> list[EventEnvelope]:
    events: list[EventEnvelope] = []
    if not path.exists():
        return events
    with open(path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                events.append(EventEnvelope.model_validate(json.loads(line)))
    return events
