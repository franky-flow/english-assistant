"""
Correction API endpoints
Handles writing correction and grammar checking
"""
import logging
from typing import Dict, Any

from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import JSONResponse

from models.api_models import CorrectionRequest, CorrectionResponse, ErrorResponse
from agents.correction_agent import CorrectionAgent
from utils.error_handler import ErrorHandler, HTTPExceptionHandler

logger = logging.getLogger("correction_api")
router = APIRouter()

# Initialize correction agent
correction_agent = CorrectionAgent()
error_handler = ErrorHandler("correction_api")


async def get_correction_agent() -> CorrectionAgent:
    """Dependency to get correction agent instance"""
    return correction_agent


@router.post("/", response_model=CorrectionResponse)
async def correct_text(
    request: CorrectionRequest,
    agent: CorrectionAgent = Depends(get_correction_agent)
) -> CorrectionResponse:
    """
    Correct English text with grammar and style improvements
    
    - **text**: Text to correct (1-5000 characters)
    - **correction_level**: Level of correction (basic/comprehensive)
    
    Returns corrected text with detailed explanations and grammar rules.
    """
    try:
        logger.info(f"Correction request: {len(request.text)} characters")
        
        # Validate request
        if not request.text.strip():
            raise HTTPException(
                status_code=422,
                detail="Text cannot be empty"
            )
        
        if len(request.text) > 5000:
            raise HTTPException(
                status_code=422,
                detail="Text too long (maximum 5000 characters)"
            )
        
        # Process text correction
        response = await agent.correct_text(request)
        
        logger.info(f"Correction response generated with {response.correction_count} corrections")
        return response
        
    except ValueError as e:
        logger.warning(f"Validation error: {e}")
        raise HTTPExceptionHandler.validation_exception(str(e))
        
    except Exception as e:
        logger.error(f"Text correction error: {e}")
        error_response = error_handler.handle_model_error(e, "CorrectionAgent")
        raise HTTPExceptionHandler.create_http_exception(500, error_response)


@router.get("/health")
async def correction_health_check(
    agent: CorrectionAgent = Depends(get_correction_agent)
) -> Dict[str, Any]:
    """
    Health check for correction service
    
    Returns status of correction agent and available correction methods.
    """
    try:
        health_status = agent.health_check()
        return health_status
        
    except Exception as e:
        logger.error(f"Correction health check error: {e}")
        return {"status": "error", "message": str(e)}


@router.get("/correction-levels")
async def get_correction_levels() -> Dict[str, Any]:
    """
    Get available correction levels
    
    Returns information about different correction levels and their features.
    """
    return {
        "correction_levels": {
            "basic": {
                "description": "Basic grammar and spelling corrections",
                "features": ["spelling", "basic_grammar", "punctuation"]
            },
            "comprehensive": {
                "description": "Comprehensive grammar, style, and clarity improvements",
                "features": ["spelling", "grammar", "style", "clarity", "word_choice"]
            }
        },
        "default": "comprehensive"
    }