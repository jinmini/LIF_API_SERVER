from app.domain.model.entity.statement_entity import StatementEntity
from app.domain.model.schema.statement_schema import StatementSchema
from app.domain.service.fin_service import FinService
from .action import StatementAction

class StatementFactory:
    _strategy_map = {
        StatementAction.GET: FinService(),
        StatementAction.GET_ALL: FinService(),
        StatementAction.CREATE: FinService(),
        StatementAction.UPDATE: FinService(),
        StatementAction.DELETE: FinService()
    }

    @staticmethod
    async def create(strategy: StatementAction, **kwargs):
        instance = StatementFactory._strategy_map[strategy]
        if not instance:
            raise Exception("Invalid strategy")
        return await instance.execute(**kwargs) 