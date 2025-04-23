from app.domain.model.entity.company_entity import CompanyEntity
from app.domain.model.schema.company_schema import CompanySchema
from app.domain.service.company_info_service import CompanyInfoService
from .action import CompanyAction

class CompanyFactory:
    _strategy_map = {
        CompanyAction.GET: CompanyInfoService(),
        CompanyAction.GET_ALL: CompanyInfoService(),
        CompanyAction.CREATE: CompanyInfoService(),
        CompanyAction.UPDATE: CompanyInfoService(),
        CompanyAction.DELETE: CompanyInfoService()
    }

    @staticmethod
    async def create(strategy: CompanyAction, **kwargs):
        instance = CompanyFactory._strategy_map[strategy]
        if not instance:
            raise Exception("Invalid strategy")
        return await instance.execute(**kwargs) 