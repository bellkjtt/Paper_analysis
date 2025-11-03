"""
PDF extraction service
Handles PDF page rendering and text extraction
Single Responsibility: PDF processing only
"""

import os
from pathlib import Path
from typing import List
import fitz  # PyMuPDF

from ..models.domain import PageData
from ..config import PDF_DPI_SCALE, MAX_PAGES_DEFAULT
from .layout_detector_service import LayoutDetectorService


class PDFExtractionService:
    """
    Service for extracting pages and text from PDF files
    Immutable configuration, pure transformation functions
    """

    def __init__(self, output_dir: Path):
        """
        Initialize PDF extraction service

        Args:
            output_dir: Directory where page images will be saved
        """
        self._output_dir = output_dir
        self._ensure_output_directory()
        self._layout_detector = LayoutDetectorService(output_dir)

    def _ensure_output_directory(self) -> None:
        """Create output directory if it doesn't exist"""
        os.makedirs(self._output_dir, exist_ok=True)

    def extract_pages(
        self,
        pdf_path: Path,
        max_pages: int = None
    ) -> List[PageData]:
        """
        Extract all pages from PDF as images and text
        Automatically excludes reference pages
        Pure function with no side effects except file I/O

        Args:
            pdf_path: Path to the PDF file
            max_pages: Optional limit on pages (None = all pages)

        Returns:
            List of PageData objects containing page information

        Raises:
            FileNotFoundError: If PDF file doesn't exist
            ValueError: If PDF cannot be opened or is empty
        """
        if not pdf_path.exists():
            raise FileNotFoundError(f"PDF file not found: {pdf_path}")

        doc = self._open_pdf_document(pdf_path)
        total_pages = len(doc)

        if total_pages == 0:
            doc.close()
            raise ValueError(f"PDF file is empty: {pdf_path}")

        # Extract all pages if max_pages not specified
        pages_to_extract = total_pages if max_pages is None else min(max_pages, total_pages)

        # Detect and exclude reference section
        reference_start = self._detect_reference_section(doc, pages_to_extract)
        if reference_start is not None:
            pages_to_extract = reference_start

        pages_data = self._extract_pages_from_document(doc, pages_to_extract)

        doc.close()
        return pages_data

    def _open_pdf_document(self, pdf_path: Path) -> fitz.Document:
        """Open PDF document with error handling"""
        try:
            return fitz.open(pdf_path)
        except Exception as e:
            raise ValueError(f"Failed to open PDF: {e}")

    def _extract_pages_from_document(
        self,
        doc: fitz.Document,
        pages_to_extract: int
    ) -> List[PageData]:
        """Extract multiple pages from PDF document"""
        pages_data = []

        for page_num in range(pages_to_extract):
            page_data = self._extract_single_page(doc, page_num)
            pages_data.append(page_data)

        return pages_data

    def _extract_single_page(
        self,
        doc: fitz.Document,
        page_index: int
    ) -> PageData:
        """
        Extract a single page from PDF

        Args:
            doc: Open PDF document
            page_index: Zero-based page index

        Returns:
            PageData object with page information
        """
        page = doc[page_index]
        page_number = page_index + 1

        text_content = self._extract_text_from_page(page)
        image_path = self._render_page_to_image(page, page_number)
        image_filename = image_path.name
        figure_paths = self._extract_figures_from_page(doc, page, page_number)

        return PageData(
            page_number=page_number,
            text_content=text_content,
            image_path=image_path,
            image_filename=image_filename,
            figure_paths=tuple(figure_paths)
        )

    def _extract_text_from_page(self, page: fitz.Page) -> str:
        """Extract text content from page"""
        return page.get_text()

    def _render_page_to_image(
        self,
        page: fitz.Page,
        page_number: int
    ) -> Path:
        """
        Render page to high-resolution image

        Args:
            page: PDF page object
            page_number: One-based page number for filename

        Returns:
            Path to saved image file
        """
        transformation_matrix = fitz.Matrix(PDF_DPI_SCALE, PDF_DPI_SCALE)
        pixmap = page.get_pixmap(matrix=transformation_matrix)

        image_filename = f"page_{page_number}.png"
        image_path = self._output_dir / image_filename

        pixmap.save(str(image_path))

        return image_path

    def _extract_figures_from_page(
        self,
        doc: fitz.Document,
        page: fitz.Page,
        page_number: int
    ) -> List[Path]:
        """
        Extract figure images from PDF page using layout detection
        Falls back to PyMuPDF if detectron2 not available

        Args:
            doc: PDF document
            page: PDF page object
            page_number: One-based page number

        Returns:
            List of paths to extracted figure images
        """
        return self._layout_detector.extract_figures_from_page(doc, page, page_number)

    def _detect_reference_section(
        self,
        doc: fitz.Document,
        max_pages: int
    ) -> int:
        """
        Detect where reference section starts
        Returns page index (0-based) or None if not found

        Args:
            doc: PDF document
            max_pages: Maximum pages to check

        Returns:
            Page index where references start, or None
        """
        reference_keywords = [
            'references',
            'bibliography',
            'works cited',
            'citations',
            '참고문헌',
            '참고 문헌'
        ]

        for page_num in range(max_pages):
            page = doc[page_num]
            text = page.get_text().lower()

            # Check first 500 characters for reference heading
            text_start = text[:500]

            for keyword in reference_keywords:
                # Look for keyword as a heading (standalone on line)
                if f'\n{keyword}\n' in text_start or text_start.startswith(keyword):
                    return page_num

        return None
