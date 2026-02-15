import uuid
from datetime import datetime

from sqlmodel import Field, Relationship, SQLModel

from app.types.enums import Currency


class ProductCategoryLink(SQLModel, table=True):
    product_id: uuid.UUID = Field(foreign_key="product.id", primary_key=True)
    category_id: uuid.UUID = Field(foreign_key="category.id", primary_key=True)


class Product(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    sku: int = Field(index=True, unique=True)
    name: str = Field()
    description: str | None = Field(default=None)
    price: float = Field(default=0.0)
    currency: Currency = Field(default="IDR")
    stock: int = Field(default=0)
    created_at: datetime = Field(default_factory=datetime.utcnow)

    categories: list["Category"] = Relationship(back_populates="products", link_model=ProductCategoryLink)


class Category(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    name: str = Field(index=True, unique=True)
    description: str | None = Field(default=None)
    created_at: datetime = Field(default_factory=datetime.utcnow)

    products: list["Product"] = Relationship(back_populates="categories", link_model=ProductCategoryLink)
