# Paper Analysis API

FastAPI-based service for analyzing academic papers using Gemini Flash 2.5 with multi-turn conversation.

## Architecture

Modular FastAPI application following clean code principles:

```
paper_analysis_api/
├── main.py                 # FastAPI application entry point
├── config.py               # Configuration constants
├── models/
│   ├── domain.py          # Domain entities (PageData, AnalysisResult)
│   └── schemas.py         # Pydantic request/response models
├── services/
│   ├── pdf_service.py     # PDF extraction service
│   └── gemini_service.py  # Gemini analysis service
└── api/
    └── endpoints.py       # API route handlers
```

## Features

- **PDF Page Extraction**: High-resolution page rendering (300 DPI)
- **Text Extraction**: Full text content from PDF pages
- **Multi-turn Analysis**: Sequential page delivery to Gemini
- **Easy Explanations**: High school level with metaphors and analogies
- **Template Format**: Structured Korean analysis output

## Installation

```bash
cd paper_analysis_api
pip install -r requirements.txt
```

## Usage

### Start Server

```bash
# Development mode with auto-reload
python -m uvicorn paper_analysis_api.main:app --reload --port 8000

# Or using the main.py directly
cd paper_analysis_api
python main.py
```

### API Endpoints

**POST /api/v1/analyze**
- Upload PDF file for analysis
- Optional: `max_pages` query parameter (default: 10, max: 50)
- Returns: Analysis in markdown format

**GET /**
- API information

**GET /health**
- Health check

### Example Request (curl)

```bash
curl -X POST "http://localhost:8000/api/v1/analyze?max_pages=10" \
  -F "file=@paper.pdf"
```

### Example Request (Python)

```python
import requests

url = "http://localhost:8000/api/v1/analyze"
files = {"file": open("paper.pdf", "rb")}
params = {"max_pages": 10}

response = requests.post(url, files=files, params=params)
result = response.json()

print(result["markdown_content"])
```

## API Response Schema

```json
{
  "markdown_content": "# 논문 분석...",
  "pdf_filename": "paper.pdf",
  "total_pages": 10,
  "analysis_timestamp": "2025-01-15 10:30:00",
  "model_used": "gemini-2.5-flash-preview-05-20",
  "output_path": "/path/to/saved/analysis.md"
}
```

## Configuration

Edit `config.py` to customize:

- `GEMINI_API_KEY`: Gemini API key
- `MAX_PAGES_DEFAULT`: Default max pages to analyze
- `PDF_DPI_SCALE`: Image resolution (default: 300 DPI)
- `OUTPUT_BASE_DIR`: Output directory path

## Development Principles

This codebase follows strict clean code principles:

1. **Single Responsibility**: Each module has one clear purpose
2. **Immutability**: Domain models are frozen dataclasses
3. **Type Safety**: Full type hints and validation
4. **No Magic Values**: All constants defined in config
5. **Pure Functions**: Services use pure transformation functions
6. **DRY**: No code duplication

## Interactive Documentation

Once the server is running, visit:

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc
