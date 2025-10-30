from collections.abc import AsyncGenerator
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import SQLModel
from db.config import settings

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

