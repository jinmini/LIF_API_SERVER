from app.domain.model.entity.report_entity import ReportEntity
from app.domain.model.schema.report_schema import ReportSchema
from app.domain.service.dart_api_service import DartApiService
from .action import ReportAction

class ReportFactory:
    _strategy_map = {
        ReportAction.GET: DartApiService(),
        ReportAction.GET_ALL: DartApiService(),
        ReportAction.CREATE: DartApiService(),
        ReportAction.UPDATE: DartApiService(),
        ReportAction.DELETE: DartApiService()
    }

    @staticmethod
    async def create(strategy: ReportAction, **kwargs):
        instance = ReportFactory._strategy_map[strategy]
        if not instance:
            raise Exception("Invalid strategy")
        return await instance.execute(**kwargs) 