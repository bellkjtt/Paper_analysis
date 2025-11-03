"""
Domain models representing core business entities
Immutable data structures for type safety and predictability
"""

from dataclasses import dataclass
from pathlib import Path
from typing import Optional, Tuple


@dataclass(frozen=True)
class PageData:
    """
    Represents a single page extracted from PDF
    Immutable to prevent accidental modifications
    """
    page_number: int
    text_content: str
    image_path: Path
    image_filename: str
    figure_paths: Tuple[Path, ...] = ()  # Paths to extracted figure images

    def __post_init__(self):
        """Validate page data on creation"""
        if self.page_number < 1:
            raise ValueError(f"Page number must be positive, got {self.page_number}")
        if not self.image_path.exists():
            raise FileNotFoundError(f"Image file not found: {self.image_path}")


@dataclass(frozen=True)
class AnalysisResult:
    """
    Represents the result of paper analysis
    Contains the generated markdown content and metadata
    """
    markdown_content: str
    pdf_filename: str
    total_pages: int
    analysis_timestamp: str
    model_used: str
    output_path: Optional[Path] = None

    def __post_init__(self):
        """Validate analysis result on creation"""
        if not self.markdown_content:
            raise ValueError("Markdown content cannot be empty")
        if self.total_pages < 1:
            raise ValueError(f"Total pages must be positive, got {self.total_pages}")
