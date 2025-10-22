"""
History API endpoints
Handles learning history management and retrieval
"""
import logging
from datetime import datetime
from typing import Dict, Any, List, Optional

from fastapi import APIRouter, HTTPException, Depends, Query
from fastapi.responses import JSONResponse

from models.api_models import (
    HistoryEntry, HistoryFilters, HistoryResponse, 
    SuccessResponse, ErrorResponse
)
from utils.error_handler import ErrorHandler, HTTPExceptionHandler
from utils.response_formatter import ResponseFormatter

logger = logging.getLogger("history_api")
router = APIRouter()
error_handler = ErrorHandler("history_api")

# In-memory history storage (would be replaced with database in production)
history_storage: List[Dict[str, Any]] = []
history_id_counter = 1


def get_next_history_id() -> int:
    """Get next available history ID"""
    global history_id_counter
    current_id = history_id_counter
    history_id_counter += 1
    return current_id


async def add_history_entry(
    section: str,
    query: str,
    result: str,
    explanation: Optional[str] = None,
    examples: Optional[List[str]] = None,
    tags: Optional[List[str]] = None
) -> HistoryEntry:
    """Add a new history entry"""
    try:
        entry_data = {
            "id": get_next_history_id(),
            "section": section,
            "query": query,
            "result": result,
            "explanation": explanation or "",
            "examples": examples or [],
            "tags": tags or [],
            "created_at": datetime.now(),
            "updated_at": datetime.now()
        }
        
        history_storage.append(entry_data)
        
        return HistoryEntry(**entry_data)
        
    except Exception as e:
        logger.error(f"Error adding history entry: {e}")
        raise e


@router.get("/", response_model=HistoryResponse)
async def get_history(
    section: str = Query(None, description="Filter by section (vocabulary/correction/grammar/phrasal_verbs)"),
    search: str = Query(None, description="Search term for query or result"),
    tags: List[str] = Query(None, description="Filter by tags"),
    date_from: Optional[datetime] = Query(None, description="Filter from date"),
    date_to: Optional[datetime] = Query(None, description="Filter to date"),
    limit: int = Query(50, ge=1, le=200, description="Maximum results to return"),
    offset: int = Query(0, ge=0, description="Results offset for pagination")
) -> HistoryResponse:
    """
    Get learning history with filtering and search
    
    - **section**: Filter by specific section
    - **search**: Search in queries and results
    - **tags**: Filter by specific tags
    - **date_from**: Filter entries from this date
    - **date_to**: Filter entries until this date
    - **limit**: Maximum number of results (1-200)
    - **offset**: Number of results to skip
    
    Returns paginated history entries matching the criteria.
    """
    try:
        logger.info(f"History request: section={section}, search={search}")
        
        # Create filters object
        filters = HistoryFilters(
            section=section,
            search=search,
            tags=tags,
            date_from=date_from,
            date_to=date_to,
            limit=limit,
            offset=offset
        )
        
        # Filter history entries
        filtered_entries = history_storage.copy()
        
        # Apply section filter
        if filters.section:
            filtered_entries = [
                entry for entry in filtered_entries
                if entry["section"] == filters.section
            ]
        
        # Apply search filter
        if filters.search:
            search_term = filters.search.lower()
            filtered_entries = [
                entry for entry in filtered_entries
                if (search_term in entry["query"].lower() or
                    search_term in entry["result"].lower() or
                    search_term in entry.get("explanation", "").lower())
            ]
        
        # Apply tags filter
        if filters.tags:
            filtered_entries = [
                entry for entry in filtered_entries
                if any(tag in entry.get("tags", []) for tag in filters.tags)
            ]
        
        # Apply date filters
        if filters.date_from:
            filtered_entries = [
                entry for entry in filtered_entries
                if entry["created_at"] >= filters.date_from
            ]
        
        if filters.date_to:
            filtered_entries = [
                entry for entry in filtered_entries
                if entry["created_at"] <= filters.date_to
            ]
        
        # Sort by creation date (newest first)
        filtered_entries.sort(key=lambda x: x["created_at"], reverse=True)
        
        # Get total count before pagination
        total_count = len(filtered_entries)
        
        # Apply pagination
        start_idx = filters.offset
        end_idx = start_idx + filters.limit
        paginated_entries = filtered_entries[start_idx:end_idx]
        
        # Convert to HistoryEntry objects
        history_entries = []
        for entry_data in paginated_entries:
            history_entry = HistoryEntry(**entry_data)
            history_entries.append(history_entry)
        
        # Create response
        response = HistoryResponse(
            entries=history_entries,
            total_count=total_count,
            has_more=end_idx < total_count,
            filters_applied=filters
        )
        
        logger.info(f"Returning {len(history_entries)} history entries (total: {total_count})")
        return response
        
    except ValueError as e:
        logger.warning(f"Validation error: {e}")
        raise HTTPExceptionHandler.validation_exception(str(e))
        
    except Exception as e:
        logger.error(f"History retrieval error: {e}")
        error_response = error_handler.handle_generic_error(e, "history retrieval")
        raise HTTPExceptionHandler.create_http_exception(500, error_response)


