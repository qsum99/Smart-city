"""CityOS common configuration — LOCAL profile (no Docker)."""
from __future__ import annotations

from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

BACKEND_ROOT = Path(__file__).resolve().parents[2]


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="CITYOS_", env_file=".env", extra="ignore")

    env: str = "local"
    data_dir: Path = BACKEND_ROOT / "data"
    db_path: Path = BACKEND_ROOT / "data" / "cityos.db"
    logs_dir: Path = BACKEND_ROOT / "logs"

    # bus
    poll_interval_ms: int = 50
    window_seconds: int = 300  # correlation window (tests use small values)

    # ports (run_all.py)
    ingest_port: int = 8001
    correlation_port: int = 8002
    ticketing_port: int = 8003

    # auth (LOCAL: dev secret; PILOT: Vault/Keycloak — 12 §0)
    jwt_secret: str = "dev-secret-change-me"
    jwt_alg: str = "HS256"
    jwt_ttl_seconds: int = 3600

    @property
    def events_log(self) -> Path:
        return self.data_dir / "events.jsonl"

    @property
    def chains_log(self) -> Path:
        return self.data_dir / "chains.jsonl"

    def ensure_dirs(self) -> None:
        for p in (self.data_dir, self.logs_dir, self.data_dir / "media", self.data_dir / "xai"):
            p.mkdir(parents=True, exist_ok=True)


settings = Settings()
settings.ensure_dirs()
