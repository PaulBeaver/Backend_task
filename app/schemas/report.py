from .base import BaseSchema


class ReportSchema(BaseSchema):
    total_revenue: float
    total_profit: float
    total_units_sold: int
    total_returns: int
