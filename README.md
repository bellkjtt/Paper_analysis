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
- Node.js 18+ (for frontend)
- Google Gemini API key ([Get one here](https://ai.google.dev/))

### Backend Setup

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

3. Install Python dependencies:
```bash
pip install -r requirements.txt
```

4. Run the API server:
```bash
uvicorn paper_analysis_api.main:app --reload --port 8000
```

5. Verify API is running:
- API: http://localhost:8000
- Interactive Docs: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

### Frontend Setup

1. Navigate to frontend directory:
```bash
cd paper-analysis-next
```

2. Install dependencies:
```bash
npm install
```

3. Configure environment variables:
```bash
cp .env.local.example .env.local
# Edit .env.local to set NEXT_PUBLIC_API_URL if needed
```

4. Run development server:
```bash
npm run dev
```

5. Access the application:
- Frontend: http://localhost:3000

### Full Stack Development

To run both backend and frontend simultaneously:

**Terminal 1 (Backend):**
```bash
uvicorn paper_analysis_api.main:app --reload --port 8000
```

**Terminal 2 (Frontend):**
```bash
cd paper-analysis-next
npm run dev
```

Then open http://localhost:3000 in your browser.

## Usage

### Web UI (Recommended)

1. Make sure both backend and frontend are running
2. Open http://localhost:3000 in your browser
3. Click "PDF 파일 선택" to upload your academic paper (PDF format)
4. Click "분석 시작" to begin analysis
5. Wait for the analysis to complete (approximately 12 seconds per page)
6. View the analysis results in an easy-to-read format
7. Download results as:
   - **Markdown**: Plain markdown file
   - **PDF**: Formatted PDF document

**Features:**
- Real-time progress tracking
- Beautiful markdown rendering
- Figure and table visualization
- Easy-to-understand explanations with metaphors
- One-click download in multiple formats

### API Endpoint (Advanced)

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

### Backend Configuration

Create a `.env` file in the project root:

```env
# Required
GEMINI_API_KEY=your_gemini_api_key_here

# Optional
GEMINI_MODEL_NAME=gemini-2.5-flash
GEMINI_FALLBACK_MODEL=gemini-1.5-flash
```

See `.env.example` for all available options.

### Frontend Configuration

Create a `.env.local` file in the `paper-analysis-next` directory:

```env
# Backend API URL
NEXT_PUBLIC_API_URL=http://localhost:8000

# For local network access (e.g., mobile testing)
# NEXT_PUBLIC_API_URL=http://192.168.1.100:8000

# For production
# NEXT_PUBLIC_API_URL=https://your-api-domain.com
```

See `paper-analysis-next/.env.local.example` for all options.

## Deployment

### Backend Deployment

#### Render

The project includes `render.yaml` for easy backend deployment:

1. Push to GitHub
2. Connect repository to Render
3. Add `GEMINI_API_KEY` environment variable in Render dashboard
4. Deploy

#### Railway

Use the included `railway.toml`:

1. Install Railway CLI: `npm install -g @railway/cli`
2. Run `railway up`
3. Add `GEMINI_API_KEY` environment variable via Railway dashboard

### Frontend Deployment

#### Vercel (Recommended for Next.js)

1. Push frontend to GitHub
2. Import project to Vercel
3. Set environment variable:
   - `NEXT_PUBLIC_API_URL`: Your deployed backend URL
4. Deploy

```bash
# Or use Vercel CLI
cd paper-analysis-next
npm install -g vercel
vercel --prod
```

#### Build for Production

```bash
cd paper-analysis-next
npm run build
npm start
```

The production server will run on port 3000.

## Architecture

### Backend (FastAPI)

- **Clean Architecture**: Separation of concerns with services, models, and API layers
- **Type Safety**: Full type hints and Pydantic validation
- **Immutability**: Frozen dataclasses for domain models
- **Environment-based Configuration**: Secure API key management
- **Error Handling**: Comprehensive error handling with retries

### Frontend (Next.js 15)

- **Modern Stack**: Next.js 15, React 18, TypeScript, Tailwind CSS
- **Client-Side Rendering**: Interactive UI with real-time progress updates
- **Responsive Design**: Mobile-friendly interface
- **Markdown Rendering**: Beautiful rendering with react-markdown
- **Export Features**: Download as Markdown or PDF (jspdf + html2canvas)
- **Type Safety**: Full TypeScript coverage
- **State Management**: React hooks for local state management

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

**Backend:**
```bash
pytest
```

**Frontend:**
```bash
cd paper-analysis-next
npm run lint
npm run build  # Test production build
```

### Code Style

**Backend:**
```bash
# Format code
black .

# Type checking
mypy paper_analysis_api/

# Linting
flake8 paper_analysis_api/
```

**Frontend:**
```bash
cd paper-analysis-next

# Linting
npm run lint

# Type checking (TypeScript)
npx tsc --noEmit
```

## Environment Variables

### Backend Environment Variables

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `GEMINI_API_KEY` | Yes | - | Google Gemini API key |
| `GEMINI_MODEL_NAME` | No | `gemini-2.5-flash` | Primary model to use |
| `GEMINI_FALLBACK_MODEL` | No | `gemini-1.5-flash` | Fallback model |

### Frontend Environment Variables

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `NEXT_PUBLIC_API_URL` | Yes | `http://localhost:8000` | Backend API URL |

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

### Backend Issues

#### API Key Issues

```
ValueError: GEMINI_API_KEY environment variable is not set
```

**Solution**: Create `.env` file with your API key or set environment variable

#### Network Errors

The system automatically retries on SSL and network errors (3 attempts with exponential backoff).

#### PDF Processing Issues

Ensure PDF is not encrypted and is a valid PDF file.

### Frontend Issues

#### Cannot connect to backend

```
Error: Failed to fetch
```

**Solutions**:
1. Ensure backend is running on `http://localhost:8000`
2. Check `NEXT_PUBLIC_API_URL` in `.env.local`
3. Verify CORS settings if using different domains
4. For mobile/network access: Use your computer's local IP address instead of `localhost`

#### Build errors

```
npm run build fails
```

**Solutions**:
1. Delete `node_modules` and `.next` folders
2. Run `npm install` again
3. Check Node.js version (requires 18+)

#### Environment variables not working

**Solutions**:
1. Restart Next.js dev server after changing `.env.local`
2. Ensure variable names start with `NEXT_PUBLIC_` for client-side access
3. Clear `.next` cache: `rm -rf .next`

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
- **Next.js**: For React framework with great developer experience
- **PyMuPDF**: For robust PDF processing
- **Tailwind CSS**: For utility-first styling
- **react-markdown**: For beautiful markdown rendering
- **jsPDF & html2canvas**: For client-side PDF generation

## Support

For issues and questions:
- Open an issue on GitHub
- Check existing documentation
- Review the API docs at `/docs` endpoint

---

**Note**: This project requires a valid Google Gemini API key. Get one at [Google AI Studio](https://ai.google.dev/).
