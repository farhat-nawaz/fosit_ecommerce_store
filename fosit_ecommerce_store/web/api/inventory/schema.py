import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, NonNegativeInt, PositiveFloat, PositiveInt


class ResponseBase(BaseModel):
    status_code: int
    message: str | None = "Operation successful!"
    error: bool = False


class SaleOut(BaseModel):
    id: UUID
    product_id: UUID
    quantity: PositiveInt
    total_price: PositiveFloat
    created_at: datetime.datetime
    modified_at: datetime.datetime

    model_config = ConfigDict(from_attributes=True)


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


class InventoryGetResponse(ResponseBase):
    inventory_status: list[InventoryOut]


class InventoryUpdateResponse(ResponseBase):
    inventory_status: InventoryOut
    sale: SaleOut | None = None


class InventorySaleResponse(InventoryUpdateResponse):
    sale: SaleOut | None = None


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
