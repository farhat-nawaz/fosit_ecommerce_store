import uuid

from fosit_ecommerce_store.db.models.inventory import ProductCategory, Products
from fosit_ecommerce_store.web.api.inventory.schema import CategoryBase, ProductBase


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

    @staticmethod
    def generate_uuid() -> uuid.UUID:
        return uuid.uuid4()
