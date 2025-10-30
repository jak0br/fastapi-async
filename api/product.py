from fastapi import APIRouter, Depends
from db.product_repository import ProductRepository
from db.product import ProductRead
from db.database import get_session
from db.sync_db import get_sync_db
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.orm import Session as SyncSession

router = APIRouter()

def _create_product_repo(
    async_session: AsyncSession = Depends(get_session),
    sync_session: SyncSession = Depends(get_sync_db)
) -> ProductRepository:
    return ProductRepository(async_session=async_session, sync_session=sync_session)

@router.get("/products", response_model=list[ProductRead])
async def list_products(repo: ProductRepository = Depends(_create_product_repo)):
    products = await repo.get_all_products()
    return products

@router.get("/sleep_async")
async def sleep_async(repo: ProductRepository = Depends(_create_product_repo)):
    repo.lock_thread()
    return "sleeping"

@router.get("/sleep_sync")
def sleep_sync(repo: ProductRepository = Depends(_create_product_repo)):
    repo.lock_thread()
    return "sleeping"

@router.get("/product_sync", response_model=list[ProductRead])
def product_sync(repo: ProductRepository = Depends(_create_product_repo)):
    products = repo.get_all_products_sync()
    return products

