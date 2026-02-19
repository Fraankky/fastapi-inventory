from datetime import datetime, timezone
from enum import Enum

from sqlmodel import SQLModel, Field, Relationship


class MovementType(str, Enum):
    IN = "in"
    OUT = "out"
    

class Category(SQLModel, table=True):

    id: int = Field(default=None, primary_key=True)
    name: str = Field(index=True, unique=True)
    description: str = Field(default=None)


    products: list["Product"] = Relationship(back_populates="category")

class Product(SQLModel, table=True):

    id: int = Field(default=None, primary_key=True)
    name: str
    description: str = Field(default=None)

    category_id: int = Field(foreign_key="category.id")

    category: "Category" = Relationship(back_populates="products")
    movements: list["StockMovement"] = Relationship(back_populates="product")


class StockMovement(SQLModel, table=True):

    id: int = Field(default=None, primary_key=True)
    product_id: int = Field(foreign_key="product.id", index=True)

    # IN = barang masuk, OUT = barang keluar
    type: MovementType = Field(index=True)
    quantity: int = Field(gt=0)
    note: str = Field(default=None)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    product: "Product" = Relationship(back_populates="movements")

