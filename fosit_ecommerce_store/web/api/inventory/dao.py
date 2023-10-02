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
    async def add_new_products(cls, products: list[ProductBase]) -> list[Products]:
        products_db = []

        for product in products:
            product_db = Products(**product.model_dump(), id=cls.generate_uuid())
            products_db.append(product_db)

        # products =

        # products = Products.bulk_create(
        #     map(
        #         lambda obj: Products(**obj.model_dump(), id=cls.generate_uuid()),
        #         products,
        #     ),
        #     batch_size=4000,
        # )

        return await Products.bulk_create(products_db, batch_size=4000)

    # @classmethod
    # async def verify_foreign_keys_exist(
    #     cls, model: BaseModel, keys: list[uuid.UUID]
    # ) -> bool:
    #     """"""

    @staticmethod
    def generate_uuid() -> uuid.UUID:
        return uuid.uuid4()
