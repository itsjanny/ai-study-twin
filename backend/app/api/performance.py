from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.models.db_models import User, TopicPerformance, QuizAttempt, Subject, Topic, Prediction
from app.api.auth import get_current_user

router = APIRouter(prefix="/performance", tags=["Performance Analytics"])

@router.get("")
def get_performance_analytics(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    perfs = db.query(TopicPerformance).filter_by(student_id=user.id).all()
    attempts = db.query(QuizAttempt).filter_by(student_id=user.id).order_by(QuizAttempt.completed_at.asc()).all()

    # 1. Strong vs Weak Doughnut Breakdown
    strong_cnt = sum(1 for p in perfs if p.status_label == "Strong")
    avg_cnt = sum(1 for p in perfs if p.status_label == "Average")
    weak_cnt = sum(1 for p in perfs if p.status_label in ["Weak", "Very Weak"])
    total_cnt = len(perfs)

    doughnut_data = {
        "labels": ["Strong (80-100%)", "Average (60-79%)", "Weak/Needs Work (<60%)"],
        "counts": [strong_cnt, avg_cnt, weak_cnt]
    }

    # 2. Radar Chart (Topic Strengths)
    radar_labels = [p.topic.name[:18] for p in perfs[:6] if p.topic]
    radar_values = [p.accuracy for p in perfs[:6]]

    # 3. Bar Chart (Subject Performance)
    subjects = db.query(Subject).all()
    bar_labels = []
    bar_values = []
    for s in subjects:
        s_perfs = [p for p in perfs if p.topic and p.topic.subject_id == s.id]
        acc = round(sum(p.accuracy for p in s_perfs) / max(1, len(s_perfs)), 1) if s_perfs else 70.0
        bar_labels.append(s.code)
        bar_values.append(acc)

    # 4. Line Chart (Performance over time)
    line_labels = []
    line_predicted = []
    line_actual = []
    for idx, att in enumerate(attempts):
        line_labels.append(f"Quiz #{idx+1}")
        line_predicted.append(att.predicted_score)
        line_actual.append(att.actual_score)

    if not line_labels:
        # Default placeholder trend
        line_labels = ["Quiz #1", "Quiz #2", "Quiz #3", "Quiz #4"]
        line_predicted = [68.0, 72.0, 70.0, 75.0]
        line_actual = [70.0, 68.0, 74.0, 78.0]

    # 5. Topic Breakdown Table
    topic_table = []
    for p in perfs:
        if not p.topic:
            continue
        days_since = int((db.query(User).first().created_at.now() - p.last_studied_date).total_seconds() / 86400.0)
        topic_table.append({
            "topic_id": p.topic_id,
            "topic_name": p.topic.name,
            "subject_name": p.topic.subject.name if p.topic.subject else "CS",
            "attempts": p.quiz_attempts,
            "accuracy": p.accuracy,
            "recent_score": p.recent_score,
            "status": p.status_label,
            "weakness_score": p.weakness_score,
            "confidence_score": p.confidence_score,
            "days_since_last_study": days_since,
            "revision_count": p.revision_count
        })

    return {
        "doughnut": doughnut_data,
        "radar": {"labels": radar_labels, "values": radar_values},
        "bar": {"labels": bar_labels, "values": bar_values},
        "line": {"labels": line_labels, "predicted": line_predicted, "actual": line_actual},
        "topic_table": topic_table
    }
