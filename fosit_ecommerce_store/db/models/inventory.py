from tortoise import fields
from tortoise.models import Model


class TimestampMixin:
    created_at = fields.DatetimeField(null=False, auto_now_add=True)
    modified_at = fields.DatetimeField(null=False, auto_now=True)


class ProductCategories(Model):
    id = fields.UUIDField(pk=True)
    name = fields.CharField(max_length=255)
    description = fields.TextField(null=True)

    products: fields.ReverseRelation["Products"]

    def __str__(self) -> str:
        return self.name

    class Meta:
        table = "product_categories"
        ordering = ("name",)


class Products(TimestampMixin, Model):
    id = fields.UUIDField(pk=True)

    category: fields.ForeignKeyRelation[ProductCategories] = fields.ForeignKeyField(
        "models.ProductCategories",
        related_name="products",
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


class Inventory(TimestampMixin, Model):
    id = fields.UUIDField(pk=True)

    product: fields.ForeignKeyRelation[Products] = fields.ForeignKeyField(
        "models.Products",
        related_name="inventory_items",
    )

    quantity_change = fields.SmallIntField()
    running_total = fields.IntField()

    def __str__(self) -> str:
        return f"{str(self.id)} {self.product.name}"

    class Meta:
        table = "inventory"
        index = ("product_id",)
        ordering = ("-created_at",)


class LowStockAlerts(TimestampMixin, Model):
    id = fields.UUIDField(pk=True)

    product: fields.ForeignKeyRelation[Products] = fields.ForeignKeyField(
        "models.Products",
        related_name="low_stock_alerts",
    )

    alert_threshold = fields.SmallIntField()

    def __str__(self) -> str:
        return f"{str(self.id)} {self.product.name}"

    class Meta:
        table = "low_stock_alerts"
        index = ("product_id",)
        ordering = ("-created_at",)
