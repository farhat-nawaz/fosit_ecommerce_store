import uuid

from pydantic.types import PositiveInt

from fosit_ecommerce_store.db.models.inventory import (
    Inventory,
    LowStockAlerts,
    ProductCategory,
    Products,
)
from fosit_ecommerce_store.db.models.sales import Sales
from fosit_ecommerce_store.web.api.inventory.schema import (
    CategoryBase,
    InventoryBase,
    ProductBase,
)


class InventoryDAO:
    """Class to interact with database tables related to inventory"""

    @classmethod
    async def add_new_categories(
        cls,
        categories: list[CategoryBase],
    ) -> list[ProductCategory]:
        categories_db = []

        for category in categories:
            category_db = ProductCategory(
                **category.model_dump(), id=cls.generate_uuid()
            )
            categories_db.append(category_db)

        return await ProductCategory.bulk_create(categories_db, batch_size=4000)

    @classmethod
    async def add_new_products(
        cls,
        products: list[ProductBase],
        fetch_related: bool = False,
    ) -> tuple[list[Products], list[ProductBase]]:
        products_db = []

        for product in products:
            product_db = Products(**product.model_dump(), id=cls.generate_uuid())
            products_db.append(product_db)

        products_db = await Products.bulk_create(
            products_db,
            batch_size=4000,
            ignore_conflicts=True,
        )

        # This algorithm efficiently divides added and rejected objects
        # TODO: provide rejection reason
        i = j = 0
        for _ in range(len(products)):
            if products_db[j].category is not None:
                if fetch_related:
                    await products_db[j].fetch_related("category")

                products.pop(i)
                j += 1

            else:
                products_db.pop(j)
                i += 1

        return products_db, products  # products added, products rejected

    @classmethod
    async def add_new_sale(
        cls,
        product_id: uuid.UUID,
        quantity: PositiveInt,
    ) -> Sales:
        product = await Products.get(id=product_id)

        sale = Sales(
            id=cls.generate_uuid(),
            product=product,
            quantity=quantity,
            total_price=product.price * quantity,
        )
        await sale.save()

        return sale

    @classmethod
    async def generate_low_stock_alert(cls, product: Products) -> LowStockAlerts:
        alert = LowStockAlerts(
            id=cls.generate_uuid(),
            product=product,
            alert_threshold=product.low_stock_alert_threshold,
        )
        await alert.save()

        return alert

    @classmethod
    async def get_inventory_status(cls) -> list[Inventory]:
        return await Inventory.raw(cls._get_inventory_status_query())  # type:ignore

    @classmethod
    async def update_inventory(cls, payload: InventoryBase) -> Inventory | None:
        # TODO: provide meaningful error messages
        product = await Products.get_or_none(id=payload.product_id)
        if product is None:
            return None

        inventory_db_existing = await Inventory.filter(product=product).first()

        running_total = payload.quantity_change
        if inventory_db_existing is not None:
            running_total += inventory_db_existing.running_total

        if running_total < 0:
            return None

        inventory = Inventory(
            id=cls.generate_uuid(),
            product=product,
            quantity_change=payload.quantity_change,
            running_total=running_total,
        )
        await inventory.save()

        if inventory.running_total < product.low_stock_alert_threshold:
            await cls.generate_low_stock_alert(product=product)

        return inventory

    @staticmethod
    def generate_uuid() -> uuid.UUID:
        return uuid.uuid4()

    @staticmethod
    async def get_all_products() -> list[Products]:
        return await Products.all()

    @staticmethod
    def _get_inventory_status_query() -> str:
        return """
            SELECT i.*
            FROM inventory i
            INNER JOIN (
                SELECT product_id, MAX(created_at) AS max_date
                FROM inventory
                GROUP BY product_id
            ) latest ON i.product_id = latest.product_id AND i.created_at = latest.max_date;
        """
