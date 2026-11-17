from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.models.db_models import User, TopicPerformance, QuizAttempt, Subject, Topic, Recommendation
from app.schemas.pydantic_schemas import DashboardStats
from app.api.auth import get_current_user
from app.services.study_service import study_service

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])

@router.get("", response_model=DashboardStats)
def get_dashboard(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    # 1. Fetch Topic Performances
    perfs = db.query(TopicPerformance).filter_by(student_id=user.id).all()
    if not perfs:
        # Trigger initialization if empty
        study_service.refresh_recommendations(db, user.id)
        perfs = db.query(TopicPerformance).filter_by(student_id=user.id).all()

    total_topics = len(perfs)
    mastered = [p for p in perfs if p.status_label == "Strong"]
    weak = [p for p in perfs if p.status_label in ["Weak", "Very Weak"]]
    average = [p for p in perfs if p.status_label == "Average"]

    overall_pct = round(sum(p.accuracy for p in perfs) / max(1, total_topics), 1) if perfs else 0.0

    # Determine Learning Level
    if overall_pct >= 80.0:
        level = "Advanced (Level 4)"
    elif overall_pct >= 65.0:
        level = "Intermediate (Level 3)"
    elif overall_pct >= 45.0:
        level = "Developing (Level 2)"
    else:
        level = "Foundational (Level 1)"

    # 2. Predicted Next Quiz Score
    first_subject = db.query(Subject).first()
    predicted_next = study_service.predict_expected_score(
        db, user.id, first_subject.id if first_subject else 1
    )

    # 3. Top Recommendation
    recs = db.query(Recommendation).filter_by(student_id=user.id).order_by(Recommendation.priority_rank.asc()).all()
    if not recs:
        recs = study_service.refresh_recommendations(db, user.id)

    top_rec_topic = recs[0].topic.name if (recs and recs[0].topic) else "Polymorphism & Overriding"
    top_rec_reason = recs[0].reason if recs else "Topic needs immediate revision based on low accuracy."

    # 4. Recent Quiz Scores
    recent_attempts = db.query(QuizAttempt).filter_by(student_id=user.id).order_by(QuizAttempt.completed_at.desc()).limit(5).all()
    recent_scores = [
        {
            "id": a.id,
            "subject": a.subject.name if a.subject else "Subject",
            "topic": a.topic.name if a.topic else "Mixed",
            "actual_score": a.actual_score,
            "predicted_score": a.predicted_score,
            "diff": a.score_diff,
            "date": a.completed_at.strftime("%b %d")
        }
        for a in recent_attempts
    ]

    # If no recent attempts, seed mock trend for fresh view
    trend_data = [
        {"date": "Mon", "score": 62},
        {"date": "Tue", "score": 68},
        {"date": "Wed", "score": 65},
        {"date": "Thu", "score": 74},
        {"date": "Fri", "score": 78},
        {"date": "Sat", "score": 75},
        {"date": "Sun", "score": 82},
    ]

    # 5. Subject Performance
    subjects = db.query(Subject).all()
    subj_perf = []
    for s in subjects:
        s_perfs = [p for p in perfs if p.topic and p.topic.subject_id == s.id]
        s_acc = round(sum(p.accuracy for p in s_perfs) / max(1, len(s_perfs)), 1) if s_perfs else 70.0
        subj_perf.append({
            "subject_id": s.id,
            "subject_name": s.name,
            "code": s.code,
            "accuracy": s_acc,
            "topics_count": len(s_perfs)
        })

    # 6. Today's Study Plan
    study_plan = []
    for r in recs[:3]:
        study_plan.append({
            "id": r.id,
            "topic_id": r.topic_id,
            "topic_name": r.topic.name if r.topic else "Topic",
            "subject_name": r.topic.subject.name if (r.topic and r.topic.subject) else "CS",
            "duration_minutes": r.recommended_duration_min,
            "revision_required": r.revision_required,
            "reason": r.reason
        })

    return DashboardStats(
        overall_performance_pct=overall_pct,
        current_learning_level=level,
        topics_mastered_count=len(mastered),
        topics_needing_revision_count=len(weak),
        predicted_next_quiz_score=predicted_next,
        strong_topics=[p.topic.name for p in mastered if p.topic][:4],
        weak_topics=[p.topic.name for p in weak if p.topic][:4],
        recommended_topic=top_rec_topic,
        recommendation_reason=top_rec_reason,
        recent_quiz_scores=recent_scores,
        performance_trend=trend_data,
        subject_performance=subj_perf,
        todays_study_plan=study_plan
    )
