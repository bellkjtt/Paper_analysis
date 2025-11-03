"""
Gemini analysis service
Handles multi-turn conversation with Gemini for paper analysis
Single Responsibility: Gemini API interaction only
"""

import time
from pathlib import Path
from typing import List, Callable, Any
import google.generativeai as genai
import ssl

from ..models.domain import PageData, AnalysisResult
from ..config import (
    GEMINI_API_KEY,
    GEMINI_MODEL_NAME,
    GEMINI_FALLBACK_MODEL,
    GEMINI_RATE_LIMIT_DELAY,
    TEMPLATE_PATH,
    TEMPLATE_INSTRUCTIONS,
    FINAL_ANALYSIS_REQUEST,
    TEXT_TRUNCATE_LENGTH
)


class GeminiAnalysisService:
    """
    Service for analyzing papers using Gemini multi-turn conversation
    Immutable configuration, handles API communication
    """

    def __init__(self):
        """Initialize Gemini analysis service with API configuration"""
        genai.configure(api_key=GEMINI_API_KEY)
        self._model_name = self._determine_model_to_use()

    def _determine_model_to_use(self) -> str:
        """
        Determine which Gemini model to use
        Uses stable Flash 2.5 model, avoids preview and exp versions
        """
        try:
            available_models = genai.list_models()
            flash_models = [
                m for m in available_models
                if 'flash' in m.name.lower()
            ]

            # Find Flash 2.5 stable (exclude preview and exp)
            flash_25_stable = [
                m for m in flash_models
                if ('2.5' in m.name or '2-5' in m.name)
                and 'preview' not in m.name.lower()
                and 'exp' not in m.name.lower()
            ]

            if flash_25_stable:
                return flash_25_stable[0].name.split('/')[-1]

            # Use configured stable model
            return GEMINI_MODEL_NAME

        except Exception:
            return GEMINI_FALLBACK_MODEL

    def analyze_paper(
        self,
        pages_data: List[PageData],
        pdf_filename: str
    ) -> AnalysisResult:
        """
        Analyze paper using multi-turn Gemini conversation

        Args:
            pages_data: List of extracted page data
            pdf_filename: Name of the PDF file being analyzed

        Returns:
            AnalysisResult containing the generated analysis

        Raises:
            RuntimeError: If Gemini API fails
        """
        template_content = self._load_template()
        chat = self._initialize_chat()

        self._send_initial_instructions(chat, template_content)
        self._send_pages_sequentially(chat, pages_data)
        analysis_text = self._request_final_analysis(chat, len(pages_data))

        return self._create_analysis_result(
            analysis_text,
            pdf_filename,
            len(pages_data)
        )

    def _retry_on_error(self, func: Callable, *args, max_retries: int = 3, **kwargs) -> Any:
        """
        Retry function on SSL and network errors

        Args:
            func: Function to retry
            max_retries: Maximum number of retry attempts
            *args, **kwargs: Arguments to pass to the function

        Returns:
            Result from successful function call

        Raises:
            Last exception if all retries fail
        """
        last_error = None
        for attempt in range(max_retries):
            try:
                return func(*args, **kwargs)
            except (ssl.SSLError, ConnectionError, TimeoutError, OSError) as e:
                last_error = e
                if attempt < max_retries - 1:
                    wait_time = (attempt + 1) * 2  # Exponential backoff: 2s, 4s, 6s
                    print(f"Network error (attempt {attempt + 1}/{max_retries}): {e}. Retrying in {wait_time}s...")
                    time.sleep(wait_time)
                else:
                    raise RuntimeError(f"Failed after {max_retries} retries: {e}") from last_error
            except Exception as e:
                # For non-network errors, fail immediately
                raise RuntimeError(f"Analysis failed: {e}") from e

        raise RuntimeError(f"Failed after {max_retries} retries: {last_error}") from last_error

    def _load_template(self) -> str:
        """Load template content from file"""
        try:
            with open(TEMPLATE_PATH, "r", encoding="utf-8") as f:
                return f.read()
        except FileNotFoundError:
            return ""

    def _initialize_chat(self) -> genai.ChatSession:
        """Initialize Gemini chat session"""
        model = genai.GenerativeModel(self._model_name)
        return model.start_chat(history=[])

    def _send_initial_instructions(
        self,
        chat: genai.ChatSession,
        template_content: str
    ) -> None:
        """Send initial instructions and template to Gemini with retry logic"""
        template_preview = template_content[:2000] if template_content else "..."

        initial_prompt = TEMPLATE_INSTRUCTIONS.format(
            template_content=template_preview
        )

        def send_message():
            chat.send_message(initial_prompt)
            time.sleep(GEMINI_RATE_LIMIT_DELAY)

        self._retry_on_error(send_message)

    def _send_pages_sequentially(
        self,
        chat: genai.ChatSession,
        pages_data: List[PageData]
    ) -> None:
        """Send each page with image and text to Gemini"""
        for page_data in pages_data:
            self._send_single_page(chat, page_data)

    def _send_single_page(
        self,
        chat: genai.ChatSession,
        page_data: PageData
    ) -> None:
        """Send a single page to Gemini with text and image with retry logic"""
        truncated_text = self._truncate_text(page_data.text_content)

        page_message = self._construct_page_message(
            page_data.page_number,
            truncated_text,
            page_data.image_path,
            len(page_data.figure_paths)
        )

        def send_page():
            chat.send_message(page_message)
            time.sleep(GEMINI_RATE_LIMIT_DELAY)

        try:
            self._retry_on_error(send_page)
        except RuntimeError as e:
            raise RuntimeError(
                f"Failed to send page {page_data.page_number}: {e}"
            ) from e

    def _truncate_text(self, text: str) -> str:
        """Truncate text to reasonable length for API"""
        return text[:TEXT_TRUNCATE_LENGTH]

    def _construct_page_message(
        self,
        page_number: int,
        text_content: str,
        image_path: Path,
        figure_count: int
    ) -> List:
        """
        Construct message parts for a single page

        Returns:
            List of message parts (text and image)
        """
        uploaded_file = genai.upload_file(str(image_path))

        figure_info = f"\n**이 페이지의 Figure 개수: {figure_count}개**\n" if figure_count > 0 else ""

        return [
            f"\n### Page {page_number}\n\n",
            f"**텍스트 내용:**\n{text_content}\n\n",
            "**페이지 이미지:**\n",
            uploaded_file,
            f"\n[Page {page_number} 이미지 - 이 페이지의 모든 Figure, 그래프, 수식을 확인하세요]{figure_info}\n"
        ]

    def _request_final_analysis(
        self,
        chat: genai.ChatSession,
        total_pages: int
    ) -> str:
        """Request final comprehensive analysis from Gemini with retry logic"""
        final_prompt = FINAL_ANALYSIS_REQUEST.format(
            total_pages=total_pages
        )

        def request_analysis():
            response = chat.send_message(final_prompt)
            return response.text

        try:
            return self._retry_on_error(request_analysis)
        except RuntimeError as e:
            raise RuntimeError(f"Failed to get final analysis: {e}") from e

    def _create_analysis_result(
        self,
        markdown_content: str,
        pdf_filename: str,
        total_pages: int
    ) -> AnalysisResult:
        """Create AnalysisResult object from analysis output"""
        timestamp = time.strftime('%Y-%m-%d %H:%M:%S')

        return AnalysisResult(
            markdown_content=markdown_content,
            pdf_filename=pdf_filename,
            total_pages=total_pages,
            analysis_timestamp=timestamp,
            model_used=self._model_name
        )
