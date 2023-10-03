import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, NonNegativeInt, PositiveFloat


class ResponseBase(BaseModel):
    status_code: int
    message: str | None = "Operation successful!"
    error: bool = False


class InventoryBase(BaseModel):
    """Model to represent inventory update payload"""

    product_id: UUID
    quantity_change: int

    model_config = ConfigDict(from_attributes=True)


class InventoryOut(InventoryBase):
    id: UUID
    running_total: NonNegativeInt
    created_at: datetime.datetime
    modified_at: datetime.datetime


class InventoryResponse(ResponseBase):
    inventory_status: InventoryOut


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
    price: PositiveFloat

    model_config = ConfigDict(from_attributes=True)


class ProductsIn(BaseModel):
    products: list[ProductBase]


class ProductsOut(ProductBase):
    id: UUID


class ProductAddedResponse(ResponseBase):
    products: list[ProductsOut]
    products_rejected: list[ProductBase]


class ProductGetResponse(ResponseBase):
    products: list[ProductsOut]


class ErrorResponse(ResponseBase):
    status_code: int = 400
    error: bool = True
