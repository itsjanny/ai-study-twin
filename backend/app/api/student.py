from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.models.db_models import User, StudentProfile
from app.schemas.pydantic_schemas import StudentProfileOut, StudentProfileUpdate
from app.api.auth import get_current_user

router = APIRouter(prefix="/student", tags=["Student Profile"])

@router.get("/profile", response_model=StudentProfileOut)
def get_profile(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    prof = db.query(StudentProfile).filter_by(user_id=user.id).first()
    if not prof:
        prof = StudentProfile(user_id=user.id)
        db.add(prof)
        db.commit()
        db.refresh(prof)
    
    return StudentProfileOut(
        user_id=user.id,
        email=user.email,
        full_name=user.full_name,
        college=prof.college,
        course=prof.course,
        semester=prof.semester,
        learning_goals=prof.learning_goals
    )

@router.put("/profile", response_model=StudentProfileOut)
def update_profile(
    data: StudentProfileUpdate,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if data.full_name:
        user.full_name = data.full_name
    
    prof = db.query(StudentProfile).filter_by(user_id=user.id).first()
    if not prof:
        prof = StudentProfile(user_id=user.id)
        db.add(prof)
    
    if data.college is not None:
        prof.college = data.college
    if data.course is not None:
        prof.course = data.course
    if data.semester is not None:
        prof.semester = data.semester
    if data.learning_goals is not None:
        prof.learning_goals = data.learning_goals

    db.commit()
    db.refresh(user)
    db.refresh(prof)

    return StudentProfileOut(
        user_id=user.id,
        email=user.email,
        full_name=user.full_name,
        college=prof.college,
        course=prof.course,
        semester=prof.semester,
        learning_goals=prof.learning_goals
    )
