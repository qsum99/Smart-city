"""BP0 walking-skeleton demo: two flood-zone events -> chain -> ticket -> approve -> citizen view.

Run:  python run_all.py          (in one terminal)
      python scripts/demo.py     (in another)
"""
from __future__ import annotations

import sys
import time
from pathlib import Path

import httpx

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

INGEST = "http://127.0.0.1:8001"
CORR = "http://127.0.0.1:8002"
TICKET = "http://127.0.0.1:8003"

WINDOW = 6  # matches CITYOS_WINDOW_SECONDS used by run_all demo default


def get_token(client: httpx.Client) -> str:
    r = client.post(f"{TICKET}/auth/token",
                    data={"username": "approver", "password": "approver123"})
    r.raise_for_status()
    return r.json()["access_token"]


def main() -> None:
    with httpx.Client(timeout=10) as client:
        # wait for services
        for base in (INGEST, CORR, TICKET):
            for _ in range(40):
                try:
                    if client.get(f"{base}/healthz").status_code == 200:
                        break
                except httpx.TransportError:
                    time.sleep(0.25)
            else:
                sys.exit(f"service not reachable: {base}")

        token = get_token(client)
        headers = {"Authorization": f"Bearer {token}"}
        op_headers = {"Authorization": f"Bearer {token}"}

        print("1) posting flood zone events ...")
        events = [
            {"type": "flood.threshold_exceeded", "source": "gauge-G17", "zone_id": "Z3",
             "geo": {"lat": 12.97, "lon": 77.59},
             "payload": {"gauge_id": "G17", "level_m": 4.8, "threshold_m": 4.5}},
            {"type": "road.closure", "source": "ops-R7", "zone_id": "Z3",
             "geo": {"lat": 12.975, "lon": 77.595},
             "payload": {"road_id": "R7", "reason": "waterlogging"}},
        ]
        for e in events:
            r = client.post(f"{INGEST}/api/v1/events", json=e, headers=op_headers)
            r.raise_for_status()
            print(f"   accepted={r.json()['accepted']} duplicate={r.json()['duplicate']}")

        # duplicate test
        r = client.post(f"{INGEST}/api/v1/events", json=events[0], headers=op_headers)
        print(f"   replay same event -> duplicate={r.json()['duplicate']} (idempotency OK)")

        print(f"2) waiting {WINDOW}s for correlation window ...")
        time.sleep(WINDOW + 1)

        chains = client.get(f"{CORR}/api/v1/chains").json()["items"]
        assert chains, "no chain built!"
        chain = chains[-1]
        print(f"   chain {chain['chain_id']} label={chain['label']} "
              f"nodes={len(chain['nodes'])} confidence={chain['confidence']}")
        for n in chain["nodes"]:
            print(f"     - {n['kind']}")

        print("3) looking for auto-created ticket ...")
        ticket_id = None
        for _ in range(20):
            items = client.get(f"{TICKET}/api/v1/tickets", headers=op_headers).json()["items"]
            if items:
                ticket_id = items[0]["ticket_id"]
                print(f"   {ticket_id} dept={items[0]['dept']} status={items[0]['status']} "
                      f"severity={items[0]['severity']}")
                break
            time.sleep(0.5)
        assert ticket_id, "no ticket created!"

        print("4) approver approves the recommended action ...")
        r = client.post(f"{TICKET}/api/v1/tickets/{ticket_id}/approve", headers=headers)
        r.raise_for_status()
        print(f"   -> {r.json()}")

        detail = client.get(f"{TICKET}/api/v1/tickets/{ticket_id}", headers=op_headers).json()
        print("5) ticket timeline (citizen-visible status):")
        for t in detail["timeline"]:
            print(f"     {t['at']}  {t['state']:<14} {t['actor']}  {t['note']}")

        print("\nBP0 DEMO OK   event -> chain -> routed ticket -> approval -> timeline")
        print("audit + events.jsonl + chains.jsonl written under ./data/")


if __name__ == "__main__":
    main()
