from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.logger import logger

from app.domain.controller.fin_controller import FinController
from app.foundation.infra.database.database import get_db_session
from app.domain.model.schema.schema import (
    CompanyNameRequest,
    FinancialMetricsResponse
)

router = APIRouter()

@router.post("/financial", summary="회사명으로 재무제표 조회 (최근 3개년)", response_model=FinancialMetricsResponse)
async def get_financial_by_name(
    payload: CompanyNameRequest,
    db: AsyncSession = Depends(get_db_session)
):
    """
    회사명으로 재무제표를 조회합니다.
    - 최근 3개년(당기, 전기, 전전기)의 재무제표 데이터를 반환합니다.
    - 재무지표: 영업이익률, 순이익률, ROE, ROA
    - 성장성: 매출액 성장률, 순이익 성장률
    - 안정성: 부채비율, 유동비율
    """
    logger.info(f"🕞🕞🕞🕞🕞🕞get_financial_by_name 호출 - 회사명: {payload.company_name}")
    controller = FinController(db)
    return await controller.get_financial(company_name=payload.company_name)