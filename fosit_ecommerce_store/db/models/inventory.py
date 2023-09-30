from tortoise import fields
from tortoise.models import Model


class TimestampMixin(Model):
    created_at = fields.DatetimeField(null=False, auto_now_add=True)
    modified_at = fields.DatetimeField(null=False, auto_now=True)

    class Meta:
        abstract = True


class ProductCategory(TimestampMixin):
    id = fields.UUIDField(pk=True, index=True)
    name = fields.CharField(max_length=255)
    description = fields.TextField(null=True)

    products: fields.ReverseRelation["Products"]

    def __str__(self) -> str:
        return self.name

    class Meta:
        table = "product_categories"
        ordering = ("name",)


class Products(TimestampMixin):
    id = fields.UUIDField(pk=True, index=True)

    category: fields.ForeignKeyRelation[ProductCategory] = fields.ForeignKeyField(
        "models.ProductCategory",
        related_name="products",
        index=True,
    )

    name = fields.CharField(max_length=255)
    description = fields.TextField(null=True)
    price = fields.IntField()

    inventory_items: fields.ReverseRelation["Inventory"]
    low_stock_alerts: fields.ReverseRelation["LowStockAlerts"]

    def __str__(self) -> str:
        return self.name

    class Meta:
        table = "products"
        index = ("id",)
        ordering = ("name",)


class Inventory(TimestampMixin):
    id = fields.UUIDField(pk=True, index=True)

    product: fields.ForeignKeyRelation[Products] = fields.ForeignKeyField(
        "models.Products",
        related_name="inventory_items",
        index=True,
    )

    quantity_change = fields.SmallIntField()
    running_total = fields.IntField()

    def __str__(self) -> str:
        return f"{str(self.id)} {self.product.name}"

    class Meta:
        table = "inventory"
        index = ("product_id",)
        ordering = ("-created_at",)


class LowStockAlerts(TimestampMixin):
    id = fields.UUIDField(pk=True)

    product: fields.ForeignKeyRelation[Products] = fields.ForeignKeyField(
        "models.Products",
        related_name="low_stock_alerts",
        index=True,
    )

    alert_threshold = fields.SmallIntField()

    def __str__(self) -> str:
        return f"{str(self.id)} {self.product.name}"

    class Meta:
        table = "low_stock_alerts"
        index = ("product_id",)
        ordering = ("-created_at",)
