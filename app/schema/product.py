from uuid import UUID

from pydantic import BaseModel, Field

from app.types.enums import Currency


class ProductResponse(BaseModel):
    id: UUID
    sku: int = Field(..., ge=3)
    name: str = Field(..., min_length=3, example="Sample Product")
    description: str | None = Field(default=None)
    price: float = Field(default=0.0, le=999999999.0)
    currency: Currency = Field(default="IDR")
    stock: int = Field(default=0, le=1000)


class ProductListResponse(BaseModel):
    data: list[ProductResponse]
    message: str


class ProductRequest(BaseModel):
    sku: int = Field(..., ge=3)
    name: str = Field(..., min_length=3, example="Sample Product")
    description: str | None = Field(default=None)
    price: float = Field(default=0.0, le=999999999.0)
    currency: Currency = Field(default="IDR")
    stock: int = Field(default=0, le=1000)


class ProductCreateResponse(BaseModel):
    data: ProductResponse
    message: str
