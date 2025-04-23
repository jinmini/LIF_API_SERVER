from enum import Enum

class BaseAction(Enum):
    """기본 액션 Enum 클래스"""
    GET = "get"
    GET_ALL = "get_all"
    CREATE = "create"
    UPDATE = "update"
    DELETE = "delete"

class CompanyAction(BaseAction):
    """기업 관련 액션"""
    pass

class StatementAction(BaseAction):
    """재무제표 구분 관련 액션"""
    pass

class ReportAction(BaseAction):
    """공시보고서 관련 액션"""
    pass

class FinancialAction(BaseAction):
    """재무제표 계정 관련 액션"""
    pass

class MetricAction(BaseAction):
    """재무지표 관련 액션"""
    pass 