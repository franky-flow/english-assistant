"""
Response formatting utilities for English Assistant API
Handles standardized response formatting and data transformation
"""
from datetime import datetime
from typing import Any, Dict, List, Optional, Union
from uuid import uuid4

from backend.models.api_models import (
    BaseResponse, ErrorResponse, SuccessResponse,
    VocabularyResponse, CorrectionResponse, GrammarResponse,
    HistoryEntry, PhrasalVerb
)


class ResponseFormatter:
    """Utility class for formatting API responses"""
    
    @staticmethod
    def format_vocabulary_response(
        query: str,
        result: str,
        translations: Dict[str, str],
        language_detected: str,
        explanation: Optional[str] = None,
        examples: Optional[List[str]] = None,
        tags: Optional[List[str]] = None,
        **kwargs
    ) -> VocabularyResponse:
        """Format vocabulary explanation response"""
        return VocabularyResponse(
            query=query,
            result=result,
            explanation=explanation or "",
            examples=examples or [],
            tags=tags or ["vocabulary", "translation"],
            translations=translations,
            language_detected=language_detected,
            phonetic=kwargs.get('phonetic'),
            word_type=kwargs.get('word_type'),
            difficulty_level=kwargs.get('difficulty_level', 'intermediate')
        )
    
    @staticmethod
    def format_correction_response(
        query: str,
        original_text: str,
        corrected_text: str,
        corrections: List[Dict[str, Any]],
        explanation: Optional[str] = None,
        examples: Optional[List[str]] = None,
        tags: Optional[List[str]] = None,
        **kwargs
    ) -> CorrectionResponse:
        """Format writing correction response"""
        from backend.models.api_models import CorrectionDetail
        
        # Convert correction dictionaries to CorrectionDetail objects
        correction_details = []
        for correction in corrections:
            correction_details.append(CorrectionDetail(**correction))
        
        return CorrectionResponse(
            query=query,
            result=corrected_text,
            explanation=explanation or "Text has been corrected for grammar and style.",
            examples=examples or [],
            tags=tags or ["correction", "grammar"],
            original_text=original_text,
            corrected_text=corrected_text,
            corrections=correction_details,
            grammar_rules=kwargs.get('grammar_rules', []),
            correction_count=len(corrections),
            confidence_score=kwargs.get('confidence_score')
        )
    
    @staticmethod
    def format_grammar_response(
        query: str,
        result: str,
        rule_category: str,
        explanation: Optional[str] = None,
        examples: Optional[List[str]] = None,
        tags: Optional[List[str]] = None,
        **kwargs
    ) -> GrammarResponse:
        """Format grammar explanation response"""
        return GrammarResponse(
            query=query,
            result=result,
            explanation=explanation or "",
            examples=examples or [],
            tags=tags or ["grammar", "explanation"],
            rule_category=rule_category,
            related_concepts=kwargs.get('related_concepts', []),
            difficulty_level=kwargs.get('difficulty_level', 'intermediate'),
            common_mistakes=kwargs.get('common_mistakes', [])
        )
    
    @staticmethod
    def format_success_response(
        message: str,
        data: Optional[Dict[str, Any]] = None
    ) -> SuccessResponse:
        """Format generic success response"""
        return SuccessResponse(
            message=message,
            data=data
        )
    
    @staticmethod
    def format_error_response(
        error: str,
        message: str,
        details: Optional[Dict[str, Any]] = None,
        request_id: Optional[str] = None
    ) -> ErrorResponse:
        """Format error response"""
        return ErrorResponse(
            error=error,
            message=message,
            details=details,
            request_id=request_id or str(uuid4())
        )


