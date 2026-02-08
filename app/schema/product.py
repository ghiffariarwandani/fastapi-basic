from typing import Literal
from pydantic import BaseModel, Field


class ProductResponse(BaseModel):
  id: int
  sku: int = Field(..., ge=3)
  name: str = Field(..., min_length=3, example="Sample Product")
  description: str | None = Field(default=None)
  price: float = Field(default=0.0, le=999999999.0) 
  currency: Literal["USD", "IDR"] = Field(default="IDR")
  stock: int = Field(default=0,le=1000)

class ProductRequest(BaseModel):
  sku: int = Field(..., ge=3)
  name: str = Field(..., min_length=3, example="Sample Product")
  description: str | None = Field(default=None)
  price: float = Field(default=0.0, le=999999999.0) 
  currency: Literal["USD", "IDR"] = Field(default="IDR")
  stock: int = Field(default=0,le=1000)
