from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

# Auth Schemas
class UserRegister(BaseModel):
    email: str
    password: str
    full_name: str
    college: Optional[str] = "State University"
    course: Optional[str] = "Computer Science & Engineering"
    semester: Optional[str] = "Semester 4"
    learning_goals: Optional[str] = "Master Core Programming & DS"

class UserLogin(BaseModel):
    email: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user_id: int
    full_name: str

class StudentProfileUpdate(BaseModel):
    full_name: Optional[str] = None
    college: Optional[str] = None
    course: Optional[str] = None
    semester: Optional[str] = None
    learning_goals: Optional[str] = None

class StudentProfileOut(BaseModel):
    user_id: int
    email: str
    full_name: str
    college: str
    course: str
    semester: str
    learning_goals: str

# Subject & Topic Schemas
class TopicOut(BaseModel):
    id: int
    subject_id: int
    name: str
    difficulty_level: int
    importance_weight: float
    status_label: Optional[str] = "Not Attempted"
    accuracy: Optional[float] = 0.0

    class Config:
        from_attributes = True

class SubjectOut(BaseModel):
    id: int
    name: str
    code: str
    description: str
    topics: List[TopicOut] = []

    class Config:
        from_attributes = True

# Quiz Schemas
class QuestionOut(BaseModel):
    id: int
    question_text: str
    option_a: str
    option_b: str
    option_c: str
    option_d: str
    sub_concept: Optional[str] = None

class QuizStartResponse(BaseModel):
    attempt_id: int
    subject_id: int
    subject_name: str
    topic_id: Optional[int] = None
    topic_name: Optional[str] = None
    predicted_score: float
    total_questions: int
    questions: List[QuestionOut]

class AnswerSubmit(BaseModel):
    question_id: int
    selected_option: str # 'A', 'B', 'C', 'D'

class QuizSubmission(BaseModel):
    attempt_id: int
    answers: List[AnswerSubmit]
    time_taken_seconds: int = 60

class AnswerExplanation(BaseModel):
    question_id: int
    question_text: str
    selected_option: str
    correct_option: str
    is_correct: bool
    explanation: str
    sub_concept: Optional[str] = None

class QuizResultResponse(BaseModel):
    attempt_id: int
    actual_score: float
    predicted_score: float
    score_diff: float
    correct_answers: int
    total_questions: int
    time_taken_seconds: int
    explanations: List[AnswerExplanation]
    weak_concepts_identified: List[str]
    recommended_revision: str
    next_recommended_topic: str

# Dashboard & Performance Schemas
class DashboardStats(BaseModel):
    overall_performance_pct: float
    current_learning_level: str
    topics_mastered_count: int
    topics_needing_revision_count: int
    predicted_next_quiz_score: float
    strong_topics: List[str]
    weak_topics: List[str]
    recommended_topic: str
    recommendation_reason: str
    recent_quiz_scores: List[dict]
    performance_trend: List[dict]
    subject_performance: List[dict]
    todays_study_plan: List[dict]

class PerformanceOverview(BaseModel):
    overall_accuracy: float
    quizzes_completed: int
    total_study_hours: float
    strong_vs_weak: dict
    topic_breakdown: List[dict]
    subject_breakdown: List[dict]
    predicted_vs_actual: List[dict]

class RecommendationOut(BaseModel):
    id: int
    topic_id: int
    topic_name: str
    subject_name: str
    priority_rank: int
    priority_score: float
    reason: str
    revision_required: str
    recommended_duration_min: int

class StudyPlanOut(BaseModel):
    date: str
    total_minutes: int
    sessions: List[dict]
