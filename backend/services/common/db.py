"""SQLAlchemy engine/session — SQLite WAL (LOCAL profile) with Postgres upgrade path."""
from __future__ import annotations

from collections.abc import Iterator
from contextlib import contextmanager
from datetime import datetime

from sqlalchemy import DateTime, Float, Integer, String, Text, create_engine, event
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column, sessionmaker

from services.common.config import settings


class Base(DeclarativeBase):
    pass


def _make_engine():
    eng = create_engine(
        f"sqlite:///{settings.db_path}",
        connect_args={"check_same_thread": False, "timeout": 30},
        future=True,
    )

    @event.listens_for(eng, "connect")
    def _set_sqlite_pragma(dbapi_conn, _):
        cur = dbapi_conn.cursor()
        cur.execute("PRAGMA journal_mode=WAL")
        cur.execute("PRAGMA foreign_keys=ON")
        cur.execute("PRAGMA busy_timeout=30000")
        cur.close()

    return eng


engine = _make_engine()
SessionLocal = sessionmaker(bind=engine, autoflush=False, expire_on_commit=False, future=True)


def init_db() -> None:
    from services.common import tables  # noqa: F401

    Base.metadata.create_all(engine)


@contextmanager
def session_scope() -> Iterator[Session]:
    session = SessionLocal()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()


# --- shared column helpers -------------------------------------------------
def pk() -> Mapped[str]:
    return mapped_column(String(64), primary_key=True)


def ts(default: datetime | None = None) -> Mapped[datetime]:
    return mapped_column(DateTime(timezone=True), default=default or datetime.utcnow)


__all__ = [
    "Base",
    "SessionLocal",
    "engine",
    "init_db",
    "session_scope",
    "pk",
    "ts",
    "Mapped",
    "mapped_column",
    "String",
    "Integer",
    "Float",
    "Text",
    "DateTime",
]
