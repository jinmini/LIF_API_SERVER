from pydantic import Field
from typing import List, Optional
from datetime import datetime
from app.foundation.infra.database.base_schema import BaseSchema

# DART API 원본 데이터 스키마
class DartApiResponse(BaseSchema):
    """DART API 응답 기본 구조"""
    status: str = Field(..., description="API 응답 상태")
    message: str = Field(..., description="API 응답 메시지")
    list: Optional[List[dict]] = Field(None, description="API 응답 데이터 리스트")

    model_config = {
        "from_attributes": True
    }

class AccountsForRatios(BaseSchema):
    """재무비율 계산에 필요한 계정과목 데이터"""
    # 안정성 지표 계산용 계정
    total_liabilities: Optional[str] = Field(None, description="부채총계 (부채비율)")
    total_equity: Optional[str] = Field(None, description="자본총계 (부채비율)")
    current_assets: Optional[str] = Field(None, description="유동자산 (유동비율)")
    current_liabilities: Optional[str] = Field(None, description="유동부채 (유동비율)")
    operating_income: Optional[str] = Field(None, description="영업이익 (이자보상배율)")
    interest_expense: Optional[str] = Field(None, description="이자비용 (이자보상배율)")

    # 수익성 지표 계산용 계정
    net_income: Optional[str] = Field(None, description="당기순이익 (ROE, ROA)")
    total_assets: Optional[str] = Field(None, description="자산총계 (ROA)")

    # 건전성 지표 계산용 계정
    borrowings: Optional[str] = Field(None, description="차입금 (차입금의존도)")
    operating_cash_flow: Optional[str] = Field(None, description="영업활동현금흐름 (현금흐름대부채비율)")

    # 성장성 지표 계산용 계정
    revenue: Optional[str] = Field(None, description="당기 매출액 (매출 성장률)")
    prev_revenue: Optional[str] = Field(None, description="전기 매출액")
    prev_operating_income: Optional[str] = Field(None, description="전기 영업이익 (영업이익 성장률)")
    eps: Optional[str] = Field(None, description="당기 EPS (EPS 성장률)")
    prev_eps: Optional[str] = Field(None, description="전기 EPS")

    model_config = {
        "from_attributes": True
    }

class RawFinancialStatement(BaseSchema):
    """DART API 재무제표 원본 데이터"""
    rcept_no: str = Field(..., description="접수번호")
    reprt_code: str = Field(..., description="보고서 코드")
    bsns_year: str = Field(..., description="사업연도")
    corp_code: str = Field(..., description="회사 코드")
    sj_div: str = Field(..., description="재무제표 구분")
    sj_nm: str = Field(..., description="재무제표명")
    account_nm: str = Field(..., description="계정명")
    thstrm_nm: str = Field(..., description="당기명")
    thstrm_amount: str = Field(..., description="당기금액")
    frmtrm_nm: str = Field(..., description="전기명")
    frmtrm_amount: str = Field(..., description="전기금액")
    bfefrmtrm_nm: str = Field(..., description="전전기명")
    bfefrmtrm_amount: Optional[str] = Field(None, description="전전기금액")
    ord: int = Field(..., description="계정과목 정렬순서")
    currency: str = Field(..., description="통화 단위")

    model_config = {
        "from_attributes": True
    }

class CompanyInfo(BaseSchema):
    """DART에서 제공하는 회사 기본 정보"""
    corp_code: str = Field(..., description="회사 코드")
    corp_name: str = Field(..., description="회사명")
    stock_code: str = Field(..., description="주식 코드")
    modify_date: str = Field(..., description="최종 수정일")

    model_config = {
        "from_attributes": True
    }

class StockInfo(BaseSchema):
    """주식 발행정보"""
    istc_totqy: int = Field(..., description="발행한 주식의 총수")
    distb_stock_qy: int = Field(..., description="유통주식수")
    tesstk_co: int = Field(..., description="자기주식수")

    model_config = {
        "from_attributes": True
    }

class CompanyNameRequest(BaseSchema):
    company_name: str = Field(..., description="회사명")

    model_config = {
        "from_attributes": True
    }

class FinancialMetrics(BaseSchema):
    operatingMargin: List[float] = Field(..., description="영업이익률")
    netMargin: List[float] = Field(..., description="순이익률")
    roe: List[float] = Field(..., description="자기자본이익률")
    roa: List[float] = Field(..., description="총자산이익률")
    years: List[str] = Field(..., description="연도 목록")

    model_config = {
        "from_attributes": True
    }

class GrowthData(BaseSchema):
    revenueGrowth: List[float] = Field(..., description="매출액 성장률")
    netIncomeGrowth: List[float] = Field(..., description="순이익 성장률")
    years: List[str] = Field(..., description="연도 목록")

    model_config = {
        "from_attributes": True
    }

class DebtLiquidityData(BaseSchema):
    debtRatio: List[float] = Field(..., description="부채비율")
    currentRatio: List[float] = Field(..., description="유동비율")
    years: List[str] = Field(..., description="연도 목록")

    model_config = {
        "from_attributes": True
    }

class FinancialMetricsResponse(BaseSchema):
    companyName: str = Field(..., description="회사명")
    financialMetrics: FinancialMetrics = Field(..., description="재무지표 데이터")
    growthData: GrowthData = Field(..., description="성장성 데이터")
    debtLiquidityData: DebtLiquidityData = Field(..., description="부채 및 유동성 데이터")

    model_config = {
        "from_attributes": True
    }