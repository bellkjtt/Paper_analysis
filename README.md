# Paper Analysis System

AI-powered academic paper analysis system using Google Gemini Flash 2.5 for comprehensive paper understanding with easy-to-understand explanations.

## Features

- **Multi-turn Conversation Analysis**: Sequential page delivery to Gemini for comprehensive understanding
- **High-Quality PDF Processing**: 300 DPI page rendering with text extraction
- **Easy Explanations**: High school level explanations with metaphors and analogies
- **Structured Output**: Template-based Korean analysis format
- **Full-Stack Solution**: FastAPI backend + Next.js frontend
- **Cloud Deployment Ready**: Pre-configured for Render, Railway, and other platforms

## Project Structure

```
.
├── paper_analysis_api/          # FastAPI backend service
│   ├── main.py                  # API entry point
│   ├── config.py                # Configuration with environment variables
│   ├── models/                  # Domain models and schemas
│   ├── services/                # Business logic (PDF, Gemini)
│   └── api/                     # API endpoints
├── paper-analysis-next/         # Next.js frontend (if applicable)
├── template.md                  # Analysis template format
├── .env.example                 # Environment variable template
├── requirements.txt             # Python dependencies
└── LICENSE                      # Apache 2.0 License
```

## Quick Start

### Prerequisites

- Python 3.11+
- Google Gemini API key ([Get one here](https://ai.google.dev/))

### Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd <repository-name>
```

2. Create and configure environment variables:
```bash
cp .env.example .env
# Edit .env and add your GEMINI_API_KEY
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run the API server:
```bash
uvicorn paper_analysis_api.main:app --reload --port 8000
```

5. Access the API:
- API: http://localhost:8000
- Interactive Docs: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Usage

### API Endpoint

**POST /api/v1/analyze**

Upload a PDF file for analysis:

```bash
curl -X POST "http://localhost:8000/api/v1/analyze?max_pages=10" \
  -F "file=@paper.pdf"
```

### Python Client Example

```python
import requests

url = "http://localhost:8000/api/v1/analyze"
files = {"file": open("paper.pdf", "rb")}
params = {"max_pages": 10}

response = requests.post(url, files=files, params=params)
result = response.json()

print(result["markdown_content"])
```

### Response Format

```json
{
  "markdown_content": "# 논문 분석 결과...",
  "pdf_filename": "paper.pdf",
  "total_pages": 10,
  "analysis_timestamp": "2025-01-15 10:30:00",
  "model_used": "gemini-2.5-flash",
  "output_path": "/path/to/analysis.md"
}
```

## Configuration

Create a `.env` file in the project root:

```env
# Required
GEMINI_API_KEY=your_gemini_api_key_here

# Optional
GEMINI_MODEL_NAME=gemini-2.5-flash
GEMINI_FALLBACK_MODEL=gemini-1.5-flash
```

See `.env.example` for all available options.

## Deployment

### Render

The project includes `render.yaml` for easy deployment:

1. Push to GitHub
2. Connect repository to Render
3. Add `GEMINI_API_KEY` environment variable
4. Deploy

### Railway

Use the included `railway.toml`:

1. Install Railway CLI
2. Run `railway up`
3. Add environment variables via Railway dashboard

## Architecture

### Backend (FastAPI)

- **Clean Architecture**: Separation of concerns with services, models, and API layers
- **Type Safety**: Full type hints and Pydantic validation
- **Immutability**: Frozen dataclasses for domain models
- **Environment-based Configuration**: Secure API key management
- **Error Handling**: Comprehensive error handling with retries

### Analysis Workflow

1. **PDF Upload**: Client uploads PDF file
2. **Page Extraction**: Extract pages as high-resolution images (300 DPI)
3. **Text Extraction**: Extract text content from each page
4. **Multi-turn Analysis**: Send pages sequentially to Gemini
5. **Template-based Output**: Generate structured Korean analysis
6. **Result Delivery**: Return markdown analysis to client

## Development

### Code Principles

- **Single Responsibility**: Each module has one clear purpose
- **No Magic Values**: All constants in `config.py`
- **DRY**: No code duplication
- **Pure Functions**: Functional programming for transformations
- **Security First**: Environment variables for secrets

### Running Tests

```bash
pytest
```

### Code Style

```bash
# Format code
black .

# Type checking
mypy paper_analysis_api/

# Linting
flake8 paper_analysis_api/
```

## Environment Variables

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `GEMINI_API_KEY` | Yes | - | Google Gemini API key |
| `GEMINI_MODEL_NAME` | No | `gemini-2.5-flash` | Primary model to use |
| `GEMINI_FALLBACK_MODEL` | No | `gemini-1.5-flash` | Fallback model |

## Analysis Template

The system uses a structured Korean template (`template.md`) that includes:

- **Read Section**: Title, abstract, figures with easy explanations
- **QnA Section**: 4 key questions about the paper
- **Limitations**: 3 key limitations of the research

See `template.md` for the full format.

## Security

- **No Hardcoded Secrets**: All API keys via environment variables
- **Input Validation**: Pydantic schema validation
- **File Size Limits**: Configurable upload limits
- **Error Messages**: No sensitive information in error responses

## Performance

- **High-Resolution Processing**: 300 DPI for accurate text and image extraction
- **Rate Limiting**: 2-second delay between Gemini API calls
- **Retry Logic**: Automatic retry on network errors with exponential backoff
- **Efficient Extraction**: Text truncation to 3000 characters per page

## Troubleshooting

### API Key Issues

```
ValueError: GEMINI_API_KEY environment variable is not set
```

**Solution**: Create `.env` file with your API key or set environment variable

### Network Errors

The system automatically retries on SSL and network errors (3 attempts with exponential backoff).

### PDF Processing Issues

Ensure PDF is not encrypted and is a valid PDF file.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## License

This project is licensed under the Apache License 2.0 - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- **Google Gemini**: For powerful AI analysis capabilities
- **FastAPI**: For modern, fast web framework
- **PyMuPDF**: For robust PDF processing

## Support

For issues and questions:
- Open an issue on GitHub
- Check existing documentation
- Review the API docs at `/docs` endpoint

---

**Note**: This project requires a valid Google Gemini API key. Get one at [Google AI Studio](https://ai.google.dev/).
