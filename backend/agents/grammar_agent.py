"""
Grammar Agent for English Assistant
Handles grammar explanations and word comparisons
"""
import logging
import re
from typing import Dict, List, Optional, Tuple, Any

from models.api_models import GrammarRequest, GrammarResponse
from utils.model_manager import get_model_manager
from utils.response_formatter import ResponseFormatter, DataTransformer
from utils.error_handler import ModelErrorHandler


class GrammarAgent:
    """Agent for grammar explanations and word comparisons"""
    
    def __init__(self):
        self.logger = logging.getLogger("grammar_agent")
        self.model_manager = get_model_manager()
        
        # Grammar knowledge base
        self.grammar_rules = {
            "articles": {
                "category": "Articles",
                "description": "Usage of a, an, and the",
                "rules": [
                    "Use 'a' before consonant sounds",
                    "Use 'an' before vowel sounds", 
                    "Use 'the' for specific nouns"
                ],
                "examples": [
                    "a book, an apple, the sun",
                    "a university (consonant sound), an hour (vowel sound)"
                ]
            },
            "verb_tenses": {
                "category": "Verb Tenses",
                "description": "Present, past, and future tenses",
                "rules": [
                    "Present simple: I work",
                    "Past simple: I worked",
                    "Future simple: I will work"
                ],
                "examples": [
                    "I eat breakfast every day (present)",
                    "I ate breakfast yesterday (past)",
                    "I will eat breakfast tomorrow (future)"
                ]
            },
            "prepositions": {
                "category": "Prepositions",
                "description": "Words that show relationships between nouns",
                "rules": [
                    "in, on, at for time and place",
                    "by, with, for purpose and method"
                ],
                "examples": [
                    "in the morning, on Monday, at 3 o'clock",
                    "go by car, write with a pen, study for exams"
                ]
            },
            "subject_verb_agreement": {
                "category": "Subject-Verb Agreement",
                "description": "Subjects and verbs must agree in number",
                "rules": [
                    "Singular subjects take singular verbs",
                    "Plural subjects take plural verbs"
                ],
                "examples": [
                    "The cat runs (singular)",
                    "The cats run (plural)"
                ]
            },
            "conditionals": {
                "category": "Conditional Sentences",
                "description": "If-then statements and hypothetical situations",
                "rules": [
                    "First conditional: If + present, will + base verb",
                    "Second conditional: If + past, would + base verb"
                ],
                "examples": [
                    "If it rains, I will stay home",
                    "If I had money, I would travel"
                ]
            },
            "modal_verbs": {
                "category": "Modal Verbs",
                "description": "Can, could, should, must, might, may, will, would",
                "rules": [
                    "Express ability, possibility, permission, obligation",
                    "Followed by base form of verb"
                ],
                "examples": [
                    "I can swim (ability)",
                    "You should study (advice)",
                    "It might rain (possibility)"
                ]
            }
        }
        
        # Common word comparisons
        self.word_comparisons = {
            ("affect", "effect"): {
                "affect": "verb - to influence something",
                "effect": "noun - a result or consequence",
                "examples": [
                    "The rain will affect our plans (verb)",
                    "The effect of rain was cancelled plans (noun)"
                ]
            },
            ("accept", "except"): {
                "accept": "verb - to receive or agree to",
                "except": "preposition - excluding, but not",
                "examples": [
                    "I accept your invitation (verb)",
                    "Everyone came except John (preposition)"
                ]
            },
            ("advice", "advise"): {
                "advice": "noun - suggestions or recommendations",
                "advise": "verb - to give suggestions",
                "examples": [
                    "Your advice is helpful (noun)",
                    "I advise you to study (verb)"
                ]
            },
            ("lose", "loose"): {
                "lose": "verb - to misplace or not win",
                "loose": "adjective - not tight",
                "examples": [
                    "Don't lose your keys (verb)",
                    "This shirt is too loose (adjective)"
                ]
            },
            ("then", "than"): {
                "then": "adverb - at that time, next",
                "than": "conjunction - used in comparisons",
                "examples": [
                    "First eat, then sleep (sequence)",
                    "She is taller than me (comparison)"
                ]
            }
        }
    
    async def explain_grammar(self, request: GrammarRequest) -> GrammarResponse:
        """
        Explain grammar rules or compare words
        
        Args:
            request: GrammarRequest with question and type
            
        Returns:
            GrammarResponse with explanations and examples
        """
        try:
            self.logger.info(f"Processing grammar request: {request.question}")
            
            # Clean and validate input
            question = DataTransformer.clean_text(request.question)
            if not question:
                raise ValueError("Empty question after cleaning")
            
            # Determine response based on question type
            if request.question_type == "comparison":
                response_data = self._handle_word_comparison(question)
            elif request.question_type == "usage":
                response_data = self._handle_usage_question(question)
            else:  # explanation
                response_data = self._handle_grammar_explanation(question)
            
            # Generate tags
            tags = DataTransformer.extract_tags(question, "grammar")
            tags.extend([request.question_type, response_data["rule_category"].lower().replace(" ", "_")])
            
            # Format response
            return ResponseFormatter.format_grammar_response(
                query=request.question,
                result=response_data["result"],
                rule_category=response_data["rule_category"],
                explanation=response_data["explanation"],
                examples=response_data["examples"],
                tags=list(set(tags)),
                related_concepts=response_data.get("related_concepts", []),
                difficulty_level=response_data.get("difficulty_level", "intermediate"),
                common_mistakes=response_data.get("common_mistakes", [])
            )
            
        except Exception as e:
            self.logger.error(f"Error in grammar explanation: {e}")
            error_response = ModelErrorHandler.handle_inference_error("GrammarAgent", e)
            raise Exception(error_response.message)
    
    def _handle_word_comparison(self, question: str) -> Dict[str, Any]:
        """Handle word comparison questions"""
        # Extract words to compare
        words = self._extract_comparison_words(question)
        
        if len(words) >= 2:
            # Check if we have a predefined comparison
            word_pair = tuple(sorted(words[:2]))
            
            for comparison_key, comparison_data in self.word_comparisons.items():
                if set(comparison_key) == set(word_pair):
                    return {
                        "result": f"Comparison between '{words[0]}' and '{words[1]}'",
                        "rule_category": "Word Usage",
                        "explanation": self._format_word_comparison(comparison_data),
                        "examples": comparison_data["examples"],
                        "related_concepts": ["vocabulary", "word_choice"],
                        "difficulty_level": "intermediate"
                    }
            
            # Generic comparison if not predefined
            return self._generate_generic_comparison(words[0], words[1])
        
        # If no clear comparison found
        return {
            "result": "Please specify two words to compare",
            "rule_category": "Word Comparison",
            "explanation": "To compare words, please ask something like 'What's the difference between X and Y?'",
            "examples": ["What's the difference between 'affect' and 'effect'?"],
            "related_concepts": ["vocabulary"],
            "difficulty_level": "beginner"
        }
    
    def _handle_usage_question(self, question: str) -> Dict[str, Any]:
        """Handle usage questions"""
        # Look for specific grammar topics in the question
        question_lower = question.lower()
        
        # Check for specific grammar topics
        for topic_key, topic_data in self.grammar_rules.items():
            topic_keywords = topic_key.split("_") + [topic_data["category"].lower()]
            
            if any(keyword in question_lower for keyword in topic_keywords):
                return {
                    "result": f"Usage of {topic_data['category']}",
                    "rule_category": topic_data["category"],
                    "explanation": topic_data["description"],
                    "examples": topic_data["examples"],
                    "related_concepts": self._get_related_concepts(topic_key),
                    "difficulty_level": self._determine_difficulty(topic_key),
                    "common_mistakes": self._get_common_mistakes(topic_key)
                }
        
        # Generic usage response
        return self._generate_generic_usage_response(question)
    
    def _handle_grammar_explanation(self, question: str) -> Dict[str, Any]:
        """Handle general grammar explanation questions"""
        question_lower = question.lower()
        
        # Look for grammar topics
        for topic_key, topic_data in self.grammar_rules.items():
            topic_keywords = topic_key.split("_") + [topic_data["category"].lower()]
            
            if any(keyword in question_lower for keyword in topic_keywords):
                return {
                    "result": f"Explanation of {topic_data['category']}",
                    "rule_category": topic_data["category"],
                    "explanation": self._format_grammar_explanation(topic_data),
                    "examples": topic_data["examples"],
                    "related_concepts": self._get_related_concepts(topic_key),
                    "difficulty_level": self._determine_difficulty(topic_key),
                    "common_mistakes": self._get_common_mistakes(topic_key)
                }
        
        # Use LanguageTool for additional analysis if available
        lt_analysis = self._analyze_with_languagetool(question)
        if lt_analysis:
            return lt_analysis
        
        # Generic grammar response
        return self._generate_generic_grammar_response(question)
    
    def _extract_comparison_words(self, question: str) -> List[str]:
        """Extract words to compare from question"""
        # Common comparison patterns
        patterns = [
            r"difference between ['\"]?(\w+)['\"]? and ['\"]?(\w+)['\"]?",
            r"['\"]?(\w+)['\"]? (?:vs|versus) ['\"]?(\w+)['\"]?",
            r"['\"]?(\w+)['\"]? or ['\"]?(\w+)['\"]?",
            r"compare ['\"]?(\w+)['\"]? (?:and|with) ['\"]?(\w+)['\"]?"
        ]
        
        for pattern in patterns:
            match = re.search(pattern, question.lower())
            if match:
                return list(match.groups())
        
        # Fallback: look for quoted words
        quoted_words = re.findall(r"['\"](\w+)['\"]", question)
        if len(quoted_words) >= 2:
            return quoted_words[:2]
        
        return []
    
    def _format_word_comparison(self, comparison_data: Dict[str, Any]) -> str:
        """Format word comparison explanation"""
        explanations = []
        
        for word, definition in comparison_data.items():
            if word != "examples":
                explanations.append(f"'{word}': {definition}")
        
        return ". ".join(explanations) + "."
    
    def _generate_generic_comparison(self, word1: str, word2: str) -> Dict[str, Any]:
        """Generate generic comparison for unknown word pairs"""
        return {
            "result": f"Comparison between '{word1}' and '{word2}'",
            "rule_category": "Word Usage",
            "explanation": f"'{word1}' and '{word2}' are different words with distinct meanings and uses. Check a dictionary for specific definitions.",
            "examples": [f"Example with '{word1}': [context needed]", f"Example with '{word2}': [context needed]"],
            "related_concepts": ["vocabulary", "word_choice"],
            "difficulty_level": "intermediate"
        }
    
    def _generate_generic_usage_response(self, question: str) -> Dict[str, Any]:
        """Generate generic usage response"""
        return {
            "result": "General usage guidance",
            "rule_category": "Usage",
            "explanation": "For specific usage questions, please provide more context or specify the grammar topic you're asking about.",
            "examples": ["How do I use articles?", "When should I use past tense?"],
            "related_concepts": ["grammar_rules"],
            "difficulty_level": "beginner"
        }
    
    def _generate_generic_grammar_response(self, question: str) -> Dict[str, Any]:
        """Generate generic grammar response"""
        return {
            "result": "Grammar explanation",
            "rule_category": "General Grammar",
            "explanation": "English grammar includes many rules for sentence structure, verb tenses, articles, prepositions, and more. Please ask about a specific grammar topic for detailed help.",
            "examples": [
                "Subject-verb agreement: The cat runs",
                "Article usage: a book, an apple, the sun",
                "Verb tenses: I work, I worked, I will work"
            ],
            "related_concepts": ["sentence_structure", "parts_of_speech"],
            "difficulty_level": "beginner"
        }
    
    def _format_grammar_explanation(self, topic_data: Dict[str, Any]) -> str:
        """Format grammar explanation"""
        explanation = topic_data["description"]
        
        if "rules" in topic_data:
            rules_text = ". ".join(topic_data["rules"])
            explanation += f". Key rules: {rules_text}"
        
        return explanation + "."
    
    def _get_related_concepts(self, topic_key: str) -> List[str]:
        """Get related grammar concepts"""
        concept_map = {
            "articles": ["determiners", "noun_phrases"],
            "verb_tenses": ["time_expressions", "aspect"],
            "prepositions": ["phrasal_verbs", "collocations"],
            "subject_verb_agreement": ["number", "person"],
            "conditionals": ["if_clauses", "hypothetical_situations"],
            "modal_verbs": ["auxiliary_verbs", "modality"]
        }
        
        return concept_map.get(topic_key, ["grammar_rules"])
    
    def _determine_difficulty(self, topic_key: str) -> str:
        """Determine difficulty level for grammar topic"""
        difficulty_map = {
            "articles": "intermediate",
            "verb_tenses": "beginner",
            "prepositions": "advanced",
            "subject_verb_agreement": "beginner",
            "conditionals": "advanced",
            "modal_verbs": "intermediate"
        }
        
        return difficulty_map.get(topic_key, "intermediate")
    
    def _get_common_mistakes(self, topic_key: str) -> List[str]:
        """Get common mistakes for grammar topic"""
        mistakes_map = {
            "articles": [
                "Using 'a' before vowel sounds",
                "Omitting 'the' with specific nouns"
            ],
            "verb_tenses": [
                "Mixing past and present tenses",
                "Incorrect past participle forms"
            ],
            "prepositions": [
                "Using wrong preposition with time/place",
                "Literal translation from native language"
            ],
            "subject_verb_agreement": [
                "Singular subject with plural verb",
                "Confusion with collective nouns"
            ],
            "conditionals": [
                "Using 'will' in if-clauses",
                "Mixing conditional types"
            ],
            "modal_verbs": [
                "Adding 'to' after modal verbs",
                "Using wrong modal for context"
            ]
        }
        
        return mistakes_map.get(topic_key, [])
    
    def _analyze_with_languagetool(self, question: str) -> Optional[Dict[str, Any]]:
        """Analyze question with LanguageTool if available"""
        try:
            language_tool = self.model_manager.get_language_tool()
            if language_tool is None:
                return None
            
            # Check if the question itself has grammar issues
            matches = language_tool.check(question)
            
            if matches:
                # If the question has grammar issues, explain them
                return {
                    "result": "Grammar analysis of your question",
                    "rule_category": "Grammar Check",
                    "explanation": f"I found {len(matches)} potential issue(s) in your question. Let me help you with grammar rules.",
                    "examples": [match.message for match in matches[:2]],
                    "related_concepts": ["grammar_checking"],
                    "difficulty_level": "intermediate"
                }
            
            return None
            
        except Exception as e:
            self.logger.error(f"LanguageTool analysis failed: {e}")
            return None
    
    def get_available_topics(self) -> List[str]:
        """Get list of available grammar topics"""
        return list(self.grammar_rules.keys())
    
    def get_word_comparisons(self) -> List[Tuple[str, str]]:
        """Get list of available word comparisons"""
        return list(self.word_comparisons.keys())
    
    def health_check(self) -> Dict[str, Any]:
        """Perform health check on grammar agent"""
        try:
            # Check LanguageTool availability
            language_tool = self.model_manager.get_language_tool()
            lt_available = language_tool is not None
            
            return {
                "status": "healthy",
                "languagetool": "available" if lt_available else "unavailable",
                "grammar_topics": len(self.grammar_rules),
                "word_comparisons": len(self.word_comparisons),
                "available_topics": list(self.grammar_rules.keys())
            }
            
        except Exception as e:
            return {
                "status": "error",
                "message": str(e)
            }