"""
Models package for Paper Analysis API
"""

from .domain import PageData, AnalysisResult
from .schemas import AnalysisRequest, AnalysisResponse

__all__ = ["PageData", "AnalysisResult", "AnalysisRequest", "AnalysisResponse"]
