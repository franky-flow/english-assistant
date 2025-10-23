"""
Phrasal Verb Agent for English Assistant
Handles phrasal verb management, filtering, and progress tracking
"""
import logging
from datetime import datetime
from typing import Dict, List, Optional, Any
import json

from models.api_models import (
    PhrasalVerb, PhrasalVerbFilters, PhrasalVerbUpdateRequest, 
    PhrasalVerbProgress
)
from utils.response_formatter import DataTransformer
from utils.error_handler import ModelErrorHandler


class PhrasalVerbAgent:
    """Agent for phrasal verb operations and progress tracking"""
    
    def __init__(self):
        self.logger = logging.getLogger("phrasal_verb_agent")
        
        # In-memory phrasal verb database (would be replaced with actual DB)
        self.phrasal_verbs_data = self._initialize_phrasal_verbs()
        
        # Progress tracking
        self.user_progress = {}
    
    def _initialize_phrasal_verbs(self) -> List[Dict[str, Any]]:
        """Initialize phrasal verbs database with common phrasal verbs"""
        return [
            {
                "id": 1,
                "verb": "break down",
                "definition": "to stop working (machine); to lose control emotionally",
                "examples": [
                    "My car broke down on the highway",
                    "She broke down when she heard the news"
                ],
                "difficulty": "beginner",
                "status": "pending",
                "progress": {
                    "attempts": 0,
                    "correct_answers": 0,
                    "last_practiced": None,
                    "mastery_level": 0.0
                }
            },
            {
                "id": 2,
                "verb": "bring up",
                "definition": "to mention a topic; to raise a child",
                "examples": [
                    "Don't bring up that subject again",
                    "She was brought up by her grandmother"
                ],
                "difficulty": "beginner",
                "status": "pending",
                "progress": {
                    "attempts": 0,
                    "correct_answers": 0,
                    "last_practiced": None,
                    "mastery_level": 0.0
                }
            },
            {
                "id": 3,
                "verb": "call off",
                "definition": "to cancel something",
                "examples": [
                    "They called off the meeting due to bad weather",
                    "The wedding was called off at the last minute"
                ],
                "difficulty": "beginner",
                "status": "pending",
                "progress": {
                    "attempts": 0,
                    "correct_answers": 0,
                    "last_practiced": None,
                    "mastery_level": 0.0
                }
            },
            {
                "id": 4,
                "verb": "come across",
                "definition": "to find by chance; to seem or appear",
                "examples": [
                    "I came across an old photo while cleaning",
                    "He comes across as very confident"
                ],
                "difficulty": "intermediate",
                "status": "pending",
                "progress": {
                    "attempts": 0,
                    "correct_answers": 0,
                    "last_practiced": None,
                    "mastery_level": 0.0
                }
            },
            {
                "id": 5,
                "verb": "cut down on",
                "definition": "to reduce the amount of something",
                "examples": [
                    "I need to cut down on sugar",
                    "The company is cutting down on expenses"
                ],
                "difficulty": "intermediate",
                "status": "pending",
                "progress": {
                    "attempts": 0,
                    "correct_answers": 0,
                    "last_practiced": None,
                    "mastery_level": 0.0
                }
            },
            {
                "id": 6,
                "verb": "figure out",
                "definition": "to understand or solve something",
                "examples": [
                    "I can't figure out this math problem",
                    "We need to figure out what went wrong"
                ],
                "difficulty": "beginner",
                "status": "pending",
                "progress": {
                    "attempts": 0,
                    "correct_answers": 0,
                    "last_practiced": None,
                    "mastery_level": 0.0
                }
            },
            {
                "id": 7,
                "verb": "get along with",
                "definition": "to have a good relationship with someone",
                "examples": [
                    "I get along well with my coworkers",
                    "Do you get along with your neighbors?"
                ],
                "difficulty": "intermediate",
                "status": "pending",
                "progress": {
                    "attempts": 0,
                    "correct_answers": 0,
                    "last_practiced": None,
                    "mastery_level": 0.0
                }
            },
            {
                "id": 8,
                "verb": "give up",
                "definition": "to stop trying; to quit",
                "examples": [
                    "Don't give up on your dreams",
                    "I gave up smoking last year"
                ],
                "difficulty": "beginner",
                "status": "pending",
                "progress": {
                    "attempts": 0,
                    "correct_answers": 0,
                    "last_practiced": None,
                    "mastery_level": 0.0
                }
            },
            {
                "id": 9,
                "verb": "look forward to",
                "definition": "to anticipate with pleasure",
                "examples": [
                    "I'm looking forward to the weekend",
                    "We look forward to hearing from you"
                ],
                "difficulty": "intermediate",
                "status": "pending",
                "progress": {
                    "attempts": 0,
                    "correct_answers": 0,
                    "last_practiced": None,
                    "mastery_level": 0.0
                }
            },
            {
                "id": 10,
                "verb": "put off",
                "definition": "to postpone or delay",
                "examples": [
                    "Don't put off until tomorrow what you can do today",
                    "The meeting was put off until next week"
                ],
                "difficulty": "intermediate",
                "status": "pending",
                "progress": {
                    "attempts": 0,
                    "correct_answers": 0,
                    "last_practiced": None,
                    "mastery_level": 0.0
                }
            },
            {
                "id": 11,
                "verb": "run into",
                "definition": "to meet by chance; to encounter a problem",
                "examples": [
                    "I ran into my old teacher at the store",
                    "We ran into some technical difficulties"
                ],
                "difficulty": "intermediate",
                "status": "pending",
                "progress": {
                    "attempts": 0,
                    "correct_answers": 0,
                    "last_practiced": None,
                    "mastery_level": 0.0
                }
            },
            {
                "id": 12,
                "verb": "turn down",
                "definition": "to refuse; to reduce volume or intensity",
                "examples": [
                    "She turned down the job offer",
                    "Please turn down the music"
                ],
                "difficulty": "beginner",
                "status": "pending",
                "progress": {
                    "attempts": 0,
                    "correct_answers": 0,
                    "last_practiced": None,
                    "mastery_level": 0.0
                }
            },
            {
                "id": 13,
                "verb": "work out",
                "definition": "to exercise; to solve or develop successfully",
                "examples": [
                    "I work out at the gym three times a week",
                    "I hope everything works out for you"
                ],
                "difficulty": "beginner",
                "status": "pending",
                "progress": {
                    "attempts": 0,
                    "correct_answers": 0,
                    "last_practiced": None,
                    "mastery_level": 0.0
                }
            },
            {
                "id": 14,
                "verb": "keep up with",
                "definition": "to maintain the same pace; to stay informed about",
                "examples": [
                    "I can't keep up with the fast pace",
                    "It's hard to keep up with technology"
                ],
                "difficulty": "advanced",
                "status": "pending",
                "progress": {
                    "attempts": 0,
                    "correct_answers": 0,
                    "last_practiced": None,
                    "mastery_level": 0.0
                }
            },
            {
                "id": 15,
                "verb": "take after",
                "definition": "to resemble a family member in appearance or behavior",
                "examples": [
                    "She takes after her mother in looks",
                    "He takes after his father's personality"
                ],
                "difficulty": "advanced",
                "status": "pending",
                "progress": {
                    "attempts": 0,
                    "correct_answers": 0,
                    "last_practiced": None,
                    "mastery_level": 0.0
                }
            }
        ]
    
    async def get_phrasal_verbs(self, filters: PhrasalVerbFilters) -> List[PhrasalVerb]:
        """
        Get phrasal verbs with filtering and sorting
        
        Args:
            filters: PhrasalVerbFilters with search and filter criteria
            
        Returns:
            List of PhrasalVerb objects matching the criteria
        """
        try:
            self.logger.info(f"Getting phrasal verbs with filters: {filters}")
            
            # Start with all phrasal verbs
            filtered_verbs = self.phrasal_verbs_data.copy()
            
            # Apply filters
            if filters.difficulty:
                filtered_verbs = [
                    verb for verb in filtered_verbs 
                    if verb["difficulty"] == filters.difficulty
                ]
            
            if filters.status:
                filtered_verbs = [
                    verb for verb in filtered_verbs 
                    if verb["status"] == filters.status
                ]
            
            if filters.search:
                search_term = filters.search.lower()
                filtered_verbs = [
                    verb for verb in filtered_verbs
                    if (search_term in verb["verb"].lower() or 
                        search_term in verb["definition"].lower())
                ]
            
            # Sort by verb name (alphabetical)
            filtered_verbs.sort(key=lambda x: x["verb"])
            
            # Apply pagination
            start_idx = filters.offset
            end_idx = start_idx + filters.limit
            paginated_verbs = filtered_verbs[start_idx:end_idx]
            
            # Convert to PhrasalVerb objects
            result = []
            for verb_data in paginated_verbs:
                progress = PhrasalVerbProgress(**verb_data["progress"])
                phrasal_verb = PhrasalVerb(
                    id=verb_data["id"],
                    verb=verb_data["verb"],
                    definition=verb_data["definition"],
                    examples=verb_data["examples"],
                    difficulty=verb_data["difficulty"],
                    status=verb_data["status"],
                    progress=progress,
                    created_at=datetime.now(),
                    updated_at=datetime.now()
                )
                result.append(phrasal_verb)
            
            self.logger.info(f"Returning {len(result)} phrasal verbs")
            return result
            
        except Exception as e:
            self.logger.error(f"Error getting phrasal verbs: {e}")
            error_response = ModelErrorHandler.handle_inference_error("PhrasalVerbAgent", e)
            raise Exception(error_response.message)
    
    async def update_phrasal_verb_progress(
        self, 
        verb_id: int, 
        update_request: PhrasalVerbUpdateRequest
    ) -> PhrasalVerb:
        """
        Update progress for a specific phrasal verb
        
        Args:
            verb_id: ID of the phrasal verb to update
            update_request: Progress update data
            
        Returns:
            Updated PhrasalVerb object
        """
        try:
            self.logger.info(f"Updating progress for phrasal verb ID: {verb_id}")
            
            # Find the phrasal verb
            verb_data = None
            for verb in self.phrasal_verbs_data:
                if verb["id"] == verb_id:
                    verb_data = verb
                    break
            
            if not verb_data:
                raise ValueError(f"Phrasal verb with ID {verb_id} not found")
            
            # Update status
            verb_data["status"] = update_request.status
            
            # Update progress if provided
            if update_request.progress:
                verb_data["progress"].update(update_request.progress.dict())
                verb_data["progress"]["last_practiced"] = datetime.now().isoformat()
            
            # Auto-calculate mastery level based on performance
            if verb_data["progress"]["attempts"] > 0:
                accuracy = verb_data["progress"]["correct_answers"] / verb_data["progress"]["attempts"]
                verb_data["progress"]["mastery_level"] = min(1.0, accuracy)
            
            # Auto-update status based on mastery level
            mastery = verb_data["progress"]["mastery_level"]
            if mastery >= 0.8 and verb_data["progress"]["attempts"] >= 3:
                verb_data["status"] = "learned"
            elif mastery >= 0.5 or verb_data["progress"]["attempts"] > 0:
                verb_data["status"] = "in_progress"
            
            # Convert to PhrasalVerb object
            progress = PhrasalVerbProgress(**verb_data["progress"])
            updated_verb = PhrasalVerb(
                id=verb_data["id"],
                verb=verb_data["verb"],
                definition=verb_data["definition"],
                examples=verb_data["examples"],
                difficulty=verb_data["difficulty"],
                status=verb_data["status"],
                progress=progress,
                created_at=datetime.now(),
                updated_at=datetime.now()
            )
            
            self.logger.info(f"Updated phrasal verb {verb_id} to status: {verb_data['status']}")
            return updated_verb
            
        except Exception as e:
            self.logger.error(f"Error updating phrasal verb progress: {e}")
            error_response = ModelErrorHandler.handle_inference_error("PhrasalVerbAgent", e)
            raise Exception(error_response.message)
    
    async def get_phrasal_verb_by_id(self, verb_id: int) -> Optional[PhrasalVerb]:
        """Get a specific phrasal verb by ID"""
        try:
            for verb_data in self.phrasal_verbs_data:
                if verb_data["id"] == verb_id:
                    progress = PhrasalVerbProgress(**verb_data["progress"])
                    return PhrasalVerb(
                        id=verb_data["id"],
                        verb=verb_data["verb"],
                        definition=verb_data["definition"],
                        examples=verb_data["examples"],
                        difficulty=verb_data["difficulty"],
                        status=verb_data["status"],
                        progress=progress,
                        created_at=datetime.now(),
                        updated_at=datetime.now()
                    )
            return None
            
        except Exception as e:
            self.logger.error(f"Error getting phrasal verb by ID: {e}")
            return None
    
    def get_progress_statistics(self) -> Dict[str, Any]:
        """Get overall progress statistics"""
        try:
            total_verbs = len(self.phrasal_verbs_data)
            
            status_counts = {"pending": 0, "in_progress": 0, "learned": 0}
            difficulty_counts = {"beginner": 0, "intermediate": 0, "advanced": 0}
            
            total_attempts = 0
            total_correct = 0
            
            for verb in self.phrasal_verbs_data:
                status_counts[verb["status"]] += 1
                difficulty_counts[verb["difficulty"]] += 1
                
                total_attempts += verb["progress"]["attempts"]
                total_correct += verb["progress"]["correct_answers"]
            
            overall_accuracy = (total_correct / total_attempts) if total_attempts > 0 else 0
            
            return {
                "total_phrasal_verbs": total_verbs,
                "status_distribution": status_counts,
                "difficulty_distribution": difficulty_counts,
                "overall_accuracy": round(overall_accuracy, 2),
                "total_attempts": total_attempts,
                "total_correct_answers": total_correct,
                "completion_percentage": round((status_counts["learned"] / total_verbs) * 100, 1)
            }
            
        except Exception as e:
            self.logger.error(f"Error getting progress statistics: {e}")
            return {}
    
    def get_recommended_verbs(self, limit: int = 5) -> List[PhrasalVerb]:
        """Get recommended phrasal verbs for practice"""
        try:
            # Prioritize verbs that need practice
            recommendations = []
            
            # Sort by priority: pending > in_progress with low mastery > not practiced recently
            for verb_data in self.phrasal_verbs_data:
                priority_score = 0
                
                # Status priority
                if verb_data["status"] == "pending":
                    priority_score += 10
                elif verb_data["status"] == "in_progress":
                    priority_score += 5
                
                # Mastery level (lower is higher priority)
                mastery = verb_data["progress"]["mastery_level"]
                priority_score += (1.0 - mastery) * 5
                
                # Difficulty (beginner gets higher priority)
                if verb_data["difficulty"] == "beginner":
                    priority_score += 3
                elif verb_data["difficulty"] == "intermediate":
                    priority_score += 2
                
                # Add to recommendations with score
                progress = PhrasalVerbProgress(**verb_data["progress"])
                phrasal_verb = PhrasalVerb(
                    id=verb_data["id"],
                    verb=verb_data["verb"],
                    definition=verb_data["definition"],
                    examples=verb_data["examples"],
                    difficulty=verb_data["difficulty"],
                    status=verb_data["status"],
                    progress=progress,
                    created_at=datetime.now(),
                    updated_at=datetime.now()
                )
                
                recommendations.append((priority_score, phrasal_verb))
            
            # Sort by priority score (descending) and return top results
            recommendations.sort(key=lambda x: x[0], reverse=True)
            return [verb for _, verb in recommendations[:limit]]
            
        except Exception as e:
            self.logger.error(f"Error getting recommended verbs: {e}")
            return []
    
    def search_phrasal_verbs(self, query: str) -> List[PhrasalVerb]:
        """Search phrasal verbs by query"""
        try:
            query_lower = query.lower()
            results = []
            
            for verb_data in self.phrasal_verbs_data:
                # Search in verb, definition, and examples
                if (query_lower in verb_data["verb"].lower() or
                    query_lower in verb_data["definition"].lower() or
                    any(query_lower in example.lower() for example in verb_data["examples"])):
                    
                    progress = PhrasalVerbProgress(**verb_data["progress"])
                    phrasal_verb = PhrasalVerb(
                        id=verb_data["id"],
                        verb=verb_data["verb"],
                        definition=verb_data["definition"],
                        examples=verb_data["examples"],
                        difficulty=verb_data["difficulty"],
                        status=verb_data["status"],
                        progress=progress,
                        created_at=datetime.now(),
                        updated_at=datetime.now()
                    )
                    results.append(phrasal_verb)
            
            return results
            
        except Exception as e:
            self.logger.error(f"Error searching phrasal verbs: {e}")
            return []
    
    def get_available_difficulties(self) -> List[str]:
        """Get list of available difficulty levels"""
        return ["beginner", "intermediate", "advanced"]
    
    def get_available_statuses(self) -> List[str]:
        """Get list of available status values"""
        return ["pending", "in_progress", "learned"]
    
    def health_check(self) -> Dict[str, Any]:
        """Perform health check on phrasal verb agent"""
        try:
            total_verbs = len(self.phrasal_verbs_data)
            
            return {
                "status": "healthy",
                "total_phrasal_verbs": total_verbs,
                "available_difficulties": self.get_available_difficulties(),
                "available_statuses": self.get_available_statuses(),
                "data_source": "in_memory"  # Would be "database" in production
            }
            
        except Exception as e:
            return {
                "status": "error",
                "message": str(e)
            }