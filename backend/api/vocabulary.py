"""
Vocabulary API endpoints
Handles vocabulary explanations and translations
"""
import logging
from typing import Dict, Any

from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import JSONResponse

from models.api_models import VocabularyRequest, VocabularyResponse, ErrorResponse
from agents.vocabulary_agent import VocabularyAgent
from utils.error_handler import ErrorHandler, HTTPExceptionHandler

logger = logging.getLogger("vocabulary_api")
router = APIRouter()

# Initialize vocabulary agent
vocabulary_agent = VocabularyAgent()
error_handler = ErrorHandler("vocabulary_api")


async def get_vocabulary_agent() -> VocabularyAgent:
    """Dependency to get vocabulary agent instance"""
    return vocabulary_agent


@router.post("/", response_model=VocabularyResponse)
async def explain_vocabulary(
    request: VocabularyRequest,
    agent: VocabularyAgent = Depends(get_vocabulary_agent)
) -> VocabularyResponse:
    """
    Explain vocabulary using bilingual translation models
    
    - **query**: Word or sentence to explain
    - **source_language**: Source language code (default: es)
    - **target_language**: Target language code (default: en)
    
    Returns vocabulary explanation with translations and examples.
    """
    try:
        logger.info(f"Vocabulary request: {request.query}")
        
        # Validate request
        if not request.query.strip():
            raise HTTPException(
                status_code=422,
                detail="Query cannot be empty"
            )
        
        # Process vocabulary explanation
        response = await agent.explain_vocabulary(request)
        
        logger.info(f"Vocabulary response generated for: {request.query}")
        return response
        
    except ValueError as e:
        logger.warning(f"Validation error: {e}")
        raise HTTPExceptionHandler.validation_exception(str(e))
        
    except Exception as e:
        logger.error(f"Vocabulary explanation error: {e}")
        error_response = error_handler.handle_model_error(e, "VocabularyAgent")
        raise HTTPExceptionHandler.create_http_exception(500, error_response)


@router.get("/health")
async def vocabulary_health_check(
    agent: VocabularyAgent = Depends(get_vocabulary_agent)
) -> Dict[str, Any]:
    """
    Health check for vocabulary service
    
    Returns status of vocabulary agent and available models.
    """
    try:
        health_status = agent.health_check()
        return health_status
        
    except Exception as e:
        logger.error(f"Vocabulary health check error: {e}")
        return {"status": "error", "message": str(e)}


@router.get("/languages")
async def get_supported_languages(
    agent: VocabularyAgent = Depends(get_vocabulary_agent)
) -> Dict[str, Any]:
    """
    Get supported languages for vocabulary explanations
    
    Returns list of supported language codes.
    """
    try:
        languages = agent.get_supported_languages()
        return {
            "supported_languages": languages,
            "language_codes": {
                "es": "Spanish",
                "en": "English"
            }
        }
        
    except Exception as e:
        logger.error(f"Error getting supported languages: {e}")
        return {"supported_languages": [], "error": str(e)}