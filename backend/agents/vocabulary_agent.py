"""
Vocabulary Agent for English Assistant
Handles vocabulary explanations using bilingual translation models
"""
import logging
import re
from typing import Dict, List, Optional, Tuple
from langdetect import detect, DetectorFactory

from backend.models.api_models import VocabularyRequest, VocabularyResponse
from backend.utils.model_manager import get_model_manager
from backend.utils.response_formatter import ResponseFormatter, DataTransformer
from backend.utils.error_handler import ModelErrorHandler


# Set seed for consistent language detection
DetectorFactory.seed = 0


class VocabularyAgent:
    """Agent for vocabulary explanations and translations"""
    
    def __init__(self):
        self.logger = logging.getLogger("vocabulary_agent")
        self.model_manager = get_model_manager()
        
        # Translation model preferences (in order of preference)
        self.translation_models = [
            "nllb-200",
            "opus-mt-es-en", 
            "m2m100"
        ]
        
        # Language code mappings
        self.language_codes = {
            "spanish": "es",
            "english": "en",
            "es": "es",
            "en": "en"
        }
    
    async def explain_vocabulary(self, request: VocabularyRequest) -> VocabularyResponse:
        """
        Explain vocabulary using bilingual translation models
        
        Args:
            request: VocabularyRequest with query and language preferences
            
        Returns:
            VocabularyResponse with explanations and translations
        """
        try:
            self.logger.info(f"Processing vocabulary request: {request.query}")
            
            # Clean and validate input
            query = DataTransformer.clean_text(request.query)
            if not query:
                raise ValueError("Empty query after cleaning")
            
            # Detect language
            detected_language = self._detect_language(query)
            self.logger.info(f"Detected language: {detected_language}")
            
            # Get translations
            translations = await self._get_translations(
                query, 
                detected_language,
                request.target_language
            )
            
            # Generate explanation
            explanation = self._generate_explanation(
                query, 
                translations, 
                detected_language
            )
            
            # Get examples
            examples = self._generate_examples(query, translations)
            
            # Extract additional information
            word_info = self._analyze_word(query)
            
            # Generate tags
            tags = DataTransformer.extract_tags(query, "vocabulary")
            tags.extend([detected_language, request.target_language])
            
            # Format response
            return ResponseFormatter.format_vocabulary_response(
                query=request.query,
                result=translations.get(request.target_language, query),
                translations=translations,
                language_detected=detected_language,
                explanation=explanation,
                examples=examples,
                tags=list(set(tags)),
                phonetic=word_info.get("phonetic"),
                word_type=word_info.get("word_type"),
                difficulty_level=word_info.get("difficulty_level", "intermediate")
            )
            
        except Exception as e:
            self.logger.error(f"Error in vocabulary explanation: {e}")
            error_response = ModelErrorHandler.handle_inference_error("VocabularyAgent", e)
            raise Exception(error_response.message)
    
    def _detect_language(self, text: str) -> str:
        """Detect the language of input text"""
        try:
            # Use langdetect for language detection
            detected = detect(text)
            
            # Map common language codes
            language_mapping = {
                "es": "es",
                "en": "en",
                "ca": "es",  # Catalan -> Spanish (similar)
                "pt": "es",  # Portuguese -> Spanish (similar)
            }
            
            return language_mapping.get(detected, "en")  # Default to English
            
        except Exception as e:
            self.logger.warning(f"Language detection failed: {e}, defaulting to English")
            return "en"
    
    async def _get_translations(
        self, 
        text: str, 
        source_lang: str, 
        target_lang: str
    ) -> Dict[str, str]:
        """Get translations using available models"""
        translations = {}
        
        # Try each translation model in order of preference
        for model_key in self.translation_models:
            try:
                translation = await self._translate_with_model(
                    text, source_lang, target_lang, model_key
                )
                
                if translation and translation != text:
                    translations[target_lang] = translation
                    self.logger.info(f"Translation successful with {model_key}")
                    break
                    
            except Exception as e:
                self.logger.warning(f"Translation failed with {model_key}: {e}")
                continue
        
        # If no translation found, use the original text
        if target_lang not in translations:
            translations[target_lang] = text
            self.logger.warning("No translation model succeeded, using original text")
        
        # Add source language
        translations[source_lang] = text
        
        return translations
    
    async def _translate_with_model(
        self, 
        text: str, 
        source_lang: str, 
        target_lang: str, 
        model_key: str
    ) -> Optional[str]:
        """Translate text using a specific model"""
        try:
            pipeline = self.model_manager.get_pipeline(model_key)
            if pipeline is None:
                raise Exception(f"Failed to get pipeline for {model_key}")
            
            # Prepare input based on model type
            if model_key == "nllb-200":
                # NLLB format
                input_text = text
                result = pipeline(
                    input_text,
                    src_lang=f"{source_lang}_Latn",
                    tgt_lang=f"{target_lang}_Latn",
                    max_length=200
                )
            elif model_key == "opus-mt-es-en":
                # OPUS-MT format (Spanish to English only)
                if source_lang == "es" and target_lang == "en":
                    result = pipeline(text, max_length=200)
                else:
                    return None
            elif model_key == "m2m100":
                # M2M100 format
                result = pipeline(
                    text,
                    src_lang=source_lang,
                    tgt_lang=target_lang,
                    max_length=200
                )
            else:
                return None
            
            # Extract translation from result
            if isinstance(result, list) and len(result) > 0:
                if isinstance(result[0], dict) and "translation_text" in result[0]:
                    return result[0]["translation_text"].strip()
                elif isinstance(result[0], dict) and "generated_text" in result[0]:
                    return result[0]["generated_text"].strip()
            
            return None
            
        except Exception as e:
            self.logger.error(f"Translation error with {model_key}: {e}")
            raise e
    
    def _generate_explanation(
        self, 
        query: str, 
        translations: Dict[str, str], 
        detected_language: str
    ) -> str:
        """Generate explanation for the vocabulary"""
        explanations = []
        
        # Basic translation explanation
        if "en" in translations and "es" in translations:
            if detected_language == "es":
                explanations.append(f"'{query}' in English means '{translations['en']}'")
            else:
                explanations.append(f"'{query}' in Spanish is '{translations['es']}'")
        
        # Word type analysis
        word_info = self._analyze_word(query)
        if word_info.get("word_type"):
            explanations.append(f"This is a {word_info['word_type']}")
        
        # Usage context
        if len(query.split()) == 1:
            explanations.append("This is a single word")
        else:
            explanations.append("This is a phrase or sentence")
        
        return ". ".join(explanations) + "."
    
    def _generate_examples(self, query: str, translations: Dict[str, str]) -> List[str]:
        """Generate usage examples"""
        examples = []
        
        # Simple example generation based on word type
        word_lower = query.lower()
        
        # Common example patterns
        example_patterns = {
            "hello": ["Hello, how are you?", "Hello everyone!"],
            "goodbye": ["Goodbye, see you later!", "Goodbye for now."],
            "thank": ["Thank you very much.", "Thanks for your help."],
            "please": ["Please help me.", "Could you please wait?"],
            "house": ["I live in a big house.", "The house is beautiful."],
            "car": ["I drive a red car.", "The car is very fast."],
            "book": ["I'm reading a good book.", "This book is interesting."],
            "water": ["I need some water.", "The water is cold."],
            "food": ["The food is delicious.", "I love Italian food."],
        }
        
        # Check for pattern matches
        for pattern, pattern_examples in example_patterns.items():
            if pattern in word_lower:
                examples.extend(pattern_examples[:2])
                break
        
        # Generic examples if no pattern found
        if not examples:
            if len(query.split()) == 1:
                # Single word examples
                examples = [
                    f"I use '{query}' in my daily conversation.",
                    f"The word '{query}' is important to learn."
                ]
            else:
                # Phrase examples
                examples = [
                    f"You can say: '{query}'",
                    f"Example usage: '{query}'"
                ]
        
        return examples[:3]  # Limit to 3 examples
    
    def _analyze_word(self, text: str) -> Dict[str, str]:
        """Analyze word characteristics"""
        analysis = {}
        
        # Simple word type detection
        text_lower = text.lower().strip()
        
        # Common word patterns
        if re.match(r'^(hello|hi|hey|good morning|good afternoon|good evening)$', text_lower):
            analysis["word_type"] = "greeting"
        elif re.match(r'^(goodbye|bye|see you|farewell)$', text_lower):
            analysis["word_type"] = "farewell"
        elif re.match(r'^(please|thank you|thanks|excuse me|sorry)$', text_lower):
            analysis["word_type"] = "polite expression"
        elif re.match(r'^(yes|no|maybe|perhaps)$', text_lower):
            analysis["word_type"] = "response word"
        elif text_lower.endswith('ing'):
            analysis["word_type"] = "verb (present participle)"
        elif text_lower.endswith('ed'):
            analysis["word_type"] = "verb (past tense)"
        elif text_lower.endswith('ly'):
            analysis["word_type"] = "adverb"
        elif len(text.split()) == 1:
            analysis["word_type"] = "word"
        else:
            analysis["word_type"] = "phrase"
        
        # Difficulty level based on length and complexity
        word_count = len(text.split())
        char_count = len(text)
        
        if word_count == 1 and char_count <= 5:
            analysis["difficulty_level"] = "beginner"
        elif word_count <= 3 and char_count <= 15:
            analysis["difficulty_level"] = "intermediate"
        else:
            analysis["difficulty_level"] = "advanced"
        
        return analysis
    
    def get_supported_languages(self) -> List[str]:
        """Get list of supported languages"""
        return ["es", "en"]
    
    def health_check(self) -> Dict[str, any]:
        """Perform health check on vocabulary agent"""
        try:
            # Check model availability
            available_models = []
            for model_key in self.translation_models:
                health = self.model_manager.health_check(model_key)
                if health["status"] == "healthy":
                    available_models.append(model_key)
            
            return {
                "status": "healthy" if available_models else "degraded",
                "available_models": available_models,
                "total_models": len(self.translation_models),
                "supported_languages": self.get_supported_languages()
            }
            
        except Exception as e:
            return {
                "status": "error",
                "message": str(e)
            }