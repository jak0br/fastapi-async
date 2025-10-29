from collections.abc import AsyncGenerator
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import SQLModel
from app.db.config import settings
from sqlalchemy import create_engine as create_sync_engine
from sqlalchemy.orm import Session as SyncSession
from contextlib import contextmanager
from typing import Generator
from sqlmodel import create_engine

DATABASE_URL = (
    f"postgresql+asyncpg://{settings.DB_USER}:{settings.DB_PASSWORD}"
    f"@{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}"
)

# Single process-wide async engine with a pooled connection backend
engine = create_async_engine(
    DATABASE_URL,
    echo=False,                    # set True for SQL logs
    pool_size=settings.POOL_SIZE,  # base pool
    max_overflow=settings.MAX_OVERFLOW,  # burst capacity
    pool_pre_ping=True,            # validate connections
    pool_recycle=1800,             # recycle every 30 min
)

# Async session factory bound to the pooled engine
AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False,
)  # type: ignore[call-arg]

# Dependency: yields a session; FastAPI handles enter/exit and returns
# the underlying DB connection to the pool after the request
async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        yield session

# Optional: create tables at startup (use Alembic in real prod)
async def init_db() -> None:
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)

# ---------------------------------------------------------------------------
# Synchronous (blocking) engine & session for tests / profiling
# This does NOT replace the async engine above — it's provided only for
# use-cases where an asyncio loop is undesired (simple tests, profiling, ad-hoc
# scripts).
# ---------------------------------------------------------------------------

SYNC_DATABASE_URL = (
    f"postgresql://{settings.DB_USER}:{settings.DB_PASSWORD}"
    f"@{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}"
)

# Blocking engine (uses a sync DB driver such as psycopg2)
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