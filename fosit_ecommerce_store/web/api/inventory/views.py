from fastapi import APIRouter

from fosit_ecommerce_store.web.api.inventory.dao import InventoryDAO
from fosit_ecommerce_store.web.api.inventory.schema import (
    CategoryAddedResponse,
    CategoryIn,
    ErrorResponse,
    Inventory,
    ProductAddedResponse,
    ProductsIn,
)

router = APIRouter()


@router.post(
    "/add_categories",
    status_code=201,
    response_model=CategoryAddedResponse,
)
async def add_product_categories(payload: CategoryIn) -> CategoryAddedResponse:
    """
    Add new categories to the system.

    It returns 201 if category is added successfully.
    """
    categories = await InventoryDAO.add_new_categories(categories=payload.categories)

    return CategoryAddedResponse(status_code=201, categories=categories)  # type:ignore


@router.post(
    "/add_products",
    status_code=201,
    response_model=ProductAddedResponse,
    responses={404: {"model": ErrorResponse}},
)
async def add_products(payload: ProductsIn) -> ProductAddedResponse:
    """
    Add new products to the system.

    It returns 201 if product is added successfully.
    """

    products, products_rejected = await InventoryDAO.add_new_products(
        products=payload.products,
        fetch_related=True,
    )

    return ProductAddedResponse(
        status_code=201,
        products=products,  # type:ignore
        products_rejected=products_rejected,
    )  # type:ignore


@router.post("/update_inventory")
def update_inventory(payload: Inventory) -> None:
    """
    Checks the health of a project.

    It returns 200 if the project is healthy.
    """
