"""
Pydantic schemas for API request/response validation
Type-safe data transfer objects for FastAPI
"""

from pydantic import BaseModel, Field, field_validator
from typing import Optional


class AnalysisRequest(BaseModel):
    """
    Request schema for paper analysis
    Validates user input before processing
    """
    max_pages: int = Field(
        default=10,
        ge=1,
        le=50,
        description="Maximum number of pages to analyze (1-50)"
    )

    @field_validator('max_pages')
    @classmethod
    def validate_max_pages(cls, value: int) -> int:
        """Ensure max_pages is within reasonable bounds"""
        if value < 1:
            raise ValueError("max_pages must be at least 1")
        if value > 50:
            raise ValueError("max_pages cannot exceed 50 for performance reasons")
        return value


class AnalysisResponse(BaseModel):
    """
    Response schema for successful paper analysis
    Provides analysis results and metadata to client
    """
    markdown_content: str = Field(
        description="Generated analysis in markdown format"
    )
    pdf_filename: str = Field(
        description="Name of the analyzed PDF file"
    )
    total_pages: int = Field(
        ge=1,
        description="Number of pages analyzed"
    )
    analysis_timestamp: str = Field(
        description="ISO timestamp when analysis was completed"
    )
    model_used: str = Field(
        description="Gemini model used for analysis"
    )
    output_path: Optional[str] = Field(
        default=None,
        description="Path where analysis was saved (if applicable)"
    )


class ErrorResponse(BaseModel):
    """
    Error response schema for failed requests
    Provides clear error information to client
    """
    error: str = Field(
        description="Error message describing what went wrong"
    )
    detail: Optional[str] = Field(
        default=None,
        description="Additional error details for debugging"
    )
