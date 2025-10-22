"""
Pydantic models for API requests and responses
English Assistant - Core data validation and serialization
"""
from datetime import datetime
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field, validator


# Base Response Models
class BaseResponse(BaseModel):
    """Base response model for all API endpoints"""
    query: str = Field(..., description="Original user query")
    result: str = Field(..., description="Processed result")
    explanation: Optional[str] = Field(None, description="Detailed explanation")
    examples: List[str] = Field(default_factory=list, description="Usage examples")
    tags: List[str] = Field(default_factory=list, description="Categorization tags")
    timestamp: datetime = Field(default_factory=datetime.now, description="Response timestamp")


class ErrorResponse(BaseModel):
    """Standardized error response model"""
    error: str = Field(..., description="Error type")
    message: str = Field(..., description="Human-readable error message")
    details: Optional[Dict[str, Any]] = Field(None, description="Additional error details")
    timestamp: datetime = Field(default_factory=datetime.now, description="Error timestamp")
    request_id: Optional[str] = Field(None, description="Request identifier for tracking")


# Vocabulary Models
class VocabularyRequest(BaseModel):
    """Request model for vocabulary explanations"""
    query: str = Field(..., min_length=1, max_length=500, description="Word or sentence to explain")
    source_language: str = Field(default="es", description="Source language code (default: Spanish)")
    target_language: str = Field(default="en", description="Target language code (default: English)")
    
    @validator('query')
    def validate_query(cls, v):
        if not v.strip():
            raise ValueError('Query cannot be empty or whitespace only')
        return v.strip()


class VocabularyResponse(BaseResponse):
    """Response model for vocabulary explanations"""
    translations: Dict[str, str] = Field(default_factory=dict, description="Translation mappings")
    language_detected: str = Field(..., description="Detected source language")
    phonetic: Optional[str] = Field(None, description="Phonetic pronunciation")
    word_type: Optional[str] = Field(None, description="Part of speech")
    difficulty_level: Optional[str] = Field(None, description="Difficulty level (beginner/intermediate/advanced)")


# Writing Correction Models
class CorrectionRequest(BaseModel):
    """Request model for writing correction"""
    text: str = Field(..., min_length=1, max_length=5000, description="Text to correct")
    correction_level: str = Field(default="comprehensive", description="Level of correction (basic/comprehensive)")
    
    @validator('text')
    def validate_text(cls, v):
        if not v.strip():
            raise ValueError('Text cannot be empty or whitespace only')
        return v.strip()
    
    @validator('correction_level')
    def validate_correction_level(cls, v):
        allowed_levels = ['basic', 'comprehensive']
        if v not in allowed_levels:
            raise ValueError(f'Correction level must be one of: {allowed_levels}')
        return v


class CorrectionDetail(BaseModel):
    """Individual correction detail"""
    original: str = Field(..., description="Original text segment")
    corrected: str = Field(..., description="Corrected text segment")
    error_type: str = Field(..., description="Type of error (grammar/spelling/punctuation)")
    rule_explanation: str = Field(..., description="Grammar rule explanation")
    position: Dict[str, int] = Field(..., description="Position in text (start, end)")


class CorrectionResponse(BaseResponse):
    """Response model for writing correction"""
    original_text: str = Field(..., description="Original submitted text")
    corrected_text: str = Field(..., description="Fully corrected text")
    corrections: List[CorrectionDetail] = Field(default_factory=list, description="Individual corrections")
    grammar_rules: List[str] = Field(default_factory=list, description="Applied grammar rules")
    correction_count: int = Field(default=0, description="Total number of corrections")
    confidence_score: Optional[float] = Field(None, description="Correction confidence (0-1)")


# Grammar Models
class GrammarRequest(BaseModel):
    """Request model for grammar explanations"""
    question: str = Field(..., min_length=1, max_length=1000, description="Grammar question or words to compare")
    question_type: str = Field(default="explanation", description="Type of question (explanation/comparison)")
    
    @validator('question')
    def validate_question(cls, v):
        if not v.strip():
            raise ValueError('Question cannot be empty or whitespace only')
        return v.strip()
    
    @validator('question_type')
    def validate_question_type(cls, v):
        allowed_types = ['explanation', 'comparison', 'usage']
        if v not in allowed_types:
            raise ValueError(f'Question type must be one of: {allowed_types}')
        return v


class GrammarResponse(BaseResponse):
    """Response model for grammar explanations"""
    rule_category: str = Field(..., description="Grammar rule category")
    related_concepts: List[str] = Field(default_factory=list, description="Related grammar concepts")
    difficulty_level: str = Field(default="intermediate", description="Concept difficulty level")
    common_mistakes: List[str] = Field(default_factory=list, description="Common mistakes to avoid")


