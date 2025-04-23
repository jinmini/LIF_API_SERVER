from typing import Dict, Any, Optional, List
from sqlalchemy.ext.asyncio import AsyncSession
import logging
from datetime import datetime
from sqlalchemy import text

logger = logging.getLogger(__name__)

class RatioService:
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    def _calculate_growth_rate(self, current: float, previous: float) -> float:
        """성장률을 계산합니다."""
        if previous == 0:
            return 0.0
        return ((current - previous) / abs(previous)) * 100

    async def _get_financial_statements(self, corp_code: str, bsns_year: str) -> List[Dict[str, Any]]:
        """재무제표 데이터를 조회합니다."""
        query = text("""
            SELECT * FROM fin_data 
            WHERE corp_code = :corp_code 
            AND bsns_year = :bsns_year
            AND sj_div IN ('BS', 'IS')
            ORDER BY sj_div, ord
        """)
        result = await self.db_session.execute(query, {
            "corp_code": corp_code,
            "bsns_year": bsns_year
        })
        
        statements = []
        for row in result:
            row_dict = {}
            for idx, column in enumerate(result.keys()):
                row_dict[column] = row[idx]
            statements.append(row_dict)
        
        return statements

    def _extract_financial_data(self, statements: List[Dict[str, Any]]) -> Dict[str, Dict[str, float]]:
        """재무제표 데이터에서 필요한 항목을 추출합니다."""
        financial_data = {
            "BS": {},  # 재무상태표
            "IS": {}   # 손익계산서
        }
        
        for statement in statements:
            sj_div = statement["sj_div"]
            account_nm = statement["account_nm"]
            
            # 당기, 전기, 전전기 데이터 추출
            financial_data[sj_div][account_nm] = {
                "current": float(statement["thstrm_amount"]),
                "previous": float(statement["frmtrm_amount"]),
                "prev_previous": float(statement["bfefrmtrm_amount"])
            }
        
        return financial_data

    def _calculate_ratios(self, data: Dict[str, Dict[str, float]]) -> Dict[str, Optional[float]]:
        """재무비율을 계산합니다."""
        try:
            # 필요한 계정과목 금액 추출
            total_assets = data.get('자산총계', {}).get('thstrm', 0)
            total_liabilities = data.get('부채총계', {}).get('thstrm', 0)
            current_assets = data.get('유동자산', {}).get('thstrm', 0)
            current_liabilities = data.get('유동부채', {}).get('thstrm', 0)
            total_equity = data.get('자본총계', {}).get('thstrm', 0)
            revenue = data.get('매출액', {}).get('thstrm', 0)
            operating_profit = data.get('영업이익', {}).get('thstrm', 0)
            net_income = data.get('당기순이익', {}).get('thstrm', 0)
            
            # 전기 데이터
            prev_revenue = data.get('매출액', {}).get('frmtrm', 0)
            prev_operating_profit = data.get('영업이익', {}).get('frmtrm', 0)
            prev_net_income = data.get('당기순이익', {}).get('frmtrm', 0)
            
            # 재무비율 계산
            ratios = {
                # 안정성 비율
                "debt_ratio": self._safe_divide(total_liabilities, total_equity) * 100 if total_equity != 0 else None,
                "current_ratio": self._safe_divide(current_assets, current_liabilities) * 100 if current_liabilities != 0 else None,
                "debt_dependency": self._safe_divide(total_liabilities, total_assets) * 100 if total_assets != 0 else None,
                
                # 수익성 비율
                "operating_profit_ratio": self._safe_divide(operating_profit, revenue) * 100 if revenue != 0 else None,
                "net_profit_ratio": self._safe_divide(net_income, revenue) * 100 if revenue != 0 else None,
                "roe": self._safe_divide(net_income, total_equity) * 100 if total_equity != 0 else None,
                "roa": self._safe_divide(net_income, total_assets) * 100 if total_assets != 0 else None,
                
                # 성장성 비율
                "sales_growth": self._calculate_growth_rate(revenue, prev_revenue),
                "operating_profit_growth": self._calculate_growth_rate(operating_profit, prev_operating_profit),
                "eps_growth": self._calculate_growth_rate(net_income, prev_net_income)
            }
            
            return ratios
            
        except Exception as e:
            logger.error(f"재무비율 계산 중 오류 발생: {str(e)}")
            raise

    def _safe_divide(self, numerator: float, denominator: float) -> Optional[float]:
        """안전한 나눗셈을 수행합니다."""
        try:
            if denominator == 0:
                return None
            return numerator / denominator
        except:
            return None

    async def calculate_and_save_ratios(self, corp_code: str, corp_name: str, bsns_year: str) -> Dict[str, Any]:
        """재무비율을 계산하고 저장합니다."""
        try:
            # 재무제표 데이터 조회
            query = text("""
                SELECT f.account_nm, f.thstrm_amount, f.frmtrm_amount
                FROM financials f
                WHERE f.corp_code = :corp_code
                AND f.bsns_year = :bsns_year
                AND f.sj_div IN ('BS', 'IS')  -- 재무상태표와 손익계산서만 조회
            """)
            result = await self.db_session.execute(query, {
                "corp_code": corp_code,
                "bsns_year": bsns_year
            })
            
            # 계정과목별 금액을 딕셔너리로 변환
            financial_data = {}
            for row in result:
                financial_data[row[0]] = {
                    'thstrm': float(row[1]) if row[1] is not None else 0,
                    'frmtrm': float(row[2]) if row[2] is not None else 0
                }

            # 재무비율 계산
            ratios = self._calculate_ratios(financial_data)
            
            # 재무비율 저장
            insert_query = text("""
                INSERT INTO metrics (
                    corp_code, bsns_year,
                    debt_ratio, current_ratio,
                    operating_profit_ratio, net_profit_ratio,
                    roe, roa, debt_dependency,
                    sales_growth, operating_profit_growth, eps_growth
                ) VALUES (
                    :corp_code, :bsns_year,
                    :debt_ratio, :current_ratio,
                    :operating_profit_ratio, :net_profit_ratio,
                    :roe, :roa, :debt_dependency,
                    :sales_growth, :operating_profit_growth, :eps_growth
                )
            """)
            
            await self.db_session.execute(insert_query, {
                "corp_code": corp_code,
                "bsns_year": bsns_year,
                "debt_ratio": ratios.get("debt_ratio"),
                "current_ratio": ratios.get("current_ratio"),
                "operating_profit_ratio": ratios.get("operating_profit_ratio"),
                "net_profit_ratio": ratios.get("net_profit_ratio"),
                "roe": ratios.get("roe"),
                "roa": ratios.get("roa"),
                "debt_dependency": ratios.get("debt_dependency"),
                "sales_growth": ratios.get("sales_growth"),
                "operating_profit_growth": ratios.get("operating_profit_growth"),
                "eps_growth": ratios.get("eps_growth")
            })
            
            await self.db_session.commit()
            
            return ratios
            
        except Exception as e:
            logger.error(f"재무비율 계산 및 저장 실패: {str(e)}")
            await self.db_session.rollback()
            raise 