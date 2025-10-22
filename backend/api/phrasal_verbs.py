"""
Phrasal Verbs API endpoints
Handles phrasal verb management and progress tracking
"""
import logging
from typing import Dict, Any, List

from fastapi import APIRouter, HTTPException, Depends, Query
from fastapi.responses import JSONResponse

from models.api_models import (
    PhrasalVerb, PhrasalVerbFilters, PhrasalVerbUpdateRequest, 
    SuccessResponse, ErrorResponse
)
from agents.phrasal_verb_agent import PhrasalVerbAgent
from utils.error_handler import ErrorHandler, HTTPExceptionHandler
from utils.response_formatter import ResponseFormatter

logger = logging.getLogger("phrasal_verbs_api")
router = APIRouter()

# Initialize phrasal verb agent
phrasal_verb_agent = PhrasalVerbAgent()
error_handler = ErrorHandler("phrasal_verbs_api")


async def get_phrasal_verb_agent() -> PhrasalVerbAgent:
    """Dependency to get phrasal verb agent instance"""
    return phrasal_verb_agent


@router.get("/", response_model=List[PhrasalVerb])
async def get_phrasal_verbs(
    difficulty: str = Query(None, description="Filter by difficulty (beginner/intermediate/advanced)"),
    status: str = Query(None, description="Filter by status (pending/in_progress/learned)"),
    search: str = Query(None, description="Search term for verb or definition"),
    limit: int = Query(50, ge=1, le=200, description="Maximum results to return"),
    offset: int = Query(0, ge=0, description="Results offset for pagination"),
    agent: PhrasalVerbAgent = Depends(get_phrasal_verb_agent)
) -> List[PhrasalVerb]:
    """
    Get phrasal verbs with filtering and pagination
    
    - **difficulty**: Filter by difficulty level
    - **status**: Filter by learning status
    - **search**: Search in verb name or definition
    - **limit**: Maximum number of results (1-200)
    - **offset**: Number of results to skip
    
    Returns list of phrasal verbs matching the criteria.
    """
    try:
        logger.info(f"Phrasal verbs request: difficulty={difficulty}, status={status}, search={search}")
        
        # Create filters object
        filters = PhrasalVerbFilters(
            difficulty=difficulty,
            status=status,
            search=search,
            limit=limit,
            offset=offset
        )
        
        # Get phrasal verbs
        phrasal_verbs = await agent.get_phrasal_verbs(filters)
        
        logger.info(f"Returning {len(phrasal_verbs)} phrasal verbs")
        return phrasal_verbs
        
    except ValueError as e:
        logger.warning(f"Validation error: {e}")
        raise HTTPExceptionHandler.validation_exception(str(e))
        
    except Exception as e:
        logger.error(f"Phrasal verbs retrieval error: {e}")
        error_response = error_handler.handle_model_error(e, "PhrasalVerbAgent")
        raise HTTPExceptionHandler.create_http_exception(500, error_response)


@router.get("/{verb_id}", response_model=PhrasalVerb)
async def get_phrasal_verb_by_id(
    verb_id: int,
    agent: PhrasalVerbAgent = Depends(get_phrasal_verb_agent)
) -> PhrasalVerb:
    """
    Get a specific phrasal verb by ID
    
    - **verb_id**: Unique identifier of the phrasal verb
    
    Returns the phrasal verb with progress information.
    """
    try:
        logger.info(f"Getting phrasal verb by ID: {verb_id}")
        
        phrasal_verb = await agent.get_phrasal_verb_by_id(verb_id)
        
        if not phrasal_verb:
            raise HTTPExceptionHandler.not_found_exception("Phrasal verb")
        
        return phrasal_verb
        
    except HTTPException:
        raise
        
    except Exception as e:
        logger.error(f"Error getting phrasal verb by ID: {e}")
        error_response = error_handler.handle_model_error(e, "PhrasalVerbAgent")
        raise HTTPExceptionHandler.create_http_exception(500, error_response)


@router.put("/{verb_id}/progress", response_model=PhrasalVerb)
async def update_phrasal_verb_progress(
    verb_id: int,
    update_request: PhrasalVerbUpdateRequest,
    agent: PhrasalVerbAgent = Depends(get_phrasal_verb_agent)
) -> PhrasalVerb:
    """
    Update progress for a specific phrasal verb
    
    - **verb_id**: Unique identifier of the phrasal verb
    - **status**: New learning status (pending/in_progress/learned)
    - **progress**: Optional progress data (attempts, correct answers, etc.)
    
    Returns the updated phrasal verb with new progress information.
    """
    try:
        logger.info(f"Updating progress for phrasal verb {verb_id}: {update_request.status}")
        
        updated_verb = await agent.update_phrasal_verb_progress(verb_id, update_request)
        
        logger.info(f"Progress updated for phrasal verb {verb_id}")
        return updated_verb
        
    except ValueError as e:
        logger.warning(f"Validation error: {e}")
        raise HTTPExceptionHandler.validation_exception(str(e))
        
    except Exception as e:
        logger.error(f"Progress update error: {e}")
        error_response = error_handler.handle_model_error(e, "PhrasalVerbAgent")
        raise HTTPExceptionHandler.create_http_exception(500, error_response)


