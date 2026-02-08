import uuid
from enum import Enum
from sqlmodel import Field, SQLModel

class Currency(str, Enum):
  USD = "USD"
  IDR = "IDR"

class Product(SQLModel, table=True):
  id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
  sku: int = Field(index=True, unique=True)
  name: str = Field()
  description: str | None = Field(default=None)
  price: float = Field(default=0.0)
  currency: Currency = Field(default="IDR")
  stock: int = Field(default=0)
  created_at: str = Field(default_factory=lambda: __import__('datetime').datetime.utcnow().isoformat())