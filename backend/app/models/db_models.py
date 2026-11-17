import datetime
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Text, Boolean, JSON
from sqlalchemy.orm import relationship
from app.database.session import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    full_name = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    profile = relationship("StudentProfile", back_populates="user", uselist=False)
    quiz_attempts = relationship("QuizAttempt", back_populates="student")
    topic_performances = relationship("TopicPerformance", back_populates="student")
    recommendations = relationship("Recommendation", back_populates="student")
    study_sessions = relationship("StudySession", back_populates="student")
    predictions = relationship("Prediction", back_populates="student")
    activity_logs = relationship("UserActivityLog", back_populates="user")
    sessions = relationship("UserSession", back_populates="user")


class StudentProfile(Base):
    __tablename__ = "student_profiles"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True, nullable=False)
    college = Column(String(255), default="State University")
    course = Column(String(255), default="Computer Science & Engineering")
    semester = Column(String(50), default="Semester 4")
    learning_goals = Column(Text, default="Master Core Programming, Data Structures, and Database Systems")
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    user = relationship("User", back_populates="profile")


class Subject(Base):
    __tablename__ = "subjects"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    code = Column(String(50), nullable=False)
    description = Column(Text, nullable=True)

    topics = relationship("Topic", back_populates="subject", cascade="all, delete-orphan")
    quiz_attempts = relationship("QuizAttempt", back_populates="subject")


class Topic(Base):
    __tablename__ = "topics"

    id = Column(Integer, primary_key=True, index=True)
    subject_id = Column(Integer, ForeignKey("subjects.id"), nullable=False)
    name = Column(String(255), nullable=False)
    difficulty_level = Column(Integer, default=3) # 1 (Easy) to 5 (Hard)
    importance_weight = Column(Float, default=1.0)
    prerequisite_topic_id = Column(Integer, ForeignKey("topics.id"), nullable=True)

    subject = relationship("Subject", back_populates="topics")
    questions = relationship("Question", back_populates="topic", cascade="all, delete-orphan")
    performances = relationship("TopicPerformance", back_populates="topic")
    quiz_attempts = relationship("QuizAttempt", back_populates="topic")
    recommendations = relationship("Recommendation", back_populates="topic")
    study_sessions = relationship("StudySession", back_populates="topic")
    predictions = relationship("Prediction", back_populates="topic")


class Question(Base):
    __tablename__ = "questions"

    id = Column(Integer, primary_key=True, index=True)
    topic_id = Column(Integer, ForeignKey("topics.id"), nullable=False)
    question_text = Column(Text, nullable=False)
    option_a = Column(Text, nullable=False)
    option_b = Column(Text, nullable=False)
    option_c = Column(Text, nullable=False)
    option_d = Column(Text, nullable=False)
    correct_option = Column(String(10), nullable=False) # 'A', 'B', 'C', 'D'
    explanation = Column(Text, nullable=False)
    sub_concept = Column(String(255), nullable=True)
    difficulty = Column(Integer, default=3)

    topic = relationship("Topic", back_populates="questions")
    quiz_answers = relationship("QuizAnswer", back_populates="question")


class TopicPerformance(Base):
    __tablename__ = "topic_performance"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    topic_id = Column(Integer, ForeignKey("topics.id"), nullable=False)
    
    quiz_attempts = Column(Integer, default=0)
    correct_answers = Column(Integer, default=0)
    total_questions = Column(Integer, default=0)
    accuracy = Column(Float, default=0.0)
    recent_score = Column(Float, default=0.0)
    avg_score = Column(Float, default=0.0)
    difficulty_level = Column(Integer, default=3)
    last_studied_date = Column(DateTime, default=datetime.datetime.utcnow)
    revision_count = Column(Integer, default=0)
    weakness_score = Column(Float, default=50.0) # Higher = weaker
    confidence_score = Column(Float, default=50.0) # Higher = stronger
    status_label = Column(String(50), default="Average") # Strong, Average, Weak, Very Weak

    student = relationship("User", back_populates="topic_performances")
    topic = relationship("Topic", back_populates="performances")


