from typing import Optional
from sqlmodel import SQLModel, Field

# ORM table
class Product(SQLModel, table=True):
    __tablename__ = "products"  # optional, explicit name
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    price: float

# Response schema (no table)
class ProductRead(SQLModel):
    id: int
    name: str
    price: float