class DataTransformer:
    """Utility class for data transformation operations"""
    
    @staticmethod
    def clean_text(text: str) -> str:
        """Clean and normalize text input"""
        if not text:
            return ""
        
        # Remove extra whitespace and normalize
        cleaned = " ".join(text.strip().split())
        
        # Remove potentially harmful characters
        cleaned = cleaned.replace('\x00', '')  # Remove null bytes
        
        return cleaned
    
    @staticmethod
    def extract_tags(text: str, section: str) -> List[str]:
        """Extract relevant tags from text and section"""
        tags = [section.lower()]
        
        # Add length-based tags
        word_count = len(text.split())
        if word_count == 1:
            tags.append("single-word")
        elif word_count <= 5:
            tags.append("short-phrase")
        elif word_count <= 20:
            tags.append("sentence")
        else:
            tags.append("paragraph")
        
        # Add content-based tags
        if any(char in text for char in '?'):
            tags.append("question")
        if any(char in text for char in '!'):
            tags.append("exclamation")
        if text.isupper():
            tags.append("uppercase")
        
        return list(set(tags))  # Remove duplicates
    
    @staticmethod
    def calculate_difficulty_level(text: str, corrections_count: int = 0) -> str:
        """Calculate difficulty level based on text complexity"""
        word_count = len(text.split())
        
        # Simple heuristic for difficulty
        if word_count <= 5 and corrections_count <= 1:
            return "beginner"
        elif word_count <= 15 and corrections_count <= 3:
            return "intermediate"
        else:
            return "advanced"
    
    @staticmethod
    def format_examples(examples: List[str], max_examples: int = 3) -> List[str]:
        """Format and limit examples list"""
        if not examples:
            return []
        
        # Clean and limit examples
        cleaned_examples = []
        for example in examples[:max_examples]:
            cleaned = DataTransformer.clean_text(example)
            if cleaned and len(cleaned) <= 200:  # Reasonable length limit
                cleaned_examples.append(cleaned)
        
        return cleaned_examples
    
    @staticmethod
    def merge_corrections(corrections: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Merge and summarize correction information"""
        if not corrections:
            return {
                'total_corrections': 0,
                'error_types': [],
                'grammar_rules': []
            }
        
        error_types = set()
        grammar_rules = set()
        
        for correction in corrections:
            if 'error_type' in correction:
                error_types.add(correction['error_type'])
            if 'rule_explanation' in correction:
                grammar_rules.add(correction['rule_explanation'])
        
        return {
            'total_corrections': len(corrections),
            'error_types': list(error_types),
            'grammar_rules': list(grammar_rules)
        }


class ValidationHelper:
    """Utility class for input validation"""
    
    @staticmethod
    def validate_language_code(code: str) -> bool:
        """Validate language code format"""
        # Simple validation for ISO 639-1 codes
        return isinstance(code, str) and len(code) == 2 and code.isalpha()
    
    @staticmethod
    def validate_text_length(text: str, min_length: int = 1, max_length: int = 5000) -> bool:
        """Validate text length constraints"""
        if not isinstance(text, str):
            return False
        
        text_length = len(text.strip())
        return min_length <= text_length <= max_length
    
    @staticmethod
    def sanitize_search_query(query: str) -> str:
        """Sanitize search query for database operations"""
        if not query:
            return ""
        
        # Remove potentially harmful characters for SQL
        sanitized = query.replace("'", "''")  # Escape single quotes
        sanitized = sanitized.replace(";", "")   # Remove semicolons
        sanitized = sanitized.replace("--", "")  # Remove SQL comments
        
        return DataTransformer.clean_text(sanitized)
    
    @staticmethod
    def validate_pagination_params(limit: int, offset: int) -> tuple[int, int]:
        """Validate and normalize pagination parameters"""
        # Ensure reasonable limits
        limit = max(1, min(limit, 200))
        offset = max(0, offset)
        
        return limit, offset


class CacheKeyGenerator:
    """Utility class for generating cache keys"""
    
    @staticmethod
    def generate_vocabulary_key(query: str, source_lang: str, target_lang: str) -> str:
        """Generate cache key for vocabulary queries"""
        normalized_query = DataTransformer.clean_text(query).lower()
        return f"vocab:{source_lang}:{target_lang}:{hash(normalized_query)}"
    
    @staticmethod
    def generate_correction_key(text: str, correction_level: str) -> str:
        """Generate cache key for correction queries"""
        normalized_text = DataTransformer.clean_text(text).lower()
        return f"correction:{correction_level}:{hash(normalized_text)}"
    
    @staticmethod
    def generate_grammar_key(question: str, question_type: str) -> str:
        """Generate cache key for grammar queries"""
        normalized_question = DataTransformer.clean_text(question).lower()
        return f"grammar:{question_type}:{hash(normalized_question)}"