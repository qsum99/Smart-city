"""Initialize DB tables + seed demo users (idempotent)."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from services.common.auth import ensure_users
from services.common.config import settings
from services.common.db import init_db

if __name__ == "__main__":
    settings.ensure_dirs()
    init_db()
    ensure_users()
    print(f"[init_db] ready -> {settings.db_path}")
