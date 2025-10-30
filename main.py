from fastapi import FastAPI
from contextlib import asynccontextmanager
from db.database import init_db, engine
from api.product import router as product_router

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

app.include_router(product_router)