@router.get("/{entry_id}", response_model=HistoryEntry)
async def get_history_entry(entry_id: int) -> HistoryEntry:
    """
    Get a specific history entry by ID
    
    - **entry_id**: Unique identifier of the history entry
    
    Returns the history entry with all details.
    """
    try:
        logger.info(f"Getting history entry by ID: {entry_id}")
        
        # Find the entry
        entry_data = None
        for entry in history_storage:
            if entry["id"] == entry_id:
                entry_data = entry
                break
        
        if not entry_data:
            raise HTTPExceptionHandler.not_found_exception("History entry")
        
        return HistoryEntry(**entry_data)
        
    except HTTPException:
        raise
        
    except Exception as e:
        logger.error(f"Error getting history entry: {e}")
        error_response = error_handler.handle_generic_error(e, "history entry retrieval")
        raise HTTPExceptionHandler.create_http_exception(500, error_response)


@router.delete("/{entry_id}", response_model=SuccessResponse)
async def delete_history_entry(entry_id: int) -> SuccessResponse:
    """
    Delete a specific history entry
    
    - **entry_id**: Unique identifier of the history entry to delete
    
    Returns success confirmation.
    """
    try:
        logger.info(f"Deleting history entry: {entry_id}")
        
        # Find and remove the entry
        entry_found = False
        for i, entry in enumerate(history_storage):
            if entry["id"] == entry_id:
                history_storage.pop(i)
                entry_found = True
                break
        
        if not entry_found:
            raise HTTPExceptionHandler.not_found_exception("History entry")
        
        return ResponseFormatter.format_success_response(
            f"History entry {entry_id} deleted successfully"
        )
        
    except HTTPException:
        raise
        
    except Exception as e:
        logger.error(f"Error deleting history entry: {e}")
        error_response = error_handler.handle_generic_error(e, "history entry deletion")
        raise HTTPExceptionHandler.create_http_exception(500, error_response)


@router.delete("/", response_model=SuccessResponse)
async def clear_history(
    section: str = Query(None, description="Clear only specific section"),
    confirm: bool = Query(False, description="Confirmation required for clearing all history")
) -> SuccessResponse:
    """
    Clear history entries
    
    - **section**: Clear only entries from specific section (optional)
    - **confirm**: Must be true to clear all history
    
    Returns success confirmation with count of deleted entries.
    """
    try:
        if section:
            # Clear specific section
            logger.info(f"Clearing history for section: {section}")
            
            initial_count = len(history_storage)
            history_storage[:] = [
                entry for entry in history_storage
                if entry["section"] != section
            ]
            deleted_count = initial_count - len(history_storage)
            
            return ResponseFormatter.format_success_response(
                f"Cleared {deleted_count} entries from {section} section"
            )
        
        elif confirm:
            # Clear all history
            logger.info("Clearing all history")
            
            deleted_count = len(history_storage)
            history_storage.clear()
            
            return ResponseFormatter.format_success_response(
                f"Cleared all {deleted_count} history entries"
            )
        
        else:
            raise HTTPException(
                status_code=400,
                detail="Must specify section or set confirm=true to clear all history"
            )
        
    except HTTPException:
        raise
        
    except Exception as e:
        logger.error(f"Error clearing history: {e}")
        error_response = error_handler.handle_generic_error(e, "history clearing")
        raise HTTPExceptionHandler.create_http_exception(500, error_response)


@router.get("/stats/summary")
async def get_history_statistics() -> Dict[str, Any]:
    """
    Get history statistics and summary
    
    Returns comprehensive statistics about learning history.
    """
    try:
        total_entries = len(history_storage)
        
        # Count by section
        section_counts = {}
        tag_counts = {}
        
        for entry in history_storage:
            section = entry["section"]
            section_counts[section] = section_counts.get(section, 0) + 1
            
            # Count tags
            for tag in entry.get("tags", []):
                tag_counts[tag] = tag_counts.get(tag, 0) + 1
        
        # Get date range
        if history_storage:
            dates = [entry["created_at"] for entry in history_storage]
            earliest_date = min(dates)
            latest_date = max(dates)
        else:
            earliest_date = None
            latest_date = None
        
        return {
            "total_entries": total_entries,
            "section_distribution": section_counts,
            "popular_tags": dict(sorted(tag_counts.items(), key=lambda x: x[1], reverse=True)[:10]),
            "date_range": {
                "earliest": earliest_date.isoformat() if earliest_date else None,
                "latest": latest_date.isoformat() if latest_date else None
            },
            "available_sections": list(section_counts.keys())
        }
        
    except Exception as e:
        logger.error(f"Error getting history statistics: {e}")
        return {"error": str(e)}


@router.get("/meta/sections")
async def get_available_sections() -> Dict[str, Any]:
    """
    Get available sections for filtering
    
    Returns list of sections that have history entries.
    """
    try:
        sections = set()
        for entry in history_storage:
            sections.add(entry["section"])
        
        return {
            "sections": list(sections),
            "descriptions": {
                "vocabulary": "Vocabulary explanations and translations",
                "correction": "Writing corrections and grammar fixes",
                "grammar": "Grammar explanations and word comparisons",
                "phrasal_verbs": "Phrasal verb learning and progress"
            }
        }
        
    except Exception as e:
        logger.error(f"Error getting sections: {e}")
        return {"sections": [], "error": str(e)}


# Helper function to add entries from other endpoints
async def save_to_history(
    section: str,
    query: str,
    result: str,
    explanation: Optional[str] = None,
    examples: Optional[List[str]] = None,
    tags: Optional[List[str]] = None
) -> None:
    """Save interaction to history (called by other API endpoints)"""
    try:
        await add_history_entry(section, query, result, explanation, examples, tags)
        logger.info(f"Saved {section} interaction to history")
    except Exception as e:
        logger.error(f"Failed to save to history: {e}")
        # Don't raise exception - history saving shouldn't break main functionality