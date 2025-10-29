from fastapi import FastAPI, Depends
from contextlib import asynccontextmanager
from sqlmodel.ext.asyncio.session import AsyncSession
from app.db.database import get_session, init_db, get_sync_db, engine
from crud import get_all_products, get_all_products_sync
from models import ProductRead
from sqlalchemy.orm import Session as SyncSession

@asynccontextmanager
async def lifespan(app: FastAPI):
    # --- Startup phase ---
    await init_db()  # create tables or migrations, one-time setup
    yield
    # --- Shutdown phase ---
    # Here you could close the engine or cleanup resources if needed
    await engine.dispose()  # optional: close all pooled connections gracefully

app = FastAPI(
    title="SQLModel + FastAPI + asyncpg (pooled)",
    lifespan=lifespan
)

@app.get("/products", response_model=list[ProductRead])
async def list_products(session: AsyncSession = Depends(get_session)):

    products = await get_all_products(session)
    return products


@app.get("/porduct_sync", response_model=list[ProductRead])
def porduct_sync(session: SyncSession = Depends(get_sync_db)):
    """Synchronous endpoint using the blocking Session and sync CRUD."""
    products = get_all_products_sync(session)
    return products
