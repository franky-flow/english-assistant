"""
API routes for English Assistant
Centralized router for all API endpoints
"""
from fastapi import APIRouter

from .vocabulary import router as vocabulary_router
from .correction import router as correction_router
from .grammar import router as grammar_router
from .phrasal_verbs import router as phrasal_verbs_router
from .history import router as history_router

# Main API router
router = APIRouter()

# Include all endpoint routers
router.include_router(vocabulary_router, prefix="/vocabulary", tags=["vocabulary"])
router.include_router(correction_router, prefix="/correction", tags=["correction"])
router.include_router(grammar_router, prefix="/grammar", tags=["grammar"])
router.include_router(phrasal_verbs_router, prefix="/phrasal-verbs", tags=["phrasal-verbs"])
router.include_router(history_router, prefix="/history", tags=["history"])


@router.get("/")
async def api_root():
    """API root endpoint"""
    return {
        "message": "English Assistant API",
        "version": "1.0.0",
        "endpoints": [
            "/api/vocabulary",
            "/api/correction", 
            "/api/grammar",
            "/api/phrasal-verbs",
            "/api/history"
        ]
    }