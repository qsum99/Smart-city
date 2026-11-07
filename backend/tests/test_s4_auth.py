"""S4 gates: role enforcement (09 §1 role matrix)."""
from __future__ import annotations

from fastapi.testclient import TestClient

from services.ticketing.app import app as ticket_app


def _token(c: TestClient, username: str, password: str) -> str | None:
    r = c.post("/auth/token", data={"username": username, "password": password})
    return r.json().get("access_token") if r.status_code == 200 else None


def test_requires_token():
    with TestClient(ticket_app) as c:
        assert c.get("/api/v1/tickets").status_code == 401


def test_operator_can_list():
    with TestClient(ticket_app) as c:
        tok = _token(c, "operator", "operator123")
        assert tok
        h = {"Authorization": f"Bearer {tok}"}
        assert c.get("/api/v1/tickets", headers=h).status_code == 200


def test_operator_role_gate_is_403_on_approve():
    with TestClient(ticket_app) as c:
        tok = _token(c, "operator", "operator123")
        h = {"Authorization": f"Bearer {tok}"}
        r = c.post("/api/v1/tickets/NOPE/approve", headers=h)
        assert r.status_code == 403  # role checked before resource lookup


def test_cannot_login_with_bad_password():
    with TestClient(ticket_app) as c:
        assert _token(c, "approver", "nope") is None
