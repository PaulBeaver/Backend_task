from fastapi import Request
from fastapi_cache.decorator import cache

from app.crud import report_crud
from app.schemas import ReportSchema

from .base import BaseRouter


class ReportRouter(BaseRouter):
    def __init__(self, model_crud, prefix) -> None:
        super().__init__(model_crud, prefix)

    def setup_routes(self) -> None:
        self.router.add_api_route(
            f"{self.prefix}-all",
            self.report,
            methods=["GET"],
            status_code=200,
            description="date in format: 2023-12-31",
        )

    @cache(expire=60 * 30)
    async def report(
        self, request: Request, start_date: str, end_date: str
    ) -> ReportSchema:
        return await report_crud.get_report(request.state.session, start_date, end_date)


report_router = ReportRouter(report_crud, "/reports").router
