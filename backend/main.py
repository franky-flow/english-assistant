"""
FastAPI application for English Assistant
Main entry point for the REST API server
"""
import logging
import sys
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.responses import JSONResponse

# Add backend to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from config import settings
from utils import get_model_manager, global_exception_handler
from api.routes import router


# Configure logging
logging.basicConfig(
    level=getattr(logging, settings.log_level),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler(settings.log_file) if settings.log_file else logging.NullHandler()
    ]
)

logger = logging.getLogger("english_assistant")


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager"""
    # Startup
    logger.info("Starting English Assistant API...")
    
    # Initialize model manager
    model_manager = get_model_manager()
    logger.info("Model manager initialized")
    
    # Preload critical models (optional, can be done on-demand)
    # model_manager.preload_models(["nllb-200", "t5-grammar"])
    
    yield
    
    # Shutdown
    logger.info("Shutting down English Assistant API...")
    model_manager.shutdown()


# Create FastAPI application
app = FastAPI(
    title="English Assistant API",
    description="A local API for helping Spanish speakers improve their English skills",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan
)


# Add middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)

app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=["localhost", "127.0.0.1", settings.api_host]
)


# Add global exception handler
app.add_exception_handler(Exception, global_exception_handler)


# Include API routes
app.include_router(router, prefix="/api")


# Health check endpoint
@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "English Assistant API"}


if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(
        "main:app",
        host=settings.api_host,
        port=settings.api_port,
        reload=settings.api_debug,
        log_level=settings.log_level.lower()
    )