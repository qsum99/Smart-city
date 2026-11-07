"""S2 gates: envelope validation + JSONL replay log round-trip."""
from __future__ import annotations

from pathlib import Path

import pytest
from pydantic import ValidationError

from services.common.envelope import EventEnvelope, append_event_log, read_event_log


def test_envelope_defaults_and_topic_mapping():
    e = EventEnvelope(type="flood.threshold_exceeded", source="g1", zone_id="Z3")
    assert e.topic == "sensor.readings"
    assert e.event_id.startswith("evt_")
    assert e.trace_id.startswith("trc_")

    e2 = EventEnvelope(type="citizen.report.received", source="app", zone_id="Z1")
    assert e2.topic == "citizen.reports"

    e3 = EventEnvelope(type="dept.road_closure", source="ops", zone_id="Z1")
    assert e3.topic == "dept.alerts"


def test_envelope_rejects_unnamespaced_type():
    with pytest.raises(ValidationError):
        EventEnvelope(type="flood", source="g1", zone_id="Z3")


def test_geo_bounds():
    with pytest.raises(ValidationError):
        EventEnvelope(type="flood.x", source="g", zone_id="Z", geo={"lat": 91, "lon": 0})


def test_jsonl_roundtrip(tmp_path: Path):
    path = tmp_path / "events.jsonl"
    e1 = EventEnvelope(type="flood.a", source="g", zone_id="Z3", payload={"level_m": 4.8})
    e2 = EventEnvelope(type="road.closure", source="ops", zone_id="Z3")
    append_event_log(path, e1)
    append_event_log(path, e2)
    back = read_event_log(path)
    assert [e.event_id for e in back] == [e1.event_id, e2.event_id]
    assert back[0].payload["level_m"] == 4.8
