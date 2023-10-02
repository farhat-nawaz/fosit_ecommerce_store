from uuid import UUID

from pydantic import BaseModel, ConfigDict


class ResponseBase(BaseModel):
    status_code: int
    message: str | None = "Operation successful!"
    error: bool = False


class Inventory(BaseModel):
    """Model to represent inventory update payload"""

    product_id: UUID
    quantity: int


class CategoryBase(BaseModel):
    """Model to represent product category payload"""

    name: str
    description: str


class CategoryIn(BaseModel):
    categories: list[CategoryBase]


class CategoryOut(CategoryBase):
    id: UUID

    model_config = ConfigDict(from_attributes=True)


class CategoryResponse(ResponseBase):
    categories: str


class CategoryAddedResponse(ResponseBase):
    categories: list[CategoryOut]


class ProductBase(BaseModel):
    """Model to represent product payload"""

    category_id: UUID
    name: str
    description: str
    price: float


class ProductsIn(BaseModel):
    products: list[ProductBase]


class ProductsOut(ProductBase):
    id: UUID

    model_config = ConfigDict(from_attributes=True)


class ProductAddedResponse(ResponseBase):
    products: list[ProductsOut]


class ErrorResponse(ResponseBase):
    error: bool = True
