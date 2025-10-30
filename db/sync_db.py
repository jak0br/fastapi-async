from sqlmodel import SQLModel
from sqlalchemy.orm import sessionmaker
from db.config import settings
from sqlalchemy import create_engine as create_sync_engine
from sqlalchemy.orm import Session as SyncSession
from contextlib import contextmanager
from typing import Generator
from sqlmodel import create_engine

SYNC_DATABASE_URL = (
    f"postgresql://{settings.DB_USER}:{settings.DB_PASSWORD}"
    f"@{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}"
)

sync_engine = create_sync_engine(
    SYNC_DATABASE_URL,
    echo=False,
    pool_size=settings.POOL_SIZE,
    max_overflow=settings.MAX_OVERFLOW,
    pool_pre_ping=True,
    pool_recycle=1800,
)

# Regular (blocking) Session factory
SyncSessionLocal = sessionmaker(
    bind=sync_engine,
    class_=SyncSession,
    expire_on_commit=False,
    autoflush=False,
)

def init_db_sync() -> None:
    """Create database tables synchronously using the blocking engine.

    Useful for quick local tests or profiling runs where you don't want the
    async startup path.
    """
    SQLModel.metadata.create_all(bind=sync_engine)

@contextmanager
def get_sync_session() -> Generator[SyncSession, None, None]:
    """Context manager that yields a regular (blocking) Session.

    Usage:
        with get_sync_session() as session:
            ...
    """
    session = SyncSessionLocal()
    try:
        yield session
    finally:
        session.close()


def init_db_sync() -> None:
    """Create database tables synchronously using the blocking engine.

    Useful for quick local tests or profiling runs where you don't want the
    async startup path.
    """
    SQLModel.metadata.create_all(bind=sync_engine)


def get_sync_db() -> Generator[SyncSession, None, None]:
    """FastAPI dependency wrapper for the blocking session.

    Usage in an endpoint:
        def endpoint(session: SyncSession = Depends(get_sync_db)):
            ...
    """
    with get_sync_session() as session:
        yield session


DATABASE_URL = "postgresql://user:password@localhost:5432/appdb"
engine = create_engine(DATABASE_URL, echo=True)

