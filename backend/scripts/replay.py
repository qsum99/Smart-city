"""Replay events.jsonl into the bus (Time Machine v0) — idempotent by event_id."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from services.common.bus import replay_from_log

if __name__ == "__main__":
    n = replay_from_log()
    print(f"[replay] republished={n} (duplicates suppressed by idempotency)")
