from tortoise import fields
from tortoise.models import Model

from fosit_ecommerce_store.db.models.inventory import Products


class TimestampMixin(Model):
    created_at = fields.DatetimeField(null=False, auto_now_add=True)
    modified_at = fields.DatetimeField(null=False, auto_now=True)

    class Meta:
        abstract = True


class Sales(TimestampMixin):
    id = fields.UUIDField(pk=True)

    product: fields.ForeignKeyRelation[Products] = fields.ForeignKeyField(
        "models.Products",
        related_name="sold_items",
    )

    quantity = fields.SmallIntField()
    total_price = fields.IntField()

    def __str__(self) -> str:
        return f"{self.quantity} items of {self.product.name} for ${self.total_price}"

    class Meta:
        table = "sales"
        index = ("product_id",)
        ordering = ("-created_at", "product_id")
