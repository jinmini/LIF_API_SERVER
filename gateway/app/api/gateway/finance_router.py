"""
Finance 라우터
- Finance 엔드포인트

"""

from fastapi import APIRouter, Request
import httpx
import os
from typing import Dict, Any
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/fin", tags=["fin"])

FINANCE_SERVICE_URL = os.getenv("FINANCE_SERVICE_URL")


@router.post("/financial")
async def get_financial_by_name(company_name: str) -> Dict[str, Any]:
    """
    회사명으로 재무제표를 조회합니다.
    """
    logger.info(f"게이트웨이 financial 엔드포인트 호출 - 회사명: {company_name}")
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{FINANCE_SERVICE_URL}/e/fin/financial",
            json={"company_name": company_name}
        )
        logger.info(f"MS 응답 상태 코드: {response.status_code}")
        return response.json()