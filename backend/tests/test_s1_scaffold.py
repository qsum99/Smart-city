"""S1 gates: services scaffolded, health endpoints, auth token endpoint."""
from __future__ import annotations

import pytest
from fastapi.testclient import TestClient

from services.correlation.app import app as corr_app
from services.ingest.app import app as ingest_app
from services.ticketing.app import app as ticket_app


@pytest.mark.parametrize(
    ("app", "name"),
    [(ingest_app, "ingest"), (corr_app, "correlation"), (ticket_app, "ticketing")],
)
def test_healthz(app, name):
    with TestClient(app) as c:
        r = c.get("/healthz")
        assert r.status_code == 200
        expected = {"service": name, "status": "ok"}
        if name == "correlation":
            expected["zones_buffered"] = 0
        assert r.json() == expected


def test_token_endpoint_issues_jwt():
    with TestClient(ticket_app) as c:
        r = c.post("/auth/token", data={"username": "approver", "password": "approver123"})
        assert r.status_code == 200
        assert r.json()["token_type"] == "bearer"
        assert r.json()["role"] == "approver"


def test_bad_password_rejected():
    with TestClient(ticket_app) as c:
        r = c.post("/auth/token", data={"username": "approver", "password": "wrong"})
        assert r.status_code == 401
