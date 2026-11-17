from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app.database.session import get_db
from app.models.db_models import User, UserActivityLog, QuizAttempt, StudentProfile
from app.api.auth import get_current_user

router = APIRouter(prefix="/admin", tags=["Admin & User Activity Tracking"])

@router.get("/activity-logs")
def get_user_activity_logs(
    user_id: Optional[int] = Query(None, description="Filter by user ID"),
    action_type: Optional[str] = Query(None, description="Filter by action type"),
    limit: int = Query(50, ge=1, le=500),
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    query = db.query(UserActivityLog)
    if user_id:
        query = query.filter(UserActivityLog.user_id == user_id)
    if action_type:
        query = query.filter(UserActivityLog.action_type == action_type)

    logs = query.order_by(UserActivityLog.created_at.desc()).limit(limit).all()

    results = []
    for log in logs:
        student_name = log.user.full_name if log.user else "Anonymous/Guest"
        student_email = log.user.email if log.user else "N/A"
        results.append({
            "id": log.id,
            "user_id": log.user_id,
            "student_name": student_name,
            "student_email": student_email,
            "action_type": log.action_type,
            "endpoint": log.endpoint,
            "ip_address": log.ip_address,
            "user_agent": log.user_agent,
            "details": log.details_json,
            "timestamp": log.created_at.strftime("%Y-%m-%d %H:%M:%S")
        })

    return {
        "total_logs_returned": len(results),
        "logs": results
    }

@router.get("/user-analytics")
def get_user_analytics_summary(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    users = db.query(User).all()
    user_summaries = []

    for u in users:
        prof = db.query(StudentProfile).filter_by(user_id=u.id).first()
        attempts = db.query(QuizAttempt).filter_by(student_id=u.id).all()
        logs_count = db.query(UserActivityLog).filter_by(user_id=u.id).count()
        last_log = db.query(UserActivityLog).filter_by(user_id=u.id).order_by(UserActivityLog.created_at.desc()).first()

        avg_score = round(sum(a.actual_score for a in attempts) / max(1, len(attempts)), 1) if attempts else 0.0

        user_summaries.append({
            "user_id": u.id,
            "full_name": u.full_name,
            "email": u.email,
            "college": prof.college if prof else "N/A",
            "total_quizzes_taken": len(attempts),
            "average_quiz_score": avg_score,
            "total_activity_events": logs_count,
            "last_active": last_log.created_at.strftime("%Y-%m-%d %H:%M:%S") if last_log else u.created_at.strftime("%Y-%m-%d %H:%M:%S")
        })

    return {
        "total_registered_students": len(users),
        "students": user_summaries
    }
