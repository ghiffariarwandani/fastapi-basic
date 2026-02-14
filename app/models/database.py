import uuid
from datetime import datetime

from sqlmodel import Field, SQLModel

from app.types.enums import Currency


class Product(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    sku: int = Field(index=True, unique=True)
    name: str = Field()
    description: str | None = Field(default=None)
    price: float = Field(default=0.0)
    currency: Currency = Field(default="IDR")
    stock: int = Field(default=0)
    created_at: datetime = Field(default_factory=datetime.utcnow)
