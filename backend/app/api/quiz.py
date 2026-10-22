import datetime
from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from typing import List, Optional
from pydantic import BaseModel
from app.database.session import get_db
from app.models.db_models import User, Subject, Topic, Question, QuizAttempt, QuizAnswer, TopicPerformance, Prediction
from app.schemas.pydantic_schemas import (
    QuizStartResponse, QuestionOut, QuizSubmission, QuizResultResponse, AnswerExplanation
)
from app.api.auth import get_current_user
from app.services.study_service import study_service
from app.services.audit_service import audit_service

router = APIRouter(prefix="/quiz", tags=["Adaptive Quiz System"])

class StartQuizRequest(BaseModel):
    subject_id: int
    topic_id: Optional[int] = None
    question_count: Optional[int] = 5

@router.post("/start", response_model=QuizStartResponse)
def start_quiz(data: StartQuizRequest, request: Request, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    subject = db.query(Subject).get(data.subject_id)
    if not subject:
        raise HTTPException(status_code=404, detail="Subject not found")

    # Fetch questions (prioritize student weak topics if topic_id not specified)
    if data.topic_id:
        topic = db.query(Topic).get(data.topic_id)
        questions = db.query(Question).filter_by(topic_id=data.topic_id).all()
    else:
        topic = None
        # Find weakest topic for this subject
        top_perfs = db.query(TopicPerformance).join(Topic).filter(
            TopicPerformance.student_id == user.id,
            Topic.subject_id == data.subject_id
        ).order_by(TopicPerformance.accuracy.asc()).all()

        if top_perfs:
            weakest_topic_id = top_perfs[0].topic_id
            topic = db.query(Topic).get(weakest_topic_id)
            questions = db.query(Question).filter_by(topic_id=weakest_topic_id).all()
        else:
            questions = db.query(Question).join(Topic).filter(Topic.subject_id == data.subject_id).all()

    if not questions:
        # Fallback to any questions in DB
        questions = db.query(Question).limit(5).all()

    selected_questions = questions[:data.question_count]

    # Predict score using ML Model 2 before quiz starts
    predicted_score = study_service.predict_expected_score(
        db=db,
        student_id=user.id,
        subject_id=data.subject_id,
        topic_id=topic.id if topic else None
    )

    attempt = QuizAttempt(
        student_id=user.id,
        subject_id=data.subject_id,
        topic_id=topic.id if topic else (selected_questions[0].topic_id if selected_questions else None),
        predicted_score=predicted_score,
        total_questions=len(selected_questions),
        completed_at=datetime.datetime.utcnow()
    )
    db.add(attempt)
    db.commit()
    db.refresh(attempt)

    # Save Prediction Log for evaluation
    pred_log = Prediction(
        student_id=user.id,
        topic_id=attempt.topic_id,
        predicted_score=predicted_score,
        features_json=f'{{"subject_id": {data.subject_id}, "questions": {len(selected_questions)}}}'
    )
    db.add(pred_log)
    db.commit()

    q_outs = [
        QuestionOut(
            id=q.id,
            question_text=q.question_text,
            option_a=q.option_a,
            option_b=q.option_b,
            option_c=q.option_c,
            option_d=q.option_d,
            sub_concept=q.sub_concept
        )
        for q in selected_questions
    ]

    audit_service.log_activity(
        db=db,
        action_type="START_QUIZ",
        user_id=user.id,
        request=request,
        details={
            "attempt_id": attempt.id,
            "subject_name": subject.name,
            "topic_name": topic.name if topic else "Mixed Topics",
            "predicted_score": predicted_score,
            "total_questions": len(selected_questions)
        }
    )

    return QuizStartResponse(
        attempt_id=attempt.id,
        subject_id=subject.id,
        subject_name=subject.name,
        topic_id=topic.id if topic else None,
        topic_name=topic.name if topic else "Mixed Topics",
        predicted_score=predicted_score,
        total_questions=len(selected_questions),
        questions=q_outs
    )

@router.post("/submit", response_model=QuizResultResponse)
def submit_quiz(data: QuizSubmission, request: Request, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    attempt = db.query(QuizAttempt).filter_by(id=data.attempt_id, student_id=user.id).first()
    if not attempt:
        raise HTTPException(status_code=404, detail="Quiz attempt not found")

    correct_count = 0
    total_q = len(data.answers)
    explanations = []
    weak_concepts = []

    for ans in data.answers:
        q = db.query(Question).get(ans.question_id)
        if not q:
            continue
        is_corr = (ans.selected_option.upper().strip() == q.correct_option.upper().strip())
        if is_corr:
            correct_count += 1
        else:
            if q.sub_concept and q.sub_concept not in weak_concepts:
                weak_concepts.append(q.sub_concept)

        qa = QuizAnswer(
            quiz_attempt_id=attempt.id,
            question_id=q.id,
            selected_option=ans.selected_option.upper().strip(),
            is_correct=is_corr
        )
        db.add(qa)

        explanations.append(AnswerExplanation(
            question_id=q.id,
            question_text=q.question_text,
            selected_option=ans.selected_option,
            correct_option=q.correct_option,
            is_correct=is_corr,
            explanation=q.explanation,
            sub_concept=q.sub_concept
        ))

    actual_score = round((correct_count / max(1, total_q)) * 100.0, 1)
    score_diff = round(actual_score - attempt.predicted_score, 1)

    attempt.actual_score = actual_score
    attempt.score_diff = score_diff
    attempt.correct_answers = correct_count
    attempt.total_questions = total_q
    attempt.time_taken_seconds = data.time_taken_seconds
    attempt.completed_at = datetime.datetime.utcnow()

    # Update prediction log actual_score
    pred_log = db.query(Prediction).filter_by(student_id=user.id, topic_id=attempt.topic_id).order_by(Prediction.id.desc()).first()
    if pred_log:
        pred_log.actual_score = actual_score

    db.commit()

    # Update Student Topic Performance Profile using ML Model 1 & recalculate recommendations
    if attempt.topic_id:
        study_service.update_performance_after_quiz(
            db=db,
            student_id=user.id,
            topic_id=attempt.topic_id,
            correct_in_quiz=correct_count,
            total_in_quiz=total_q
        )

    # Refresh recommendations for user
    study_service.refresh_recommendations(db, user.id)

    # Generate AI Feedback Statement
    topic_name = "this topic"
    if attempt.topic:
        topic_name = attempt.topic.name

    if weak_concepts:
        rev_msg = f"You showed good effort, but struggled with {', '.join(weak_concepts)}. Revise these concepts before attempting the next quiz."
    elif actual_score >= 80.0:
        rev_msg = f"Outstanding performance in {topic_name}! You have demonstrated strong conceptual mastery."
    else:
        rev_msg = f"Solid attempt in {topic_name}. Review key definitions to boost accuracy."

    recs = db.query(Topic).filter(Topic.subject_id == attempt.subject_id, Topic.id != attempt.topic_id).all()
    next_topic_name = recs[0].name if recs else "Advanced Problem Solving"

    audit_service.log_activity(
        db=db,
        action_type="SUBMIT_QUIZ",
        user_id=user.id,
        request=request,
        details={
            "attempt_id": attempt.id,
            "actual_score": actual_score,
            "predicted_score": attempt.predicted_score,
            "score_diff": score_diff,
            "correct_answers": correct_count,
            "total_questions": total_q,
            "time_taken_seconds": data.time_taken_seconds,
            "weak_concepts": weak_concepts
        }
    )

    return QuizResultResponse(
        attempt_id=attempt.id,
        actual_score=actual_score,
        predicted_score=attempt.predicted_score,
        score_diff=score_diff,
        correct_answers=correct_count,
        total_questions=total_q,
        time_taken_seconds=data.time_taken_seconds,
        explanations=explanations,
        weak_concepts_identified=weak_concepts,
        recommended_revision=rev_msg,
        next_recommended_topic=next_topic_name
    )

@router.get("/history")
def get_quiz_history(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    attempts = db.query(QuizAttempt).filter_by(student_id=user.id).order_by(QuizAttempt.completed_at.desc()).all()
    history = []
    for att in attempts:
        history.append({
            "id": att.id,
            "subject": att.subject.name if att.subject else "Subject",
            "topic": att.topic.name if att.topic else "Mixed",
            "predicted_score": att.predicted_score,
            "actual_score": att.actual_score,
            "score_diff": att.score_diff,
            "correct": att.correct_answers,
            "total": att.total_questions,
            "date": att.completed_at.strftime("%Y-%m-%d %H:%M")
        })
    return history
