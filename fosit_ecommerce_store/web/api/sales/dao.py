import uuid
from typing import Literal

import tortoise

from fosit_ecommerce_store.db.models.inventory import Products
from fosit_ecommerce_store.db.models.sales import Sales
from fosit_ecommerce_store.web.api.sales.schema import SaleIn


class SaleDAO:
    """Class to interact with database tables related to inventory"""

    periods_format_mapping: dict[str, str] = {
        "daily": "%Y-%m-%d",
        "weekly": "%Y-%u",
        "monthly": "%Y-%m-01",
    }

    @staticmethod
    async def get_raw_sales_data(params: SaleIn) -> list[Sales]:
        sales = Sales.filter()

        if params.products is not None and len(params.products):
            sales = sales.filter(product_id__in=params.products)

        if params.categories is not None and len(params.categories):
            product_ids = tortoise.expressions.Subquery(
                Products.filter(category_id__in=params.categories).values_list(
                    "id",
                    flat=True,
                ),
            )

            sales = sales.filter(product_id__in=product_ids).all()

        return await sales

    @classmethod
    async def get_revenue_by_period(
        cls,
        period: Literal["daily", "weekly", "monthly"],
    ) -> list[dict[str, str | float]]:
        revenue = (
            Sales.annotate(
                date=tortoise.expressions.RawSQL(
                    f"DATE_FORMAT(created_at, '{cls.periods_format_mapping[period]}')",
                ),
                revenue=tortoise.functions.Sum("total_price"),
            )
            .group_by("date")
            .values("date", "revenue")
        )

        return await revenue

    @classmethod
    async def compare_revenue_by_category_period(
        cls,
    ) -> list[dict[str, str | float]] | None:
        conn = tortoise.connections.get("default")

        try:
            revenue = await conn.execute_query_dict(
                cls._get_compare_revenue_by_category_period_query(),
            )
        except tortoise.exceptions.OperationalError:
            return None

        rvalue = {}
        for r in revenue:
            if r["category"] not in rvalue:
                rvalue[r["category"]] = {"category": r["category"]}

            rvalue[r["category"]][f"revenue_{r['period']}"] = r["revenue"]

        return list(rvalue.values())

    @staticmethod
    def generate_uuid() -> uuid.UUID:
        return uuid.uuid4()

    @staticmethod
    def _get_compare_revenue_by_category_period_query() -> str:
        return """
        SELECT
            category,
            SUM(total_price) AS revenue,
            CASE
                WHEN `rank` = 1 THEN "this_month"
                WHEN `rank` = 2 THEN "last_month"
            ELSE "unknown"
            END AS period
        FROM (
                SELECT
                    c.name AS category,
                    DATE_FORMAT(s.created_at, "%Y-%m-01") AS date,
                    s.total_price AS total_price,
                    ROW_NUMBER() OVER (PARTITION BY c.name ORDER BY DATE_FORMAT(s.created_at, "%Y-%m-01") DESC, c.name ASC) AS `rank` # noqa: E501
                FROM sales s
                INNER JOIN products p ON p.id = s.product_id
                INNER JOIN product_categories c ON c.id = p.category_id
        ) AS ranked_sales
        WHERE `rank` < 3
        GROUP BY category, date;
        """
