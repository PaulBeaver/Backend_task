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
            """
            SELECT
                COALESCE((
                    SELECT SUM(op.amount * p.price)
                    FROM orders_products op
                    JOIN orders o ON op.order_id = o.id
                    JOIN products p ON op.product_id = p.id
                    WHERE o.created_at BETWEEN :start_date AND :end_date
                ), 0) AS total_revenue,
                COALESCE((
                    SELECT SUM(op.amount * (p.price - p.cost))
                    FROM orders_products op
                    JOIN orders o ON op.order_id = o.id
                    JOIN products p ON op.product_id = p.id
                    WHERE o.created_at BETWEEN :start_date AND :end_date
                ), 0) AS total_profit,
                COALESCE((
                    SELECT SUM(op.amount)
                    FROM orders_products op
                    JOIN orders o ON op.order_id = o.id
                    WHERE o.created_at BETWEEN :start_date AND :end_date
                ), 0) AS total_units_sold,
                COALESCE((
                    SELECT COUNT(*)
                    FROM orders o
                    WHERE o.created_at BETWEEN :start_date AND :end_date
                      AND o.id IN (
                          SELECT op.order_id
                          FROM orders_products op
                          WHERE op.amount < 0
                      )
                ), 0) AS total_returns
            """
        )
        result = await session.execute(
            stmt, {"start_date": start_date, "end_date": end_date}
        )
        report = result.mappings().one()
        return report


report_crud: CrudReport = CrudReport(T, T)
