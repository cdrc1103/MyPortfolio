from pydantic import BaseModel
from typing import Any


class AssetProfile(BaseModel):
    """Pydantic model for keys returned by 'asset_profile' endpoint of yahooquery API"""

    address1: str
    city: str
    state: str
    zip: str
    country: str
    phone: str
    website: str
    industry: str
    sector: str
    longBusinessSummary: str
    fullTimeEmployees: str
    companyOfficers: Any
    auditRisk: str
    boardRisk: str
    compensationRisk: str
    shareHolderRightsRisk: str
    overallRisk: str
    governanceEpochDate: str
    compensationAsOfEpochDate: str
    maxAge: str


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
