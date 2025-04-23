from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional
from fastapi.logger import logger

from app.domain.controller.fin_controller import FinController
from app.foundation.infra.database.database import get_db_session
from app.domain.model.schema.schema import (
    CompanyNameRequest,
    FinancialMetricsResponse
)

router = APIRouter()

@router.post("/financial", summary="회사명으로 재무제표 조회", response_model=FinancialMetricsResponse)
async def get_financial_by_name(
    payload: CompanyNameRequest,
    year: Optional[int] = Query(None, description="조회할 연도. 지정하지 않으면 직전 연도의 데이터를 조회"),
    db: AsyncSession = Depends(get_db_session)
):
    logger.info(f"🕞🕞🕞🕞🕞🕞get_financial_by_name 호출 - 회사명: {payload.company_name}, 연도: {year}")
    controller = FinController(db)
    return await controller.get_financial(company_name=payload.company_name, year=year)