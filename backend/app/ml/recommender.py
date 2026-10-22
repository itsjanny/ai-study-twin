import datetime
from typing import List, Dict

class RecommendationEngine:
    """
    Model 3: Hybrid Recommendation Engine
    Calculates dynamic priority ranking and tailored revision requirements.
    """
    @staticmethod
    def calculate_priority_score(
        weakness_score: float,
        days_since_last_study: float,
        difficulty_level: int,
        importance_weight: float,
        prereq_mastered: bool = True
    ) -> float:
        """
        Higher score = higher priority to study next.
        """
        # Weakness component (0-100)
        w_factor = weakness_score * 0.45
        
        # Time decay (forgetting curve): +1.5 points per day unstudied (max +30)
        time_factor = min(30.0, days_since_last_study * 1.5)
        
        # Importance & Difficulty
        diff_factor = difficulty_level * 3.0
        imp_factor = importance_weight * 10.0
        
        # Prerequisite bonus: if prereq not mastered, reduce priority for current topic
        prereq_multiplier = 1.0 if prereq_mastered else 0.5
        
        priority = (w_factor + time_factor + diff_factor + imp_factor) * prereq_multiplier
        return round(priority, 1)

    @staticmethod
    def calculate_revision_requirement(status_label: str, days_since_last_study: float) -> dict:
        """
        Determines revision urgency level & recommended minutes.
        """
        if status_label == "Very Weak" or days_since_last_study > 14:
            return {
                "revision_required": "High (Intensive)",
                "recommended_minutes": 45,
                "action": "Deep conceptual review + 10 practice MCQs"
            }
        elif status_label == "Weak" or days_since_last_study > 7:
            return {
                "revision_required": "Medium (Focused)",
                "recommended_minutes": 30,
                "action": "Targeted formula/concept revision + practice quiz"
            }
        elif status_label == "Average":
            return {
                "revision_required": "Moderate",
                "recommended_minutes": 20,
                "action": "Quick refresher notes + 5 practice questions"
            }
        else: # Strong
            return {
                "revision_required": "Light Maintenance",
                "recommended_minutes": 10,
                "action": "Flashcards review to retain mastery"
            }

recommender_engine = RecommendationEngine()
