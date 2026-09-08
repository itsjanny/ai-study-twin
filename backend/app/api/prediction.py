from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.models.db_models import User, Prediction, TopicPerformance, Topic
from app.api.auth import get_current_user
from app.services.study_service import study_service

router = APIRouter(prefix="/prediction", tags=["ML Score Prediction"])

@router.get("")
def get_prediction_summary(subject_id: int = 1, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    predicted_score = study_service.predict_expected_score(db, user.id, subject_id)
    
    # Fetch recent predictions comparison
    recent_logs = db.query(Prediction).filter_by(student_id=user.id).order_by(Prediction.created_at.desc()).limit(10).all()
    logs_out = []
    for log in recent_logs:
        topic_name = log.topic.name if log.topic else "General Quiz"
        logs_out.append({
            "id": log.id,
            "topic": topic_name,
            "predicted_score": log.predicted_score,
            "actual_score": log.actual_score if log.actual_score is not None else "Pending",
            "diff": round(log.actual_score - log.predicted_score, 1) if log.actual_score is not None else "N/A",
            "date": log.created_at.strftime("%Y-%m-%d %H:%M")
        })

    return {
        "predicted_next_quiz_score": predicted_score,
        "model_version": "v1.0.0-RandomForest",
        "features_used": [
            "Previous Quiz Accuracy",
            "Attempt Frequencies",
            "Recency Decay (Days since last studied)",
            "Topic Difficulty Level",
            "Revision Count",
            "Moving Average Trend"
        ],
        "history": logs_out
    }
