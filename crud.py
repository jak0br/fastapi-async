from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from models import Product
from sqlalchemy.orm import Session as SyncSession


async def get_all_products(session: AsyncSession) -> list[Product]:
    result = await session.exec(select(Product))
    # .all() may be typed as Sequence; convert to a concrete list for the
    # declared return type list[Product]
    return list(result.all())


def get_all_products_sync(session: SyncSession) -> list[Product]:
    """Synchronous version of get_all_products for blocking sessions."""
    result = session.execute(select(Product))
    return list(result.scalars().all())
