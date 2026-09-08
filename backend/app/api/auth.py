from fastapi import APIRouter, Depends, HTTPException, status, Request
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.models.db_models import User, StudentProfile
from app.schemas.pydantic_schemas import UserRegister, UserLogin, Token, StudentProfileOut
from app.core.security import verify_password, get_password_hash, create_access_token, decode_access_token
from app.services.audit_service import audit_service

router = APIRouter(prefix="/auth", tags=["Authentication"])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> User:
    payload = decode_access_token(token)
    if not payload or "sub" not in payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    user_id = int(payload["sub"])
    user = db.query(User).filter_by(id=user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.post("/register", response_model=Token)
def register(data: UserRegister, request: Request, db: Session = Depends(get_db)):
    existing = db.query(User).filter_by(email=data.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email is already registered")

    user = User(
        email=data.email,
        hashed_password=get_password_hash(data.password),
        full_name=data.full_name
    )
    db.add(user)
    db.flush()

    profile = StudentProfile(
        user_id=user.id,
        college=data.college or "State University",
        course=data.course or "Computer Science & Engineering",
        semester=data.semester or "Semester 4",
        learning_goals=data.learning_goals or "Master Core CS Principles"
    )
    db.add(profile)
    db.commit()
    db.refresh(user)

    audit_service.log_activity(
        db=db,
        action_type="REGISTER",
        user_id=user.id,
        request=request,
        details={"email": user.email, "full_name": user.full_name}
    )

    token = create_access_token(subject=user.id)
    return Token(access_token=token, token_type="bearer", user_id=user.id, full_name=user.full_name)

@router.post("/login", response_model=Token)
def login(data: UserLogin, request: Request, db: Session = Depends(get_db)):
    user = db.query(User).filter_by(email=data.email).first()
    if not user or not verify_password(data.password, user.hashed_password):
        audit_service.log_activity(
            db=db,
            action_type="LOGIN_FAILED",
            request=request,
            details={"email": data.email}
        )
        raise HTTPException(status_code=401, detail="Invalid email or password")

    audit_service.log_activity(
        db=db,
        action_type="LOGIN_SUCCESS",
        user_id=user.id,
        request=request,
        details={"email": user.email}
    )

    token = create_access_token(subject=user.id)
    return Token(access_token=token, token_type="bearer", user_id=user.id, full_name=user.full_name)
