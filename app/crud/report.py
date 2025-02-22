from datetime import datetime

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession
from typing_extensions import TypeVar

from app.crud.base import CrudBase

T = TypeVar("T")


class CrudReport(CrudBase):
    async def get_report(self, session: AsyncSession, start_date: str, end_date: str):
        start_date, end_date = datetime.strptime(
            start_date, "%Y-%m-%d"
        ), datetime.strptime(end_date, "%Y-%m-%d")
        stmt = text(
            """WITH sales_data AS (
            SELECT
                op.order_id,
                op.product_id,
                op.amount,
                p.price,
                p.cost,
                o.created_at AS order_date
            FROM
                orders_products op
            JOIN
                products p ON op.product_id = p.id
            JOIN
                orders o ON op.order_id = o.id
            WHERE
                o.created_at BETWEEN :start_date AND :end_date
        ),
        total_revenue AS (
            SELECT
                COALESCE(SUM(amount * price), 0) AS total_revenue
            FROM
                sales_data
        ),
        total_profit AS (
            SELECT
                COALESCE(SUM(amount * (price - cost)), 0) AS total_profit
            FROM
                sales_data
        ),
        units_sold AS (
            SELECT
                COALESCE(SUM(amount), 0) AS total_units_sold
            FROM
                sales_data
        ),
        returns AS (
            SELECT
                COALESCE(COUNT(*), 0) AS total_returns
            FROM
                orders o
            WHERE
                o.created_at BETWEEN :start_date AND :end_date
                AND o.id IN (
                    SELECT
                        op.order_id
                    FROM
                        orders_products op
                    WHERE
                        op.amount < 0
                )
        )
        SELECT
            tr.total_revenue,
            tp.total_profit,
            us.total_units_sold,
            r.total_returns
        FROM
            total_revenue tr,
            total_profit tp,
            units_sold us,
            returns r;"""
        )
        result = await session.execute(
            stmt, {"start_date": start_date, "end_date": end_date}
        )
        report = result.mappings().one()
        return report


report_crud: CrudReport = CrudReport(T, T)
