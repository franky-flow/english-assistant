"""
Correction Agent for English Assistant
Handles grammar correction using T5 model and LanguageTool
"""
import logging
import re
from typing import Dict, List, Optional, Tuple, Any

from models.api_models import CorrectionRequest, CorrectionResponse
from utils.model_manager import get_model_manager
from utils.response_formatter import ResponseFormatter, DataTransformer
from utils.error_handler import ModelErrorHandler


class CorrectionAgent:
    """Agent for grammar correction and explanations"""
    
    def __init__(self):
        self.logger = logging.getLogger("correction_agent")
        self.model_manager = get_model_manager()
        
        # Grammar correction model
        self.grammar_model_key = "t5-grammar"
        
        # Grammar rule categories
        self.grammar_rules = {
            "subject_verb_agreement": "Subject and verb must agree in number",
            "article_usage": "Correct usage of articles (a, an, the)",
            "preposition_usage": "Proper preposition selection",
            "verb_tense": "Correct verb tense usage",
            "punctuation": "Proper punctuation marks",
            "capitalization": "Correct capitalization rules",
            "spelling": "Correct spelling of words",
            "word_order": "Proper word order in sentences",
            "plural_singular": "Correct plural and singular forms",
            "pronoun_usage": "Proper pronoun usage and agreement"
        }
    
    async def correct_text(self, request: CorrectionRequest) -> CorrectionResponse:
        """
        Correct text using grammar correction models and LanguageTool
        
        Args:
            request: CorrectionRequest with text to correct
            
        Returns:
            CorrectionResponse with corrections and explanations
        """
        try:
            self.logger.info(f"Processing correction request for text length: {len(request.text)}")
            
            # Clean and validate input
            original_text = DataTransformer.clean_text(request.text)
            if not original_text:
                raise ValueError("Empty text after cleaning")
            
            # Get corrections from both sources
            t5_corrections = await self._correct_with_t5(original_text)
            languagetool_corrections = self._correct_with_languagetool(original_text)
            
            # Merge and prioritize corrections
            merged_corrections = self._merge_corrections(
                original_text, 
                t5_corrections, 
                languagetool_corrections
            )
            
            # Apply corrections to get final text
            corrected_text = self._apply_corrections(original_text, merged_corrections)
            
            # Generate explanation
            explanation = self._generate_correction_explanation(
                original_text, 
                corrected_text, 
                merged_corrections
            )
            
            # Extract grammar rules
            grammar_rules = self._extract_grammar_rules(merged_corrections)
            
            # Generate examples
            examples = self._generate_correction_examples(merged_corrections)
            
            # Generate tags
            tags = DataTransformer.extract_tags(original_text, "correction")
            tags.extend(self._get_error_type_tags(merged_corrections))
            
            # Format response
            return ResponseFormatter.format_correction_response(
                query=request.text,
                original_text=original_text,
                corrected_text=corrected_text,
                corrections=merged_corrections,
                explanation=explanation,
                examples=examples,
                tags=list(set(tags)),
                grammar_rules=grammar_rules,
                confidence_score=self._calculate_confidence_score(merged_corrections)
            )
            
        except Exception as e:
            self.logger.error(f"Error in text correction: {e}")
            error_response = ModelErrorHandler.handle_inference_error("CorrectionAgent", e)
            raise Exception(error_response.message)
    
    async def _correct_with_t5(self, text: str) -> str:
        """Correct text using T5 grammar correction model"""
        try:
            pipeline = self.model_manager.get_pipeline(self.grammar_model_key)
            if pipeline is None:
                self.logger.warning("T5 grammar model not available")
                return text
            
            # Prepare input for T5 model
            input_text = f"grammar: {text}"
            
            # Get correction
            result = pipeline(
                input_text,
                max_length=len(text) + 50,  # Allow for expansion
                num_return_sequences=1,
                temperature=0.7
            )
            
            if isinstance(result, list) and len(result) > 0:
                corrected = result[0].get("generated_text", text)
                # Clean up the result
                corrected = corrected.replace("grammar: ", "").strip()
                return corrected
            
            return text
            
        except Exception as e:
            self.logger.error(f"T5 correction failed: {e}")
            return text
    
    def _correct_with_languagetool(self, text: str) -> List[Dict[str, Any]]:
        """Get corrections using LanguageTool"""
        corrections = []
        
        try:
            language_tool = self.model_manager.get_language_tool()
            if language_tool is None:
                self.logger.warning("LanguageTool not available")
                return corrections
            
            # Get matches from LanguageTool
            matches = language_tool.check(text)
            
            for match in matches:
                correction = {
                    "original": text[match.offset:match.offset + match.errorLength],
                    "corrected": match.replacements[0] if match.replacements else "",
                    "error_type": self._categorize_error_type(match.ruleId, match.category),
                    "rule_explanation": match.message,
                    "position": {
                        "start": match.offset,
                        "end": match.offset + match.errorLength
                    },
                    "confidence": self._calculate_match_confidence(match),
                    "source": "languagetool"
                }
                corrections.append(correction)
            
            return corrections
            
        except Exception as e:
            self.logger.error(f"LanguageTool correction failed: {e}")
            return corrections
    
    def _merge_corrections(
        self, 
        original_text: str, 
        t5_corrected: str, 
        lt_corrections: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """Merge corrections from T5 and LanguageTool"""
        merged_corrections = []
        
        # Add LanguageTool corrections (more specific)
        merged_corrections.extend(lt_corrections)
        
        # If T5 produced a different result, analyze the differences
        if t5_corrected != original_text:
            t5_diffs = self._find_text_differences(original_text, t5_corrected)
            
            for diff in t5_diffs:
                # Check if this correction overlaps with existing ones
                if not self._has_overlapping_correction(diff, merged_corrections):
                    correction = {
                        "original": diff["original"],
                        "corrected": diff["corrected"],
                        "error_type": "grammar",
                        "rule_explanation": "Grammar improvement suggested by AI model",
                        "position": diff["position"],
                        "confidence": 0.7,  # Medium confidence for T5
                        "source": "t5"
                    }
                    merged_corrections.append(correction)
        
        # Sort corrections by position
        merged_corrections.sort(key=lambda x: x["position"]["start"])
        
        return merged_corrections
    
    def _find_text_differences(self, original: str, corrected: str) -> List[Dict[str, Any]]:
        """Find differences between original and corrected text"""
        differences = []
        
        # Simple word-by-word comparison
        original_words = original.split()
        corrected_words = corrected.split()
        
        # Basic alignment (this could be improved with proper diff algorithm)
        min_len = min(len(original_words), len(corrected_words))
        
        for i in range(min_len):
            if original_words[i] != corrected_words[i]:
                # Find position in original text
                position_start = len(" ".join(original_words[:i]))
                if i > 0:
                    position_start += 1  # Add space
                
                differences.append({
                    "original": original_words[i],
                    "corrected": corrected_words[i],
                    "position": {
                        "start": position_start,
                        "end": position_start + len(original_words[i])
                    }
                })
        
        return differences
    
    def _has_overlapping_correction(
        self, 
        new_correction: Dict[str, Any], 
        existing_corrections: List[Dict[str, Any]]
    ) -> bool:
        """Check if a correction overlaps with existing ones"""
        new_start = new_correction["position"]["start"]
        new_end = new_correction["position"]["end"]
        
        for existing in existing_corrections:
            existing_start = existing["position"]["start"]
            existing_end = existing["position"]["end"]
            
            # Check for overlap
            if (new_start < existing_end and new_end > existing_start):
                return True
        
        return False
    
    def _apply_corrections(self, text: str, corrections: List[Dict[str, Any]]) -> str:
        """Apply corrections to text"""
        if not corrections:
            return text
        
        # Sort corrections by position (reverse order to maintain positions)
        sorted_corrections = sorted(corrections, key=lambda x: x["position"]["start"], reverse=True)
        
        corrected_text = text
        
        for correction in sorted_corrections:
            start = correction["position"]["start"]
            end = correction["position"]["end"]
            replacement = correction["corrected"]
            
            # Apply correction
            corrected_text = corrected_text[:start] + replacement + corrected_text[end:]
        
        return corrected_text
    
    def _categorize_error_type(self, rule_id: str, category: str) -> str:
        """Categorize error type based on LanguageTool rule"""
        rule_id_lower = rule_id.lower()
        category_lower = category.lower()
        
        if "spell" in rule_id_lower or "spell" in category_lower:
            return "spelling"
        elif "grammar" in category_lower or "agreement" in rule_id_lower:
            return "grammar"
        elif "punct" in rule_id_lower or "punct" in category_lower:
            return "punctuation"
        elif "capital" in rule_id_lower or "capital" in category_lower:
            return "capitalization"
        elif "article" in rule_id_lower:
            return "article_usage"
        elif "preposition" in rule_id_lower:
            return "preposition_usage"
        elif "tense" in rule_id_lower:
            return "verb_tense"
        else:
            return "grammar"
    
    def _calculate_match_confidence(self, match) -> float:
        """Calculate confidence score for LanguageTool match"""
        # Base confidence
        confidence = 0.8
        
        # Adjust based on rule category
        if hasattr(match, 'category'):
            if match.category == "GRAMMAR":
                confidence = 0.9
            elif match.category == "TYPOS":
                confidence = 0.95
            elif match.category == "STYLE":
                confidence = 0.6
        
        # Adjust based on number of suggestions
        if hasattr(match, 'replacements') and match.replacements:
            if len(match.replacements) == 1:
                confidence += 0.1
            elif len(match.replacements) > 3:
                confidence -= 0.1
        
        return min(1.0, max(0.1, confidence))
    
    def _generate_correction_explanation(
        self, 
        original: str, 
        corrected: str, 
        corrections: List[Dict[str, Any]]
    ) -> str:
        """Generate explanation for corrections"""
        if not corrections:
            return "No corrections needed. The text appears to be grammatically correct."
        
        explanations = []
        
        # Count error types
        error_counts = {}
        for correction in corrections:
            error_type = correction["error_type"]
            error_counts[error_type] = error_counts.get(error_type, 0) + 1
        
        # Generate summary
        total_corrections = len(corrections)
        explanations.append(f"Found {total_corrections} correction(s)")
        
        # Describe error types
        for error_type, count in error_counts.items():
            if count == 1:
                explanations.append(f"1 {error_type} error")
            else:
                explanations.append(f"{count} {error_type} errors")
        
        return ". ".join(explanations) + "."
    
    def _extract_grammar_rules(self, corrections: List[Dict[str, Any]]) -> List[str]:
        """Extract grammar rules from corrections"""
        rules = set()
        
        for correction in corrections:
            error_type = correction["error_type"]
            if error_type in self.grammar_rules:
                rules.add(self.grammar_rules[error_type])
            
            # Add specific rule explanation if available
            rule_explanation = correction.get("rule_explanation", "")
            if rule_explanation and len(rule_explanation) < 100:
                rules.add(rule_explanation)
        
        return list(rules)
    
    def _generate_correction_examples(self, corrections: List[Dict[str, Any]]) -> List[str]:
        """Generate examples based on corrections"""
        examples = []
        
        for correction in corrections[:3]:  # Limit to 3 examples
            original = correction["original"]
            corrected = correction["corrected"]
            
            if original and corrected and original != corrected:
                example = f"'{original}' → '{corrected}'"
                examples.append(example)
        
        return examples
    
    def _get_error_type_tags(self, corrections: List[Dict[str, Any]]) -> List[str]:
        """Get tags based on error types"""
        tags = set()
        
        for correction in corrections:
            error_type = correction["error_type"]
            tags.add(error_type)
        
        return list(tags)
    
    def _calculate_confidence_score(self, corrections: List[Dict[str, Any]]) -> float:
        """Calculate overall confidence score for corrections"""
        if not corrections:
            return 1.0  # High confidence when no corrections needed
        
        # Average confidence of all corrections
        total_confidence = sum(correction.get("confidence", 0.5) for correction in corrections)
        return total_confidence / len(corrections)
    
    def health_check(self) -> Dict[str, Any]:
        """Perform health check on correction agent"""
        try:
            # Check T5 model
            t5_health = self.model_manager.health_check(self.grammar_model_key)
            
            # Check LanguageTool
            language_tool = self.model_manager.get_language_tool()
            lt_available = language_tool is not None
            
            return {
                "status": "healthy" if (t5_health["status"] == "healthy" or lt_available) else "degraded",
                "t5_model": t5_health["status"],
                "languagetool": "available" if lt_available else "unavailable",
                "correction_methods": ["t5", "languagetool"] if lt_available else ["t5"]
            }
            
        except Exception as e:
            return {
                "status": "error",
                "message": str(e)
            }