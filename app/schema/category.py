from uuid import UUID

from pydantic import BaseModel, Field


class CategoryResponse(BaseModel):
    id: UUID
    name: str = Field(..., min_length=3, example="Sample Category")
    description: str | None = Field(default=None)


class CategoryListResponse(BaseModel):
    data: list[CategoryResponse]
    message: str


class CategoryRequest(BaseModel):
    name: str = Field(..., min_length=3, example="Sample Category")
    description: str | None = Field(default=None)


class CategoryCreateResponse(BaseModel):
    data: CategoryResponse
    message: str


class CategoryUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=3)
    description: str | None = None
