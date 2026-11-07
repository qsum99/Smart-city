"""Test bootstrap: isolated temp data dir BEFORE any service import."""
from __future__ import annotations

import os
import sys
import tempfile
from pathlib import Path

BACKEND_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(BACKEND_ROOT))

_tmp = tempfile.mkdtemp(prefix="cityos_test_")
os.environ["CITYOS_DB_PATH"] = str(Path(_tmp) / "cityos.db")
os.environ["CITYOS_DATA_DIR"] = _tmp
os.environ["CITYOS_WINDOW_SECONDS"] = "1"
os.environ["CITYOS_POLL_INTERVAL_MS"] = "20"
os.environ["CITYOS_JWT_SECRET"] = "test-secret"

from services.common.auth import ensure_users  # noqa: E402
from services.common.db import init_db  # noqa: E402

init_db()
ensure_users()
