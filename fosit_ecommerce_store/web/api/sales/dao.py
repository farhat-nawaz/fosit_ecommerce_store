import uuid

import tortoise
from tortoise.expressions import Q

from fosit_ecommerce_store.db.models.inventory import Products
from fosit_ecommerce_store.db.models.sales import Sales
from fosit_ecommerce_store.web.api.sales.schema import SaleIn, TimeGrain


class SaleDAO:
    """Class to interact with database tables related to inventory"""

    periods_format_mapping: dict[TimeGrain, str] = {
        TimeGrain.DAILY: "%Y-%m-%d",
        TimeGrain.WEEKLY: "%Y-%u",
        TimeGrain.MONTHLY: "%Y-%m-01",
    }

    @staticmethod
    async def get_raw_sales_data(params: SaleIn) -> list[Sales]:
        query = Q()

        if params.products is not None and len(params.products):
            query = query | Q(product_id__in=params.products)

        if params.categories is not None and len(params.categories):
            product_ids = tortoise.expressions.Subquery(
                Products.filter(category_id__in=params.categories).values_list(
                    "id",
                    flat=True,
                ),
            )
            query = query | Q(product_id__in=product_ids)

        return await Sales.filter(query)

    @classmethod
    async def get_revenue_by_period(
        cls,
        period: TimeGrain,
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
        except tortoise.exceptions.OperationalError as e:
            raise e

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
        SELECT category, revenue, CASE
                WHEN `rank` = 1 THEN "this_month"
                WHEN `rank` = 2 THEN "last_month"
            ELSE "unknown"
            END AS period
        FROM (
            SELECT
                category,
                SUM(total_price) AS revenue,
                ROW_NUMBER() OVER (PARTITION BY category ORDER BY date DESC) AS `rank`
            FROM (
                    SELECT
                        c.name AS category,
                        DATE_FORMAT(s.created_at, "%Y-%m-01") AS date,
                        s.total_price AS total_price
                    FROM sales s
                    INNER JOIN products p ON p.id = s.product_id
                    INNER JOIN product_categories c ON c.id = p.category_id
            ) AS base_table
            GROUP BY category, date
        ) AS ranked_sales

        WHERE `rank` < 3;
        """