class QuizAttempt(Base):
    __tablename__ = "quiz_attempts"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    subject_id = Column(Integer, ForeignKey("subjects.id"), nullable=False)
    topic_id = Column(Integer, ForeignKey("topics.id"), nullable=True)
    
    predicted_score = Column(Float, default=70.0)
    actual_score = Column(Float, default=0.0)
    score_diff = Column(Float, default=0.0)
    
    total_questions = Column(Integer, default=5)
    correct_answers = Column(Integer, default=0)
    time_taken_seconds = Column(Integer, default=120)
    completed_at = Column(DateTime, default=datetime.datetime.utcnow)

    student = relationship("User", back_populates="quiz_attempts")
    subject = relationship("Subject", back_populates="quiz_attempts")
    topic = relationship("Topic", back_populates="quiz_attempts")
    answers = relationship("QuizAnswer", back_populates="quiz_attempt", cascade="all, delete-orphan")


class QuizAnswer(Base):
    __tablename__ = "quiz_answers"

    id = Column(Integer, primary_key=True, index=True)
    quiz_attempt_id = Column(Integer, ForeignKey("quiz_attempts.id"), nullable=False)
    question_id = Column(Integer, ForeignKey("questions.id"), nullable=False)
    selected_option = Column(String(10), nullable=False)
    is_correct = Column(Boolean, nullable=False)

    quiz_attempt = relationship("QuizAttempt", back_populates="answers")
    question = relationship("Question", back_populates="quiz_answers")


class StudySession(Base):
    __tablename__ = "study_sessions"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    topic_id = Column(Integer, ForeignKey("topics.id"), nullable=False)
    duration_minutes = Column(Integer, default=30)
    completed = Column(Boolean, default=False)
    scheduled_for = Column(DateTime, default=datetime.datetime.utcnow)
    completed_at = Column(DateTime, nullable=True)

    student = relationship("User", back_populates="study_sessions")
    topic = relationship("Topic", back_populates="study_sessions")


class Recommendation(Base):
    __tablename__ = "recommendations"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    topic_id = Column(Integer, ForeignKey("topics.id"), nullable=False)
    priority_rank = Column(Integer, default=1)
    priority_score = Column(Float, default=80.0)
    reason = Column(Text, nullable=False)
    revision_required = Column(String(50), default="High") # High, Medium, Low, Light
    recommended_duration_min = Column(Integer, default=30)
    status = Column(String(50), default="Active")
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    student = relationship("User", back_populates="recommendations")
    topic = relationship("Topic", back_populates="recommendations")


class Prediction(Base):
    __tablename__ = "predictions"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    topic_id = Column(Integer, ForeignKey("topics.id"), nullable=True)
    predicted_score = Column(Float, nullable=False)
    actual_score = Column(Float, nullable=True)
    features_json = Column(Text, nullable=True)
    model_version = Column(String(50), default="v1.0.0-rf")
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    student = relationship("User", back_populates="predictions")
    topic = relationship("Topic", back_populates="predictions")


class UserActivityLog(Base):
    __tablename__ = "user_activity_logs"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    action_type = Column(String(100), nullable=False, index=True) # e.g., LOGIN, REGISTER, START_QUIZ, SUBMIT_QUIZ
    endpoint = Column(String(255), nullable=True)
    ip_address = Column(String(50), nullable=True)
    user_agent = Column(Text, nullable=True)
    details_json = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow, index=True)

    user = relationship("User", back_populates="activity_logs")


class UserSession(Base):
    __tablename__ = "user_sessions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    session_token = Column(String(255), unique=True, index=True, nullable=False)
    ip_address = Column(String(50), nullable=True)
    user_agent = Column(Text, nullable=True)
    login_at = Column(DateTime, default=datetime.datetime.utcnow)
    last_activity_at = Column(DateTime, default=datetime.datetime.utcnow)
    is_active = Column(Boolean, default=True)

    user = relationship("User", back_populates="sessions")


class StudyMaterial(Base):
    __tablename__ = "study_materials"

    id = Column(Integer, primary_key=True, index=True)
    topic_id = Column(Integer, ForeignKey("topics.id"), nullable=False)
    title = Column(String(255), nullable=False)
    content_markdown = Column(Text, nullable=False)
    code_snippet = Column(Text, nullable=True)
    cheat_sheet_json = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    topic = relationship("Topic", backref="study_materials")


