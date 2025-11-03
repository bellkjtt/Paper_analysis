"""
API endpoints for Paper Analysis
Handles HTTP requests and orchestrates services
"""

import os
from pathlib import Path
from fastapi import APIRouter, UploadFile, File, HTTPException, Query
from fastapi.responses import JSONResponse, FileResponse
from typing import Optional
import uuid

from ..models.schemas import AnalysisRequest, AnalysisResponse, ErrorResponse
from ..services import PDFExtractionService, GeminiAnalysisService
from ..config import OUTPUT_BASE_DIR, MAX_PAGES_DEFAULT
from ..utils.image_processor import insert_figure_images

router = APIRouter(prefix="/api/v1", tags=["analysis"])

ALLOWED_EXTENSIONS = {".pdf"}
MAX_FILE_SIZE_MB = 50
MAX_FILE_SIZE_BYTES = MAX_FILE_SIZE_MB * 1024 * 1024


@router.post(
    "/analyze",
    response_model=AnalysisResponse,
    responses={
        400: {"model": ErrorResponse},
        500: {"model": ErrorResponse}
    }
)
async def analyze_paper(
    file: UploadFile = File(..., description="PDF file to analyze"),
    max_pages: int = Query(
        default=None,
        ge=1,
        le=200,
        description="Optional: Maximum pages to analyze (default: all pages)"
    )
) -> AnalysisResponse:
    """
    Analyze an academic paper PDF

    Extracts pages and text, then analyzes with Gemini in multi-turn fashion
    Returns analysis in template.md format with easy-to-understand explanations
    """
    validate_uploaded_file(file)

    temp_pdf_path = await save_uploaded_file(file)

    try:
        analysis_result, analysis_id = perform_analysis(temp_pdf_path, max_pages)
        return create_success_response(analysis_result, analysis_id)

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Analysis failed: {str(e)}"
        )

    finally:
        cleanup_temp_file(temp_pdf_path)


def validate_uploaded_file(file: UploadFile) -> None:
    """
    Validate uploaded file

    Raises:
        HTTPException: If file is invalid
    """
    if not file.filename:
        raise HTTPException(
            status_code=400,
            detail="No file provided"
        )

    file_extension = Path(file.filename).suffix.lower()
    if file_extension not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid file type. Only {ALLOWED_EXTENSIONS} allowed"
        )


async def save_uploaded_file(file: UploadFile) -> Path:
    """
    Save uploaded file to temporary location

    Returns:
        Path to saved file

    Raises:
        HTTPException: If file is too large or save fails
    """
    os.makedirs(OUTPUT_BASE_DIR, exist_ok=True)

    temp_pdf_path = OUTPUT_BASE_DIR / file.filename

    try:
        file_content = await file.read()

        if len(file_content) > MAX_FILE_SIZE_BYTES:
            raise HTTPException(
                status_code=400,
                detail=f"File too large. Max size: {MAX_FILE_SIZE_MB}MB"
            )

        with open(temp_pdf_path, "wb") as f:
            f.write(file_content)

        return temp_pdf_path

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to save file: {str(e)}"
        )


def perform_analysis(pdf_path: Path, max_pages: int):
    """
    Perform complete paper analysis

    Orchestrates PDF extraction and Gemini analysis services
    """
    # Generate unique ID for this analysis
    analysis_id = str(uuid.uuid4())[:8]
    output_dir = create_output_directory(pdf_path, analysis_id)

    pdf_service = PDFExtractionService(output_dir)
    pages_data = pdf_service.extract_pages(pdf_path, max_pages)

    gemini_service = GeminiAnalysisService()
    analysis_result = gemini_service.analyze_paper(
        pages_data,
        pdf_path.name
    )

    # Insert figure images into markdown
    markdown_with_images = insert_figure_images(
        analysis_result.markdown_content,
        output_dir,
        analysis_id
    )

    # Update analysis result with image-enhanced markdown
    from ..models.domain import AnalysisResult
    enhanced_result = AnalysisResult(
        markdown_content=markdown_with_images,
        pdf_filename=analysis_result.pdf_filename,
        total_pages=analysis_result.total_pages,
        analysis_timestamp=analysis_result.analysis_timestamp,
        model_used=analysis_result.model_used,
        output_path=analysis_result.output_path
    )

    save_analysis_output(enhanced_result, output_dir)

    return enhanced_result, analysis_id


def create_output_directory(pdf_path: Path, analysis_id: str) -> Path:
    """Create unique output directory for this analysis"""
    output_dir = OUTPUT_BASE_DIR / analysis_id
    os.makedirs(output_dir, exist_ok=True)
    return output_dir


def save_analysis_output(analysis_result, output_dir: Path) -> None:
    """Save analysis markdown to file"""
    output_path = output_dir / "ANALYSIS.md"

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(f"# 논문 분석 (Gemini Flash 2.5)\n\n")
        f.write(f"**PDF**: {analysis_result.pdf_filename}\n")
        f.write(f"**분석 페이지**: {analysis_result.total_pages} 페이지\n")
        f.write(f"**생성 시각**: {analysis_result.analysis_timestamp}\n\n")
        f.write("---\n\n")
        f.write(analysis_result.markdown_content)


def create_success_response(analysis_result, analysis_id: str) -> AnalysisResponse:
    """Create successful response from analysis result"""
    return AnalysisResponse(
        markdown_content=analysis_result.markdown_content,
        pdf_filename=analysis_result.pdf_filename,
        total_pages=analysis_result.total_pages,
        analysis_timestamp=analysis_result.analysis_timestamp,
        model_used=analysis_result.model_used,
        output_path=str(analysis_result.output_path) if analysis_result.output_path else None
    )


def cleanup_temp_file(file_path: Path) -> None:
    """Clean up temporary PDF file"""
    try:
        if file_path.exists():
            os.remove(file_path)
    except Exception:
        pass  # Best effort cleanup


@router.get("/images/{analysis_id}/{filename}")
async def serve_image(analysis_id: str, filename: str):
    """
    Serve page images for analysis results

    Args:
        analysis_id: Unique analysis ID
        filename: Image filename (e.g., page_1.png)

    Returns:
        Image file
    """
    image_path = OUTPUT_BASE_DIR / analysis_id / filename

    if not image_path.exists():
        raise HTTPException(
            status_code=404,
            detail=f"Image not found: {filename}"
        )

    # Security: Ensure path is within OUTPUT_BASE_DIR
    try:
        image_path.resolve().relative_to(OUTPUT_BASE_DIR.resolve())
    except ValueError:
        raise HTTPException(
            status_code=403,
            detail="Access denied"
        )

    return FileResponse(
        image_path,
        media_type="image/png",
        headers={"Cache-Control": "public, max-age=3600"}
    )
