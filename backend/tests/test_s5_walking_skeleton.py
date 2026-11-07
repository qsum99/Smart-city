"""S5 gate: BP0 walking skeleton end-to-end — event → chain → ticket → approve → timeline."""
from __future__ import annotations

import time

from fastapi.testclient import TestClient

from services.common import bus
from services.common.envelope import EventEnvelope
from services.correlation.app import app as corr_app
from services.ticketing.app import app as ticket_app


def _wait(client: TestClient, url: str, check, timeout: float = 8.0,
          headers: dict | None = None):
    deadline = time.time() + timeout
    while time.time() < deadline:
        data = client.get(url, headers=headers or {}).json()
        if "items" not in data:
            time.sleep(0.1)
            continue
        items = check(data)
        if items:
            return items
        time.sleep(0.1)
    raise AssertionError(f"condition not met for {url} within {timeout}s")


def test_walking_skeleton():
    with TestClient(corr_app) as corr, TestClient(ticket_app) as tix:
        # operator token
        r = tix.post("/auth/token", data={"username": "approver", "password": "approver123"})
        headers = {"Authorization": f"Bearer {r.json()['access_token']}"}

        # two related events in the same zone (window = 1s in tests)
        e1 = EventEnvelope(type="flood.threshold_exceeded", source="G17", zone_id="Z3",
                           geo={"lat": 12.97, "lon": 77.59},
                           payload={"gauge_id": "G17", "level_m": 4.8})
        e2 = EventEnvelope(type="road.closure", source="ops", zone_id="Z3",
                           geo={"lat": 12.975, "lon": 77.595},
                           payload={"road_id": "R7"})
        assert bus.publish(e1)
        assert bus.publish(e2)
        assert bus.publish(e1) is False  # idempotent re-post

        # chain built after window expires (filter to this test's zone)
        def chain_check(data):
            return [c for c in data["items"]
                    if c["zone_id"] == "Z3" and len(c["nodes"]) >= 2]

        chains = _wait(corr, "/api/v1/chains", chain_check)
        chain = chains[-1]
        assert chain["label"] == "correlation"
        assert {n["kind"] for n in chain["nodes"]} == {"flood.threshold_exceeded", "road.closure"}
        assert 0.5 <= chain["confidence"] <= 0.95

        # ticket auto-created + routed (flood → WATER)
        def ticket_check(data):
            return [i for i in data["items"] if i["incident_id"] == chain["incident_id"]]

        tickets = _wait(tix, "/api/v1/tickets", ticket_check, headers=headers)
        t = tickets[0]
        assert t["dept"] == "WATER"
        assert t["status"] == "ASSIGNED"
        assert t["incident_id"] == chain["incident_id"]
        assert t["severity"] == chain["confidence"]

        # human approval (approver role)
        r = tix.post(f"/api/v1/tickets/{t['ticket_id']}/approve", headers=headers)
        assert r.status_code == 200
        assert r.json()["status"] == "IN_PROGRESS"

        # second approve → conflict
        r2 = tix.post(f"/api/v1/tickets/{t['ticket_id']}/approve", headers=headers)
        assert r2.status_code == 409

        # citizen-visible timeline: received → assigned → approved + notification logged
        detail = tix.get(f"/api/v1/tickets/{t['ticket_id']}", headers=headers).json()
        states = [x["state"] for x in detail["timeline"]]
        assert states == ["RECEIVED", "ASSIGNED", "IN_PROGRESS"]


def test_citizen_report_routing():
    with TestClient(ticket_app) as tix:
        r = tix.post("/auth/token", data={"username": "operator", "password": "operator123"})
        headers = {"Authorization": f"Bearer {r.json()['access_token']}"}

        env = EventEnvelope(type="citizen.report.received", source="app", zone_id="Z1",
                            payload={"description": "deep pothole near bus stop",
                                     "channel": "mobile"})
        bus.publish(env)

        def check(data):
            return [i for i in data["items"] if i["type"] == "citizen.report.received"]

        items = _wait(tix, "/api/v1/tickets", check, headers=headers)
        assert items[0]["dept"] == "PWD"
