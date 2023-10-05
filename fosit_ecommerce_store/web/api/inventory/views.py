from fastapi import APIRouter, HTTPException
from tortoise import transactions

from fosit_ecommerce_store.web.api.inventory.dao import InventoryDAO
from fosit_ecommerce_store.web.api.inventory.schema import (
    CategoryAddedResponse,
    CategoryIn,
    ErrorResponse,
    InventoryBase,
    InventoryGetResponse,
    InventoryOut,
    InventoryUpdateResponse,
    ProductAddedResponse,
    ProductGetResponse,
    ProductsIn,
    ResponseBase,
    SaleOut,
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


@router.get(
    "/status",
    status_code=200,
    response_model=InventoryGetResponse,
)
async def get_inventory_status() -> InventoryGetResponse:
    """
    Returns latest inventory status for all products

    It returns 200 for a successful response.
    """
    inventory_status = await InventoryDAO.get_inventory_status()

    return InventoryGetResponse(
        status_code=200,
        inventory_status=inventory_status,  # type:ignore
    )


@router.post(
    "/update_inventory",
    status_code=201,
    response_model=InventoryUpdateResponse,
)
async def update_inventory(payload: InventoryBase) -> ResponseBase:
    """
    Update quantity of a product in inventory.

    Value for `quantity_change` should be:
    - negative if selling the product
    - positive if restocking the product

    It returns 201 if inventory is updated successfully.
    """
    if payload.quantity_change == 0:
        raise HTTPException(
            status_code=400,
            detail="Param 'quantity_change' cannot be 0",
        )

    async with transactions.in_transaction():
        inventory = await InventoryDAO.update_inventory(payload=payload)
        if inventory is None:
            raise HTTPException(status_code=400, detail="Invalid request params")

        response = InventoryUpdateResponse(
            status_code=200,
            inventory_status=InventoryOut.model_validate(inventory),
        )

        if payload.quantity_change < 0:
            sale = await InventoryDAO.add_new_sale(
                payload.product_id,
                abs(payload.quantity_change),
            )
            response.sale = SaleOut.model_validate(sale)

    return response