# Phrasal Verb Models
class PhrasalVerbFilters(BaseModel):
    """Filters for phrasal verb queries"""
    difficulty: Optional[str] = Field(None, description="Filter by difficulty (beginner/intermediate/advanced)")
    status: Optional[str] = Field(None, description="Filter by status (pending/in_progress/learned)")
    search: Optional[str] = Field(None, description="Search term for verb or definition")
    limit: int = Field(default=50, ge=1, le=200, description="Maximum results to return")
    offset: int = Field(default=0, ge=0, description="Results offset for pagination")
    
    @validator('difficulty')
    def validate_difficulty(cls, v):
        if v is not None:
            allowed_difficulties = ['beginner', 'intermediate', 'advanced']
            if v not in allowed_difficulties:
                raise ValueError(f'Difficulty must be one of: {allowed_difficulties}')
        return v
    
    @validator('status')
    def validate_status(cls, v):
        if v is not None:
            allowed_statuses = ['pending', 'in_progress', 'learned']
            if v not in allowed_statuses:
                raise ValueError(f'Status must be one of: {allowed_statuses}')
        return v


class PhrasalVerbProgress(BaseModel):
    """Phrasal verb progress tracking"""
    attempts: int = Field(default=0, description="Number of practice attempts")
    correct_answers: int = Field(default=0, description="Number of correct answers")
    last_practiced: Optional[datetime] = Field(None, description="Last practice timestamp")
    mastery_level: float = Field(default=0.0, ge=0.0, le=1.0, description="Mastery level (0-1)")


class PhrasalVerb(BaseModel):
    """Phrasal verb model"""
    id: int = Field(..., description="Unique identifier")
    verb: str = Field(..., description="Phrasal verb")
    definition: str = Field(..., description="Definition")
    examples: List[str] = Field(default_factory=list, description="Usage examples")
    difficulty: str = Field(..., description="Difficulty level")
    status: str = Field(default="pending", description="Learning status")
    progress: PhrasalVerbProgress = Field(default_factory=PhrasalVerbProgress, description="Progress tracking")
    created_at: datetime = Field(default_factory=datetime.now, description="Creation timestamp")
    updated_at: datetime = Field(default_factory=datetime.now, description="Last update timestamp")


class PhrasalVerbUpdateRequest(BaseModel):
    """Request to update phrasal verb progress"""
    status: str = Field(..., description="New status (pending/in_progress/learned)")
    progress: Optional[PhrasalVerbProgress] = Field(None, description="Progress update")
    
    @validator('status')
    def validate_status(cls, v):
        allowed_statuses = ['pending', 'in_progress', 'learned']
        if v not in allowed_statuses:
            raise ValueError(f'Status must be one of: {allowed_statuses}')
        return v


# History Models
class HistoryFilters(BaseModel):
    """Filters for history queries"""
    section: Optional[str] = Field(None, description="Filter by section (vocabulary/correction/grammar/phrasal_verbs)")
    search: Optional[str] = Field(None, description="Search term for query or result")
    tags: Optional[List[str]] = Field(None, description="Filter by tags")
    date_from: Optional[datetime] = Field(None, description="Filter from date")
    date_to: Optional[datetime] = Field(None, description="Filter to date")
    limit: int = Field(default=50, ge=1, le=200, description="Maximum results to return")
    offset: int = Field(default=0, ge=0, description="Results offset for pagination")
    
    @validator('section')
    def validate_section(cls, v):
        if v is not None:
            allowed_sections = ['vocabulary', 'correction', 'grammar', 'phrasal_verbs']
            if v not in allowed_sections:
                raise ValueError(f'Section must be one of: {allowed_sections}')
        return v


class HistoryEntry(BaseModel):
    """History entry model"""
    id: int = Field(..., description="Unique identifier")
    section: str = Field(..., description="Section name")
    query: str = Field(..., description="Original query")
    result: str = Field(..., description="Result")
    explanation: Optional[str] = Field(None, description="Explanation")
    examples: List[str] = Field(default_factory=list, description="Examples")
    tags: List[str] = Field(default_factory=list, description="Tags")
    created_at: datetime = Field(..., description="Creation timestamp")
    updated_at: datetime = Field(..., description="Last update timestamp")


class HistoryResponse(BaseModel):
    """Response model for history queries"""
    entries: List[HistoryEntry] = Field(default_factory=list, description="History entries")
    total_count: int = Field(..., description="Total number of entries")
    has_more: bool = Field(..., description="Whether more entries are available")
    filters_applied: HistoryFilters = Field(..., description="Applied filters")


# Success Response Models
class SuccessResponse(BaseModel):
    """Generic success response"""
    success: bool = Field(True, description="Operation success status")
    message: str = Field(..., description="Success message")
    data: Optional[Dict[str, Any]] = Field(None, description="Additional response data")
    timestamp: datetime = Field(default_factory=datetime.now, description="Response timestamp")