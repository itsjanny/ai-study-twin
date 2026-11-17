import numpy as np

class WeakTopicClassifier:
    """
    Model 1: Weak Topic Classifier
    Rule-based & ML hybrid system to categorize student topic performance.
    """
    @staticmethod
    def classify_topic(accuracy: float, attempts: int, recent_score: float, difficulty_level: int = 3) -> dict:
        """
        Classifies topic into Strong, Average, Weak, Very Weak based on accuracy,
        recency, and difficulty penalty.
        """
        # Weighted accuracy: 60% recent performance + 40% historical accuracy
        if attempts > 0:
            effective_accuracy = (recent_score * 0.6) + (accuracy * 0.4)
        else:
            effective_accuracy = 50.0 # Neutral default for unattempted
            
        # Adjust for difficulty: hard topics get slight leniency
        diff_adjustment = (difficulty_level - 3) * 2.0
        adjusted_score = effective_accuracy + diff_adjustment

        if adjusted_score >= 80.0:
            label = "Strong"
            weakness_score = round(max(0.0, 100.0 - adjusted_score), 1)
            confidence_score = round(min(100.0, adjusted_score), 1)
        elif adjusted_score >= 60.0:
            label = "Average"
            weakness_score = round(100.0 - adjusted_score, 1)
            confidence_score = round(adjusted_score, 1)
        elif adjusted_score >= 40.0:
            label = "Weak"
            weakness_score = round(100.0 - adjusted_score, 1)
            confidence_score = round(adjusted_score, 1)
        else:
            label = "Very Weak"
            weakness_score = round(min(100.0, 100.0 - adjusted_score), 1)
            confidence_score = round(max(5.0, adjusted_score), 1)

        return {
            "label": label,
            "effective_accuracy": round(effective_accuracy, 1),
            "weakness_score": weakness_score,
            "confidence_score": confidence_score
        }

classifier_model = WeakTopicClassifier()
