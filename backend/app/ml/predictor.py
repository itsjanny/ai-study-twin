import os
import joblib
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import Ridge

MODEL_PATH = os.path.join(os.path.dirname(__file__), "models", "score_predictor.joblib")

class QuizScorePredictor:
    """
    Model 2: Quiz Score Predictor
    Predicts expected student percentage (0-100%) on an upcoming quiz.
    """
    def __init__(self):
        self.model = None
        self.load_or_create_model()

    def load_or_create_model(self):
        if os.path.exists(MODEL_PATH):
            try:
                self.model = joblib.load(MODEL_PATH)
                return
            except Exception:
                pass
        
        # Fallback default model trained on baseline synthetic student dataset
        X_dummy = np.array([
            [1, 50.0, 50.0, 50.0, 0, 5.0, 3],
            [3, 85.0, 90.0, 82.0, 2, 1.0, 2],
            [5, 40.0, 35.0, 42.0, 1, 10.0, 4],
            [2, 70.0, 75.0, 68.0, 1, 2.0, 3],
            [4, 95.0, 92.0, 94.0, 3, 0.5, 1],
            [2, 30.0, 25.0, 35.0, 0, 14.0, 5],
        ])
        y_dummy = np.array([52.0, 87.0, 38.0, 72.0, 93.0, 28.0])

        model = RandomForestRegressor(n_estimators=50, random_state=42)
        model.fit(X_dummy, y_dummy)
        self.model = model

    def predict_score(
        self,
        attempts: int,
        topic_accuracy: float,
        recent_score: float,
        overall_avg: float,
        revision_count: int,
        days_since_last_study: float,
        difficulty_level: int
    ) -> float:
        """
        Predicts quiz score percentage.
        """
        features = np.array([[
            attempts,
            topic_accuracy,
            recent_score,
            overall_avg,
            revision_count,
            days_since_last_study,
            difficulty_level
        ]])

        if self.model is not None:
            try:
                pred = float(self.model.predict(features)[0])
                return round(max(10.0, min(98.0, pred)), 1)
            except Exception:
                pass

        # Robust heuristic prediction
        base = (recent_score * 0.4) + (topic_accuracy * 0.4) + (overall_avg * 0.2)
        decay = min(15.0, days_since_last_study * 0.8)
        rev_boost = min(10.0, revision_count * 2.5)
        diff_penalty = (difficulty_level - 3) * 3.0
        
        calculated_pred = base - decay + rev_boost - diff_penalty
        return round(max(15.0, min(98.0, calculated_pred)), 1)

score_predictor = QuizScorePredictor()
