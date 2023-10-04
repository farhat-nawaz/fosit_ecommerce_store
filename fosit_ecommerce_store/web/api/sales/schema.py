import datetime
import enum
from uuid import UUID

from pydantic import BaseModel, ConfigDict, PositiveFloat, PositiveInt


class TimeGrain(enum.Enum):
    DAILY = "DAILY"
    WEEKLY = "WEEKLY"
    MONTHLY = "MONTHLY"

    @classmethod
    def _missing_(cls, value):  # type:ignore
        for member in cls:
            if member.value == value.upper():
                return member
        return None


class ResponseBase(BaseModel):
    status_code: int
    message: str | None = "Operation successful!"
    error: bool = False


class ErrorResponse(ResponseBase):
    status_code: int = 400
    error: bool = True


class SaleBase(BaseModel):
    id: UUID
    product_id: UUID
    quantity: PositiveInt
    total_price: PositiveFloat
    created_at: datetime.datetime
    modified_at: datetime.datetime

    model_config = ConfigDict(from_attributes=True)


class SaleIn(BaseModel):
    products: list[UUID] | None = None
    categories: list[UUID] | None = None


class SaleByPeriodIn(BaseModel):
    period: TimeGrain


class SaleRawDataOut(ResponseBase):
    sales: list[SaleBase]


class SaleRevenueOut(BaseModel):
    date: str
    revenue: float

    model_config = ConfigDict(from_attributes=True)


class SaleRevenueCompareOut(BaseModel):
    category: str
    revenue_this_month: float
    revenue_last_month: float | None = None

    model_config = ConfigDict(from_attributes=True)


class SaleRevenueResponse(ResponseBase):
    revenue: list[SaleRevenueOut]


class SaleRevenueCompareResponse(ResponseBase):
    comparison_data: list[SaleRevenueCompareOut]
