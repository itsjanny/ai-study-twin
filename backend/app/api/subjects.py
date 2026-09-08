from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database.session import get_db
from app.models.db_models import Subject, Topic, TopicPerformance, User
from app.schemas.pydantic_schemas import SubjectOut, TopicOut
from app.api.auth import get_current_user
from app.services.study_service import study_service

router = APIRouter(prefix="/subjects", tags=["Subjects & Topics"])

@router.get("", response_model=List[SubjectOut])
def get_subjects(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    subjects = db.query(Subject).all()
    res = []
    
    for sub in subjects:
        topic_list = []
        for top in sub.topics:
            perf = study_service.get_or_create_topic_performance(db, user.id, top.id)
            topic_list.append(TopicOut(
                id=top.id,
                subject_id=top.subject_id,
                name=top.name,
                difficulty_level=top.difficulty_level,
                importance_weight=top.importance_weight,
                status_label=perf.status_label,
                accuracy=perf.accuracy
            ))
        
        res.append(SubjectOut(
            id=sub.id,
            name=sub.name,
            code=sub.code,
            description=sub.description,
            topics=topic_list
        ))
        
    return res

@router.get("/{subject_id}/topics", response_model=List[TopicOut])
def get_subject_topics(subject_id: int, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    topics = db.query(Topic).filter_by(subject_id=subject_id).all()
    res = []
    for top in topics:
        perf = study_service.get_or_create_topic_performance(db, user.id, top.id)
        res.append(TopicOut(
            id=top.id,
            subject_id=top.subject_id,
            name=top.name,
            difficulty_level=top.difficulty_level,
            importance_weight=top.importance_weight,
            status_label=perf.status_label,
            accuracy=perf.accuracy
        ))
    return res
