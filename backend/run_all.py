"""Spawn all CityOS services as local uvicorn processes (LOCAL profile — no Docker)."""
from __future__ import annotations

import signal
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent

SERVICES = [
    ("ingest", 8001),
    ("correlation", 8002),
    ("ticketing", 8003),
]


def main() -> None:
    # ensure DB + seeded users exist before children start
    subprocess.run([sys.executable, str(ROOT / "scripts" / "init_db.py")], check=True, cwd=ROOT)

    procs: list[subprocess.Popen] = []
    for name, port in SERVICES:
        proc = subprocess.Popen(
            [sys.executable, "-m", "uvicorn", f"services.{name}.app:app",
             "--host", "127.0.0.1", "--port", str(port)],
            cwd=ROOT,
        )
        procs.append(proc)
        print(f"[run_all] {name} -> http://127.0.0.1:{port} (docs at /docs)")

    def shutdown(*_):
        print("\n[run_all] stopping services...")
        for p in procs:
            p.terminate()
        for p in procs:
            p.wait(timeout=5)
        sys.exit(0)

    signal.signal(signal.SIGINT, shutdown)
    signal.signal(signal.SIGTERM, shutdown)

    while True:
        for name, proc in zip((s[0] for s in SERVICES), procs, strict=False):
            if proc.poll() is not None:
                print(f"[run_all] {name} exited with {proc.returncode} — shutting down")
                shutdown()
        time.sleep(1)


if __name__ == "__main__":
    main()
