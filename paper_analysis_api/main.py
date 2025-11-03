"""
Paper Analysis API - Main Application
FastAPI application for analyzing academic papers with Gemini
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .api import router

app = FastAPI(
    title="Paper Analysis API",
    description="Analyze academic papers with Gemini Flash 2.5 using multi-turn conversation",
    version="1.0.0"
)

# CORS configuration for web access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes
app.include_router(router)


@app.get("/")
async def root():
    """
    Root endpoint with API information
    """
    return {
        "service": "Paper Analysis API",
        "version": "1.0.0",
        "status": "running",
        "endpoints": {
            "analyze": "/api/v1/analyze",
            "docs": "/docs"
        }
    }


@app.get("/health")
async def health_check():
    """
    Health check endpoint
    """
    return {
        "status": "healthy",
        "service": "paper-analysis-api"
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
