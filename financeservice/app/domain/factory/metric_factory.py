from app.domain.model.entity.metric_entity import MetricEntity
from app.domain.model.schema.metric_schema import MetricSchema
from app.domain.service.ratio_service import RatioService
from .action import MetricAction

class MetricFactory:
    _strategy_map = {
        MetricAction.GET: RatioService(),
        MetricAction.GET_ALL: RatioService(),
        MetricAction.CREATE: RatioService(),
        MetricAction.UPDATE: RatioService(),
        MetricAction.DELETE: RatioService()
    }

    @staticmethod
    async def create(strategy: MetricAction, **kwargs):
        instance = MetricFactory._strategy_map[strategy]
        if not instance:
            raise Exception("Invalid strategy")
        return await instance.execute(**kwargs) 