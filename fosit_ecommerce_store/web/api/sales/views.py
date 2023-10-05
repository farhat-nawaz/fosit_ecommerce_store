from fastapi import APIRouter

from fosit_ecommerce_store.web.api.sales.dao import SaleDAO
from fosit_ecommerce_store.web.api.sales.schema import (
    SaleIn,
    SaleRawDataOut,
    SaleRevenueCompareResponse,
    SaleRevenueResponse,
    TimeGrain,
)

router = APIRouter()


@router.get(
    "/compare",
    status_code=200,
    response_model=SaleRevenueCompareResponse,
)
async def compare_revenue_by_category_period() -> SaleRawDataOut:
    """
    Get comparison of sales data of categories across different periods.

    It returns 200 for a successful request.
    """
    comparison_data = await SaleDAO.compare_revenue_by_category_period()

    return SaleRevenueCompareResponse(
        status_code=200,
        comparison_data=comparison_data,  # type:ignore
    )


@router.get(
    "/raw_data",
    status_code=200,
    response_model=SaleRawDataOut,
)
async def raw_data(payload: SaleIn) -> SaleRawDataOut:
    """
    Get raw sales data. You can filter by product and category.

    It returns 200 for a successful request.
    """
    sales = await SaleDAO.get_raw_sales_data(payload)

    return SaleRawDataOut(status_code=200, sales=sales)  # type:ignore


@router.get(
    "/by_period",
    status_code=200,
    response_model=SaleRevenueResponse,
)
async def revenue_by_period(
    period: TimeGrain,
) -> SaleRevenueResponse:
    """
    Get sales data grouped by a period.

    It returns 200 for a successful request.
    """
    revenue = await SaleDAO.get_revenue_by_period(period)

    return SaleRevenueResponse(status_code=200, revenue=revenue)  # type:ignore
