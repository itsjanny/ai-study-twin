import datetime
from sqlalchemy.orm import Session
from app.models.db_models import (
    TopicPerformance, Topic, Subject, QuizAttempt, QuizAnswer, Question, Recommendation, StudySession, Prediction
)
from app.ml.classifier import classifier_model
from app.ml.predictor import score_predictor
from app.ml.recommender import recommender_engine

class StudyService:
    
    @staticmethod
    def get_or_create_topic_performance(db: Session, student_id: int, topic_id: int) -> TopicPerformance:
        perf = db.query(TopicPerformance).filter_by(student_id=student_id, topic_id=topic_id).first()
        if not perf:
            topic = db.query(Topic).get(topic_id)
            diff = topic.difficulty_level if topic else 3
            perf = TopicPerformance(
                student_id=student_id,
                topic_id=topic_id,
                quiz_attempts=0,
                correct_answers=0,
                total_questions=0,
                accuracy=0.0,
                recent_score=0.0,
                avg_score=0.0,
                difficulty_level=diff,
                last_studied_date=datetime.datetime.utcnow() - datetime.timedelta(days=7),
                revision_count=0,
                weakness_score=50.0,
                confidence_score=50.0,
                status_label="Average"
            )
            db.add(perf)
            db.commit()
            db.refresh(perf)
        return perf

    @staticmethod
    def update_performance_after_quiz(
        db: Session,
        student_id: int,
        topic_id: int,
        correct_in_quiz: int,
        total_in_quiz: int
    ):
        perf = StudyService.get_or_create_topic_performance(db, student_id, topic_id)
        
        quiz_pct = (correct_in_quiz / max(1, total_in_quiz)) * 100.0
        
        perf.quiz_attempts += 1
        perf.correct_answers += correct_in_quiz
        perf.total_questions += total_in_quiz
        
        # Calculate new cumulative accuracy
        perf.accuracy = round((perf.correct_answers / max(1, perf.total_questions)) * 100.0, 1)
        
        # Exponential moving average for recent score
        if perf.quiz_attempts == 1:
            perf.recent_score = quiz_pct
            perf.avg_score = quiz_pct
        else:
            perf.recent_score = round(0.7 * quiz_pct + 0.3 * perf.recent_score, 1)
            perf.avg_score = round((perf.avg_score * (perf.quiz_attempts - 1) + quiz_pct) / perf.quiz_attempts, 1)
            
        perf.last_studied_date = datetime.datetime.utcnow()

        # Run Weak Topic ML Classifier
        classification = classifier_model.classify_topic(
            accuracy=perf.accuracy,
            attempts=perf.quiz_attempts,
            recent_score=perf.recent_score,
            difficulty_level=perf.difficulty_level
        )

        perf.status_label = classification["label"]
        perf.weakness_score = classification["weakness_score"]
        perf.confidence_score = classification["confidence_score"]

        db.commit()
        db.refresh(perf)
        return perf

    @staticmethod
    def predict_expected_score(db: Session, student_id: int, subject_id: int, topic_id: int = None) -> float:
        """
        Uses ML Model 2 to predict upcoming quiz score.
        """
        if topic_id:
            topics = [db.query(Topic).get(topic_id)]
        else:
            topics = db.query(Topic).filter_by(subject_id=subject_id).all()

        if not topics:
            return 72.0

        scores = []
        for top in topics:
            if not top:
                continue
            perf = StudyService.get_or_create_topic_performance(db, student_id, top.id)
            days_since = (datetime.datetime.utcnow() - perf.last_studied_date).total_seconds() / 86400.0
            
            pred = score_predictor.predict_score(
                attempts=perf.quiz_attempts,
                topic_accuracy=perf.accuracy if perf.quiz_attempts > 0 else 65.0,
                recent_score=perf.recent_score if perf.quiz_attempts > 0 else 65.0,
                overall_avg=perf.avg_score if perf.quiz_attempts > 0 else 65.0,
                revision_count=perf.revision_count,
                days_since_last_study=days_since,
                difficulty_level=top.difficulty_level
            )
            scores.append(pred)

        return round(float(sum(scores) / len(scores)), 1) if scores else 70.0

    @staticmethod
    def refresh_recommendations(db: Session, student_id: int):
        """
        Calculates priority ranking across all topics using ML Model 3.
        """
        all_topics = db.query(Topic).all()
        recs = []

        # Clear existing active recommendations for this student
        db.query(Recommendation).filter_by(student_id=student_id).delete()
        db.commit()

        for top in all_topics:
            perf = StudyService.get_or_create_topic_performance(db, student_id, top.id)
            days_since = (datetime.datetime.utcnow() - perf.last_studied_date).total_seconds() / 86400.0
            
            # Prerequisite check
            prereq_mastered = True
            if top.prerequisite_topic_id:
                p_perf = StudyService.get_or_create_topic_performance(db, student_id, top.prerequisite_topic_id)
                if p_perf.accuracy < 60.0 and p_perf.quiz_attempts > 0:
                    prereq_mastered = False

            p_score = recommender_engine.calculate_priority_score(
                weakness_score=perf.weakness_score,
                days_since_last_study=days_since,
                difficulty_level=top.difficulty_level,
                importance_weight=top.importance_weight,
                prereq_mastered=prereq_mastered
            )

            rev_info = recommender_engine.calculate_revision_requirement(perf.status_label, days_since)

            # Generate reason string
            subject_name = top.subject.name if top.subject else "Subject"
            if perf.status_label in ["Weak", "Very Weak"]:
                reason = f"{subject_name} — {top.name} is currently a '{perf.status_label}' area with low recent accuracy ({perf.recent_score}%). Focus on revision before next quiz."
            elif not prereq_mastered:
                reason = f"{top.name} has unmastered prerequisite concepts. Review fundamentals first."
            elif days_since > 7:
                reason = f"{top.name} has not been studied in {int(days_since)} days. Scheduled for retention revision."
            else:
                reason = f"{top.name} aligns with your active curriculum goals for {subject_name}."

            recs.append({
                "topic": top,
                "priority_score": p_score,
                "reason": reason,
                "revision_required": rev_info["revision_required"],
                "recommended_duration_min": rev_info["recommended_minutes"]
            })

        # Sort descending by priority_score
        recs.sort(key=lambda x: x["priority_score"], reverse=True)

        # Save top recommendations
        saved_recs = []
        for idx, item in enumerate(recs, start=1):
            rec_db = Recommendation(
                student_id=student_id,
                topic_id=item["topic"].id,
                priority_rank=idx,
                priority_score=item["priority_score"],
                reason=item["reason"],
                revision_required=item["revision_required"],
                recommended_duration_min=item["recommended_duration_min"],
                status="Active"
            )
            db.add(rec_db)
            saved_recs.append(rec_db)

        db.commit()
        return saved_recs

study_service = StudyService()
