"""
Grammar API endpoints
Handles grammar explanations and word comparisons
"""
import logging
from typing import Dict, Any, List, Tuple

from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import JSONResponse

from models.api_models import GrammarRequest, GrammarResponse, ErrorResponse
from agents.grammar_agent import GrammarAgent
from utils.error_handler import ErrorHandler, HTTPExceptionHandler

logger = logging.getLogger("grammar_api")
router = APIRouter()

# Initialize grammar agent
grammar_agent = GrammarAgent()
error_handler = ErrorHandler("grammar_api")


async def get_grammar_agent() -> GrammarAgent:
    """Dependency to get grammar agent instance"""
    return grammar_agent


@router.post("/", response_model=GrammarResponse)
async def explain_grammar(
    request: GrammarRequest,
    agent: GrammarAgent = Depends(get_grammar_agent)
) -> GrammarResponse:
    """
    Explain grammar rules or compare words
    
    - **question**: Grammar question or words to compare
    - **question_type**: Type of question (explanation/comparison/usage)
    
    Returns grammar explanation with rules, examples, and related concepts.
    """
    try:
        logger.info(f"Grammar request: {request.question} (type: {request.question_type})")
        
        # Validate request
        if not request.question.strip():
            raise HTTPException(
                status_code=422,
                detail="Question cannot be empty"
            )
        
        if len(request.question) > 1000:
            raise HTTPException(
                status_code=422,
                detail="Question too long (maximum 1000 characters)"
            )
        
        # Process grammar explanation
        response = await agent.explain_grammar(request)
        
        logger.info(f"Grammar response generated for: {request.question}")
        return response
        
    except ValueError as e:
        logger.warning(f"Validation error: {e}")
        raise HTTPExceptionHandler.validation_exception(str(e))
        
    except Exception as e:
        logger.error(f"Grammar explanation error: {e}")
        error_response = error_handler.handle_model_error(e, "GrammarAgent")
        raise HTTPExceptionHandler.create_http_exception(500, error_response)


@router.get("/health")
async def grammar_health_check(
    agent: GrammarAgent = Depends(get_grammar_agent)
) -> Dict[str, Any]:
    """
    Health check for grammar service
    
    Returns status of grammar agent and available features.
    """
    try:
        health_status = agent.health_check()
        return health_status
        
    except Exception as e:
        logger.error(f"Grammar health check error: {e}")
        return {"status": "error", "message": str(e)}


@router.get("/topics")
async def get_grammar_topics(
    agent: GrammarAgent = Depends(get_grammar_agent)
) -> Dict[str, Any]:
    """
    Get available grammar topics
    
    Returns list of grammar topics that can be explained.
    """
    try:
        topics = agent.get_available_topics()
        return {
            "grammar_topics": topics,
            "total_topics": len(topics),
            "description": "Available grammar topics for explanations"
        }
        
    except Exception as e:
        logger.error(f"Error getting grammar topics: {e}")
        return {"grammar_topics": [], "error": str(e)}


@router.get("/word-comparisons")
async def get_word_comparisons(
    agent: GrammarAgent = Depends(get_grammar_agent)
) -> Dict[str, Any]:
    """
    Get available word comparisons
    
    Returns list of word pairs that can be compared.
    """
    try:
        comparisons = agent.get_word_comparisons()
        
        # Format comparisons for API response
        formatted_comparisons = []
        for word_pair in comparisons:
            formatted_comparisons.append({
                "word1": word_pair[0],
                "word2": word_pair[1],
                "comparison": f"{word_pair[0]} vs {word_pair[1]}"
            })
        
        return {
            "word_comparisons": formatted_comparisons,
            "total_comparisons": len(formatted_comparisons),
            "description": "Available word pairs for comparison"
        }
        
    except Exception as e:
        logger.error(f"Error getting word comparisons: {e}")
        return {"word_comparisons": [], "error": str(e)}


@router.get("/question-types")
async def get_question_types() -> Dict[str, Any]:
    """
    Get available question types
    
    Returns information about different types of grammar questions.
    """
    return {
        "question_types": {
            "explanation": {
                "description": "General grammar rule explanations",
                "examples": [
                    "How do I use articles?",
                    "What are modal verbs?",
                    "Explain past tense"
                ]
            },
            "comparison": {
                "description": "Compare similar words or concepts",
                "examples": [
                    "What's the difference between 'affect' and 'effect'?",
                    "Compare 'then' and 'than'",
                    "Difference between 'advice' and 'advise'"
                ]
            },
            "usage": {
                "description": "How to use specific grammar elements",
                "examples": [
                    "How do I use prepositions?",
                    "When should I use 'the'?",
                    "Usage of conditional sentences"
                ]
            }
        },
        "default": "explanation"
    }