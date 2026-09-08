import os
from sqlalchemy.orm import Session
from app.database.session import Base, engine, SessionLocal
from app.models.db_models import (
    User, StudentProfile, Subject, Topic, Question, TopicPerformance
)
from app.core.security import get_password_hash

def seed_database():
    print("Initializing Database Schema...")
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()

    try:
        # Check if already seeded
        if db.query(Subject).first():
            print("Database already seeded with subjects and questions.")
            return

        print("Seeding subjects, topics, and MCQ diagnostic questions...")

        # 1. Create Default Demo Student Account
        demo_user = User(
            email="student@demo.edu",
            hashed_password=get_password_hash("password123"),
            full_name="Alex Mercer"
        )
        db.add(demo_user)
        db.flush()

        demo_profile = StudentProfile(
            user_id=demo_user.id,
            college="MIT School of Computer Science",
            course="B.Tech Computer Science",
            semester="Semester 4",
            learning_goals="Master OOP in Java, Data Structures, and Database Systems for upcoming placement exams."
        )
        db.add(demo_profile)

        # 2. Subjects & Topics Data Definitions
        subjects_data = [
            {
                "name": "Object Oriented Programming (Java)",
                "code": "CS201",
                "description": "Core OOP paradigms including encapsulation, inheritance, polymorphism, abstraction, and exception handling in Java.",
                "topics": [
                    {
                        "name": "Variables & Data Types",
                        "difficulty": 1,
                        "importance": 1.0,
                        "questions": [
                            {
                                "question": "Which primitive data type in Java is used to store 64-bit signed integers?",
                                "a": "int", "b": "long", "c": "short", "d": "double",
                                "correct": "B",
                                "explanation": "In Java, 'long' is a 64-bit signed two's complement integer, while 'int' is 32-bit.",
                                "sub_concept": "Primitive Types"
                            },
                            {
                                "question": "What is the default value of a boolean instance variable in Java?",
                                "a": "true", "b": "false", "c": "null", "d": "0",
                                "correct": "B",
                                "explanation": "Instance boolean variables in Java automatically default to 'false' if uninitialized.",
                                "sub_concept": "Variable Initialization"
                            }
                        ]
                    },
                    {
                        "name": "Control Loops & Logic",
                        "difficulty": 2,
                        "importance": 1.1,
                        "questions": [
                            {
                                "question": "Which loop guarantees that the body executes at least once?",
                                "a": "for loop", "b": "while loop", "c": "do-while loop", "d": "for-each loop",
                                "correct": "C",
                                "explanation": "A do-while loop evaluates its condition at the bottom of the loop body, guaranteeing at least one execution.",
                                "sub_concept": "Loop Execution"
                            }
                        ]
                    },
                    {
                        "name": "Arrays & Strings",
                        "difficulty": 2,
                        "importance": 1.2,
                        "questions": [
                            {
                                "question": "Why are String objects in Java considered immutable?",
                                "a": "To save memory via the String Constant Pool and ensure thread safety.",
                                "b": "Because Java does not support string concatenation.",
                                "c": "To prevent strings from being stored in heap memory.",
                                "d": "Strings can actually be altered after creation.",
                                "correct": "A",
                                "explanation": "String immutability enables the Java String Constant Pool, preventing unintended side effects across shared references.",
                                "sub_concept": "String Immutability"
                            }
                        ]
                    },
                    {
                        "name": "Inheritance & Interfaces",
                        "difficulty": 3,
                        "importance": 1.4,
                        "questions": [
                            {
                                "question": "Which Java keyword is used by a class to inherit from an interface?",
                                "a": "extends", "b": "implements", "c": "inherits", "d": "using",
                                "correct": "B",
                                "explanation": "In Java, a class uses the 'implements' keyword to fulfill contracts defined by an interface.",
                                "sub_concept": "Interface Inheritance"
                            },
                            {
                                "question": "Does Java support multiple inheritance of classes directly?",
                                "a": "Yes, using comma separators in extends.",
                                "b": "No, Java avoids the Diamond Problem by restricting class inheritance to single parent.",
                                "c": "Yes, but only for abstract classes.",
                                "d": "Only when using final methods.",
                                "correct": "B",
                                "explanation": "Java disallows multiple class inheritance to avoid ambiguity (the Diamond Problem). Multiple interface implementation is supported.",
                                "sub_concept": "Diamond Problem"
                            }
                        ]
                    },
                    {
                        "name": "Polymorphism & Overriding",
                        "difficulty": 4,
                        "importance": 1.5,
                        "questions": [
                            {
                                "question": "What distinguishes Method Overriding from Method Overloading?",
                                "a": "Overriding occurs in the same class; Overloading requires inheritance.",
                                "b": "Overriding involves runtime dynamic dispatch with identical method signature in a subclass.",
                                "c": "Overloading changes the return type only.",
                                "d": "There is no difference.",
                                "correct": "B",
                                "explanation": "Method Overriding happens at runtime (Dynamic Binding) when a child class redefines a parent method with exact matching arguments.",
                                "sub_concept": "Dynamic Binding & Overriding"
                            },
                            {
                                "question": "What happens if you try to override a method marked as 'final' in Java?",
                                "a": "Compiler error occurs.", "b": "Runtime exception is thrown.", "c": "Method is hidden.", "d": "Code executes normally.",
                                "correct": "A",
                                "explanation": "Methods marked 'final' cannot be overridden by subclasses; attempting to do so produces a compilation failure.",
                                "sub_concept": "Final Specifier"
                            }
                        ]
                    },
                    {
                        "name": "Exception Handling",
                        "difficulty": 3,
                        "importance": 1.3,
                        "questions": [
                            {
                                "question": "Which block is guaranteed to execute regardless of whether an exception is caught or thrown?",
                                "a": "try", "b": "catch", "c": "finally", "d": "throws",
                                "correct": "C",
                                "explanation": "The 'finally' block always executes after try/catch, making it ideal for cleanup like closing resource connections.",
                                "sub_concept": "Try-Catch-Finally"
                            }
                        ]
                    }
                ]
            },
            {
                "name": "Data Structures & Algorithms",
                "code": "CS202",
                "description": "Fundamental algorithms, time/space complexity analysis, linear and non-linear data structures.",
                "topics": [
                    {
                        "name": "Big-O Time Complexity",
                        "difficulty": 2,
                        "importance": 1.5,
                        "questions": [
                            {
                                "question": "What is the average time complexity of searching in a balanced Binary Search Tree (BST)?",
                                "a": "O(1)", "b": "O(log N)", "c": "O(N)", "d": "O(N log N)",
                                "correct": "B",
                                "explanation": "Searching a balanced BST eliminates half the tree at each step, yielding O(log N) average time complexity.",
                                "sub_concept": "Tree Search Complexity"
                            }
                        ]
                    },
                    {
                        "name": "Stacks & Queues",
                        "difficulty": 2,
                        "importance": 1.2,
                        "questions": [
                            {
                                "question": "Which data structure operates on a First-In, First-Out (FIFO) principle?",
                                "a": "Stack", "b": "Queue", "c": "Array", "d": "Tree",
                                "correct": "B",
                                "explanation": "Queues strictly maintain FIFO ordering (items inserted first are removed first).",
                                "sub_concept": "FIFO Operations"
                            }
                        ]
                    },
                    {
                        "name": "Sorting Algorithms",
                        "difficulty": 4,
                        "importance": 1.4,
                        "questions": [
                            {
                                "question": "What is the worst-case time complexity of QuickSort when a poor pivot is chosen repeatedly?",
                                "a": "O(N log N)", "b": "O(N^2)", "c": "O(N)", "d": "O(log N)",
                                "correct": "B",
                                "explanation": "When an array is already sorted and the extreme element is selected as pivot, QuickSort degrades to O(N^2).",
                                "sub_concept": "QuickSort Degeneracy"
                            }
                        ]
                    }
                ]
            },
            {
                "name": "Database Management Systems",
                "code": "CS301",
                "description": "Relational algebra, SQL query optimization, normalization theory, and ACID transaction semantics.",
                "topics": [
                    {
                        "name": "SQL Joins & Subqueries",
                        "difficulty": 3,
                        "importance": 1.3,
                        "questions": [
                            {
                                "question": "Which JOIN returns all rows from the left table and matched records from the right table?",
                                "a": "INNER JOIN", "b": "LEFT OUTER JOIN", "c": "RIGHT OUTER JOIN", "d": "FULL JOIN",
                                "correct": "B",
                                "explanation": "LEFT JOIN returns all records from the left table regardless of matching records in the right table (unmatched right columns output NULL).",
                                "sub_concept": "Outer Joins"
                            }
                        ]
                    },
                    {
                        "name": "Database Normalization",
                        "difficulty": 4,
                        "importance": 1.4,
                        "questions": [
                            {
                                "question": "A relation is in Third Normal Form (3NF) if it is in 2NF and has no:",
                                "a": "Partial dependencies", "b": "Transitive dependencies", "c": "Multi-valued dependencies", "d": "Repeating groups",
                                "correct": "B",
                                "explanation": "3NF requires eliminating transitive functional dependencies (where non-key attributes depend on other non-key attributes).",
                                "sub_concept": "Transitive Dependency"
                            }
                        ]
                    },
                    {
                        "name": "ACID Properties & Transactions",
                        "difficulty": 3,
                        "importance": 1.5,
                        "questions": [
                            {
                                "question": "Which ACID property ensures that all operations in a transaction complete successfully or none are applied?",
                                "a": "Atomicity", "b": "Consistency", "c": "Isolation", "d": "Durability",
                                "correct": "A",
                                "explanation": "Atomicity follows the 'all-or-nothing' rule for database updates.",
                                "sub_concept": "Transaction Atomicity"
                            }
                        ]
                    }
                ]
            }
        ]

        # Insert subjects, topics, and questions
        for s_data in subjects_data:
            subject = Subject(name=s_data["name"], code=s_data["code"], description=s_data["description"])
            db.add(subject)
            db.flush()

            prev_topic_id = None
            for t_data in s_data["topics"]:
                topic = Topic(
                    subject_id=subject.id,
                    name=t_data["name"],
                    difficulty_level=t_data["difficulty"],
                    importance_weight=t_data["importance"],
                    prerequisite_topic_id=prev_topic_id
                )
                db.add(topic)
                db.flush()

                # Seed initial topic performance for demo user
                # Give Java OOP topics varied initial scores to show weak vs strong topics
                attempts_count = 0
                acc = 0.0
                recent = 0.0
                status = "Average"
                weakness = 50.0
                confidence = 50.0

                if t_data["name"] == "Polymorphism & Overriding":
                    attempts_count = 3
                    acc = 45.0
                    recent = 40.0
                    status = "Weak"
                    weakness = 60.0
                    confidence = 40.0
                elif t_data["name"] == "Exception Handling":
                    attempts_count = 2
                    acc = 50.0
                    recent = 52.0
                    status = "Weak"
                    weakness = 50.0
                    confidence = 50.0
                elif t_data["name"] == "Variables & Data Types":
                    attempts_count = 4
                    acc = 90.0
                    recent = 92.0
                    status = "Strong"
                    weakness = 10.0
                    confidence = 90.0
                elif t_data["name"] == "Control Loops & Logic":
                    attempts_count = 3
                    acc = 82.0
                    recent = 85.0
                    status = "Strong"
                    weakness = 18.0
                    confidence = 82.0

                t_perf = TopicPerformance(
                    student_id=demo_user.id,
                    topic_id=topic.id,
                    quiz_attempts=attempts_count,
                    correct_answers=int(attempts_count * (acc / 100.0) * 5),
                    total_questions=attempts_count * 5 if attempts_count > 0 else 0,
                    accuracy=acc,
                    recent_score=recent,
                    avg_score=acc,
                    difficulty_level=t_data["difficulty"],
                    weakness_score=weakness,
                    confidence_score=confidence,
                    status_label=status
                )
                db.add(t_perf)

                for q_data in t_data["questions"]:
                    question = Question(
                        topic_id=topic.id,
                        question_text=q_data["question"],
                        option_a=q_data["a"],
                        option_b=q_data["b"],
                        option_c=q_data["c"],
                        option_d=q_data["d"],
                        correct_option=q_data["correct"],
                        explanation=q_data["explanation"],
                        sub_concept=q_data.get("sub_concept", "General"),
                        difficulty=t_data["difficulty"]
                    )
                    db.add(question)

                prev_topic_id = topic.id

        db.commit()
        print("[OK] Database successfully seeded!")

    except Exception as e:
        db.rollback()
        print(f"Error seeding database: {e}")
        raise e
    finally:
        db.close()

if __name__ == "__main__":
    seed_database()
