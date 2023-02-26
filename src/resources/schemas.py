from pydantic import BaseModel
from typing import Any


class AssetProfile(BaseModel):
    """Pydantic model for keys returned by 'asset_profile' endpoint of yahooquery API"""

    address1: str | None
    city: str | None
    state: str | None
    zip: str | None
    country: str | None
    phone: str | None
    website: str | None
    industry: str | None
    sector: str | None
    longBusinessSummary: str | None
    fullTimeEmployees: str | None
    companyOfficers: Any
    auditRisk: str | None
    boardRisk: str | None
    compensationRisk: str | None
    shareHolderRightsRisk: str | None
    overallRisk: str | None
    governanceEpochDate: str | None
    compensationAsOfEpochDate: str | None
    maxAge: str | None


class StockInfo(BaseModel):
    """Pydantic model for keys returned by 'all_modules' endpoint of yahooquery API"""

    assetProfile: AssetProfile
    recommendationTrend: Any
    cashflowStatementHistory: Any
    indexTrend: Any
    defaultKeyStatistics: Any
    industryTrend: Any
    quoteType: Any
    incomeStatementHistory: Any
    fundOwnership: Any
    summaryDetail: Any
    insiderHolders: Any
    calendarEvents: Any
    upgradeDowngradeHistory: Any
    price: Any
    balanceSheetHistory: Any
    earningsTrend: Any
    secFilings: Any
    institutionOwnership: Any
    majorHoldersBreakdown: Any
    balanceSheetHistoryQuarterly: Any
    earningsHistory: Any
    esgScores: Any
    summaryProfile: Any
    netSharePurchaseActivity: Any
    insiderTransactions: Any
    sectorTrend: Any
    incomeStatementHistoryQuarterly: Any
    cashflowStatementHistoryQuarterly: Any
    earnings: Any
    pageViews: Any
    financialData: Any


class Stocks(BaseModel):
    stock_info: dict[str, StockInfo]
