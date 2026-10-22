import os
import joblib
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier

def train_and_save_models():
    models_dir = os.path.join(os.path.dirname(__file__), "models")
    os.makedirs(models_dir, exist_ok=True)

    print("Training ML Models for AI Study Twin...")

    # 1. Generate Synthetic Training Data for Score Predictor (Model 2)
    np.random.seed(42)
    n_samples = 500

    attempts = np.random.randint(1, 10, n_samples)
    topic_accuracy = np.random.uniform(20.0, 98.0, n_samples)
    recent_score = topic_accuracy + np.random.normal(0, 5, n_samples)
    recent_score = np.clip(recent_score, 10.0, 100.0)
    overall_avg = (topic_accuracy + recent_score) / 2
    revision_count = np.random.randint(0, 5, n_samples)
    days_since_last_study = np.random.uniform(0.1, 20.0, n_samples)
    difficulty_level = np.random.randint(1, 6, n_samples)

    # Calculate target quiz score percentage
    target_score = (
        (recent_score * 0.45) +
        (topic_accuracy * 0.35) +
        (overall_avg * 0.15) +
        (revision_count * 2.0) -
        (days_since_last_study * 0.6) -
        (difficulty_level * 2.5) +
        np.random.normal(0, 3, n_samples)
    )
    target_score = np.clip(target_score, 15.0, 99.0)

    X_train = np.column_stack([
        attempts,
        topic_accuracy,
        recent_score,
        overall_avg,
        revision_count,
        days_since_last_study,
        difficulty_level
    ])

    regressor = RandomForestRegressor(n_estimators=100, max_depth=8, random_state=42)
    regressor.fit(X_train, target_score)

    predictor_path = os.path.join(models_dir, "score_predictor.joblib")
    joblib.dump(regressor, predictor_path)
    print(f"[OK] Saved Score Predictor Model to {predictor_path}")

    # 2. Classifier Model (Model 1)
    # Target: 0 (Very Weak), 1 (Weak), 2 (Average), 3 (Strong)
    y_class = []
    for sc in target_score:
        if sc >= 80.0:
            y_class.append(3) # Strong
        elif sc >= 60.0:
            y_class.append(2) # Average
        elif sc >= 40.0:
            y_class.append(1) # Weak
        else:
            y_class.append(0) # Very Weak

    classifier = RandomForestClassifier(n_estimators=100, max_depth=6, random_state=42)
    classifier.fit(X_train, y_class)

    classifier_path = os.path.join(models_dir, "topic_classifier.joblib")
    joblib.dump(classifier, classifier_path)
    print(f"[OK] Saved Topic Classifier Model to {classifier_path}")

    print("All ML models trained and saved successfully!")

if __name__ == "__main__":
    train_and_save_models()
