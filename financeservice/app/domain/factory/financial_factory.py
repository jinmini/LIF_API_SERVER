from app.domain.model.entity.financial_entity import FinancialEntity
from app.domain.model.schema.financial_schema import FinancialSchema
from app.domain.service.financial_statement_service import FinancialStatementService
from .action import FinancialAction

class FinancialFactory:
    _strategy_map = {
        FinancialAction.GET: FinancialStatementService(),
        FinancialAction.GET_ALL: FinancialStatementService(),
        FinancialAction.CREATE: FinancialStatementService(),
        FinancialAction.UPDATE: FinancialStatementService(),
        FinancialAction.DELETE: FinancialStatementService()
    }

    @staticmethod
    async def create(strategy: FinancialAction, **kwargs):
        instance = FinancialFactory._strategy_map[strategy]
        if not instance:
            raise Exception("Invalid strategy")
        return await instance.execute(**kwargs) 