@router.get("/stats/progress")
async def get_progress_statistics(
    agent: PhrasalVerbAgent = Depends(get_phrasal_verb_agent)
) -> Dict[str, Any]:
    """
    Get overall progress statistics
    
    Returns comprehensive statistics about phrasal verb learning progress.
    """
    try:
        stats = agent.get_progress_statistics()
        return stats
        
    except Exception as e:
        logger.error(f"Error getting progress statistics: {e}")
        return {"error": str(e)}


@router.get("/recommendations/practice")
async def get_recommended_verbs(
    limit: int = Query(5, ge=1, le=20, description="Number of recommendations"),
    agent: PhrasalVerbAgent = Depends(get_phrasal_verb_agent)
) -> List[PhrasalVerb]:
    """
    Get recommended phrasal verbs for practice
    
    - **limit**: Number of recommendations to return (1-20)
    
    Returns phrasal verbs prioritized for practice based on progress and difficulty.
    """
    try:
        recommendations = agent.get_recommended_verbs(limit)
        logger.info(f"Returning {len(recommendations)} recommended phrasal verbs")
        return recommendations
        
    except Exception as e:
        logger.error(f"Error getting recommendations: {e}")
        error_response = error_handler.handle_model_error(e, "PhrasalVerbAgent")
        raise HTTPExceptionHandler.create_http_exception(500, error_response)


@router.get("/search/{query}")
async def search_phrasal_verbs(
    query: str,
    agent: PhrasalVerbAgent = Depends(get_phrasal_verb_agent)
) -> List[PhrasalVerb]:
    """
    Search phrasal verbs by query
    
    - **query**: Search term to look for in verbs, definitions, or examples
    
    Returns phrasal verbs matching the search query.
    """
    try:
        logger.info(f"Searching phrasal verbs: {query}")
        
        if len(query.strip()) < 2:
            raise HTTPException(
                status_code=422,
                detail="Search query must be at least 2 characters"
            )
        
        results = agent.search_phrasal_verbs(query)
        
        logger.info(f"Search returned {len(results)} results")
        return results
        
    except HTTPException:
        raise
        
    except Exception as e:
        logger.error(f"Search error: {e}")
        error_response = error_handler.handle_model_error(e, "PhrasalVerbAgent")
        raise HTTPExceptionHandler.create_http_exception(500, error_response)


@router.get("/meta/difficulties")
async def get_available_difficulties(
    agent: PhrasalVerbAgent = Depends(get_phrasal_verb_agent)
) -> Dict[str, Any]:
    """
    Get available difficulty levels
    
    Returns list of available difficulty levels for filtering.
    """
    try:
        difficulties = agent.get_available_difficulties()
        return {
            "difficulties": difficulties,
            "descriptions": {
                "beginner": "Basic phrasal verbs for new learners",
                "intermediate": "Common phrasal verbs for developing skills",
                "advanced": "Complex phrasal verbs for advanced learners"
            }
        }
        
    except Exception as e:
        logger.error(f"Error getting difficulties: {e}")
        return {"difficulties": [], "error": str(e)}


@router.get("/meta/statuses")
async def get_available_statuses(
    agent: PhrasalVerbAgent = Depends(get_phrasal_verb_agent)
) -> Dict[str, Any]:
    """
    Get available status values
    
    Returns list of available status values for filtering and updates.
    """
    try:
        statuses = agent.get_available_statuses()
        return {
            "statuses": statuses,
            "descriptions": {
                "pending": "Not yet practiced",
                "in_progress": "Currently learning",
                "learned": "Successfully mastered"
            }
        }
        
    except Exception as e:
        logger.error(f"Error getting statuses: {e}")
        return {"statuses": [], "error": str(e)}


@router.get("/health")
async def phrasal_verbs_health_check(
    agent: PhrasalVerbAgent = Depends(get_phrasal_verb_agent)
) -> Dict[str, Any]:
    """
    Health check for phrasal verbs service
    
    Returns status of phrasal verb agent and data availability.
    """
    try:
        health_status = agent.health_check()
        return health_status
        
    except Exception as e:
        logger.error(f"Phrasal verbs health check error: {e}")
        return {"status": "error", "message": str(e)}