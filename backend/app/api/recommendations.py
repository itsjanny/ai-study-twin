from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from app.database.session import get_db
from app.models.db_models import User, Recommendation, Topic
from app.schemas.pydantic_schemas import RecommendationOut, StudyPlanOut
from app.api.auth import get_current_user
from app.services.study_service import study_service

router = APIRouter(tags=["Recommendations & Study Plan"])

@router.get("/recommendations", response_model=List[RecommendationOut])
def get_recommendations(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    recs = db.query(Recommendation).filter_by(student_id=user.id).order_by(Recommendation.priority_rank.asc()).all()
    if not recs:
        recs = study_service.refresh_recommendations(db, user.id)

    out = []
    for r in recs:
        if not r.topic:
            continue
        out.append(RecommendationOut(
            id=r.id,
            topic_id=r.topic_id,
            topic_name=r.topic.name,
            subject_name=r.topic.subject.name if r.topic.subject else "Subject",
            priority_rank=r.priority_rank,
            priority_score=r.priority_score,
            reason=r.reason,
            revision_required=r.revision_required,
            recommended_duration_min=r.recommended_duration_min
        ))
    return out

@router.get("/study-plan")
def get_study_plan(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    recs = db.query(Recommendation).filter_by(student_id=user.id).order_by(Recommendation.priority_rank.asc()).all()
    if not recs:
        recs = study_service.refresh_recommendations(db, user.id)

    total_min = sum(r.recommended_duration_min for r in recs[:4]) + 15 # +15 min quiz
    sessions = []
    for idx, r in enumerate(recs[:4], start=1):
        sessions.append({
            "step": idx,
            "topic_id": r.topic_id,
            "topic_name": r.topic.name if r.topic else "Topic",
            "subject_name": r.topic.subject.name if (r.topic and r.topic.subject) else "CS",
            "duration_minutes": r.recommended_duration_min,
            "revision_required": r.revision_required,
            "action": f"Study {r.topic.name if r.topic else 'Topic'} for {r.recommended_duration_min} minutes. Focus on weak sub-concepts.",
            "completed": False
        })

    sessions.append({
        "step": len(sessions) + 1,
        "topic_id": recs[0].topic_id if recs else 1,
        "topic_name": "Practice Diagnostic Quiz",
        "subject_name": "Quiz Session",
        "duration_minutes": 15,
        "revision_required": "Assessment",
        "action": "Take a 5-question targeted adaptive quiz to validate your score improvement.",
        "completed": False
    })

    return {
        "date": "Today's Personalized Plan",
        "total_minutes": total_min,
        "sessions": sessions
    }
