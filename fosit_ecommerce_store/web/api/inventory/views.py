from fastapi import APIRouter, HTTPException

from fosit_ecommerce_store.web.api.inventory.dao import InventoryDAO
from fosit_ecommerce_store.web.api.inventory.schema import (
    CategoryAddedResponse,
    CategoryIn,
    ErrorResponse,
    InventoryBase,
    InventoryResponse,
    ProductAddedResponse,
    ProductGetResponse,
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


@router.get(
    "/get_products",
    status_code=200,
    response_model=ProductGetResponse,
)
async def get_products() -> ProductAddedResponse:
    """
    Returns all products in the database.

    It returns 200 if request is successful.
    """

    products = await InventoryDAO.get_all_products()
    return ProductGetResponse(status_code=200, products=products)  # type:ignore


@router.post(
    "/update_inventory",
    status_code=201,
    response_model=InventoryResponse,
)
async def update_inventory(payload: InventoryBase) -> InventoryResponse:
    """
    Update quantity of a product in inventory.

    Value for `quantity_change` should be:
        - negative if selling the product
        - positive if restocking the project

    It returns 201 if inventory is updated successfully.
    """
    if payload.quantity_change == 0:
        raise HTTPException(
            status_code=400,
            detail="Param 'quantity_change' cannot be 0",
        )

    inventory = await InventoryDAO.update_inventory(payload=payload)
    if inventory is None:
        raise HTTPException(status_code=400, detail="Invalid request params")

    return InventoryResponse(status_code=200, inventory_status=inventory)  # type:ignore
