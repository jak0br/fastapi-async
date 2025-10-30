from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from db.product import Product
from sqlalchemy.orm import Session as SyncSession
import time

class ProductRepository:

    def __init__(self, async_session: AsyncSession, sync_session: SyncSession):
        self.async_session = async_session
        self.sync_session = sync_session

    async def get_all_products(self) -> list[Product]:
        statement = select(Product)
        result = await self.async_session.exec(statement)
        return list(result.unique().all())

    def get_all_products_sync(self) -> list[Product]:
        """Synchronous version of get_all_products for blocking sessions."""
        result = self.sync_session.execute(select(Product))
        return list(result.scalars().all())

    def lock_thread(self):
        time.sleep(100)
