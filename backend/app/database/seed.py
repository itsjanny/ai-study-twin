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

        print("Seeding Python & Java (Basic to Advanced) subjects, topics, and MCQ diagnostic questions...")

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
            learning_goals="Master Python, Java Basic to Advanced, Data Structures, and Database Systems."
        )
        db.add(demo_profile)

        # 2. Subjects & Topics Data Definitions
        subjects_data = [
            {
                "name": "Python Programming (Basic to Advanced)",
                "code": "CS101",
                "description": "Comprehensive Python curriculum from basic syntax, data structures, and OOP to decorators, generators, context managers, and asyncio concurrency.",
                "topics": [
                    {
                        "name": "Python Syntax, Variables & Data Types",
                        "difficulty": 1,
                        "importance": 1.0,
                        "questions": [
                            {
                                "question": "Which of the following built-in data types in Python is MUTABLE?",
                                "a": "tuple", "b": "str", "c": "list", "d": "int",
                                "correct": "C",
                                "explanation": "In Python, lists are mutable sequence types allowing elements to be modified in-place.",
                                "sub_concept": "Data Mutability"
                            },
                            {
                                "question": "What is the output of bool([]) in Python?",
                                "a": "True", "b": "False", "c": "None", "d": "TypeError",
                                "correct": "B",
                                "explanation": "Empty containers such as empty lists [], tuples (), and strings '' evaluate to False in boolean context.",
                                "sub_concept": "Truthy & Falsy Values"
                            }
                        ]
                    },
                    {
                        "name": "Control Flow, Loops & Functions",
                        "difficulty": 2,
                        "importance": 1.1,
                        "questions": [
                            {
                                "question": "What does range(1, 10, 2) generate in Python 3?",
                                "a": "[1, 2, 3, 4, 5]", "b": "Sequence: 1, 3, 5, 7, 9", "c": "[2, 4, 6, 8, 10]", "d": "[1, 10, 2]",
                                "correct": "B",
                                "explanation": "range(start, stop, step) produces integers from start (1) up to stop (10 exclusive) in increments of step (2).",
                                "sub_concept": "Range Function"
                            }
                        ]
                    },
                    {
                        "name": "Lists, Tuples, Sets & Dictionaries",
                        "difficulty": 2,
                        "importance": 1.2,
                        "questions": [
                            {
                                "question": "What is the average time complexity of looking up a key in a Python dictionary?",
                                "a": "O(N)", "b": "O(log N)", "c": "O(1)", "d": "O(N^2)",
                                "correct": "C",
                                "explanation": "Python dictionaries use hash tables, providing average O(1) time complexity for key insertion and retrieval.",
                                "sub_concept": "Hash Table Complexity"
                            }
                        ]
                    },
                    {
                        "name": "Object-Oriented Python (Classes & Magic Methods)",
                        "difficulty": 3,
                        "importance": 1.4,
                        "questions": [
                            {
                                "question": "Which magic (dunder) method is called when str(obj) or print(obj) is executed?",
                                "a": "__init__", "b": "__repr__", "c": "__str__", "d": "__call__",
                                "correct": "C",
                                "explanation": "__str__ returns an informal user-friendly string representation of an object.",
                                "sub_concept": "Dunder Methods"
                            }
                        ]
                    },
                    {
                        "name": "Decorators, Generators & Context Managers",
                        "difficulty": 4,
                        "importance": 1.5,
                        "questions": [
                            {
                                "question": "Which keyword is used inside a Python function to turn it into a lazy generator?",
                                "a": "return", "b": "yield", "c": "await", "d": "emit",
                                "correct": "B",
                                "explanation": "The 'yield' statement suspends function execution and returns a value to the caller, resuming state on next iteration.",
                                "sub_concept": "Generators"
                            }
                        ]
                    },
                    {
                        "name": "Asynchronous Programming (asyncio & Concurrency)",
                        "difficulty": 5,
                        "importance": 1.5,
                        "questions": [
                            {
                                "question": "Which Python standard library module provides event-loop-based async and await concurrency?",
                                "a": "threading", "b": "multiprocessing", "c": "asyncio", "d": "concurrent.futures",
                                "correct": "C",
                                "explanation": "asyncio is Python's standard library for writing single-threaded concurrent code using async/await syntax.",
                                "sub_concept": "Async I/O"
                            }
                        ]
                    }
                ]
            },
            {
                "name": "Java Programming (Basic to Advanced)",
                "code": "CS201",
                "description": "Master Java from syntax basics and OOP paradigms to advanced enterprise concepts: Collections Framework, Generics, Multithreading, and Stream API.",
                "topics": [
                    {
                        "name": "Java Syntax, Variables & Primitive Types",
                        "difficulty": 1,
                        "importance": 1.0,
                        "questions": [
                            {
                                "question": "Which primitive data type in Java is used to store 64-bit signed integers?",
                                "a": "int", "b": "long", "c": "short", "d": "double",
                                "correct": "B",
                                "explanation": "In Java, 'long' is a 64-bit signed two's complement integer, while 'int' is 32-bit.",
                                "sub_concept": "Primitive Types"
                            }
                        ]
                    },
                    {
                        "name": "Control Loops, Methods & Logic",
                        "difficulty": 2,
                        "importance": 1.1,
                        "questions": [
                            {
                                "question": "Which loop guarantees that the body executes at least once in Java?",
                                "a": "for loop", "b": "while loop", "c": "do-while loop", "d": "for-each loop",
                                "correct": "C",
                                "explanation": "A do-while loop evaluates its condition at the bottom of the loop body, guaranteeing at least one execution.",
                                "sub_concept": "Loop Execution"
                            }
                        ]
                    },
                    {
                        "name": "Arrays & String Immutability",
                        "difficulty": 2,
                        "importance": 1.2,
                        "questions": [
                            {
                                "question": "Why are String objects in Java considered immutable?",
                                "a": "To save memory via String Constant Pool and ensure thread safety.",
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
                        "name": "OOP Inheritance, Interfaces & Abstract Classes",
                        "difficulty": 3,
                        "importance": 1.4,
                        "questions": [
                            {
                                "question": "Which Java keyword is used by a class to inherit from an interface?",
                                "a": "extends", "b": "implements", "c": "inherits", "d": "using",
                                "correct": "B",
                                "explanation": "In Java, a class uses the 'implements' keyword to fulfill contracts defined by an interface.",
                                "sub_concept": "Interface Inheritance"
                            }
                        ]
                    },
                    {
                        "name": "Polymorphism, Overriding & Dynamic Dispatch",
                        "difficulty": 4,
                        "importance": 1.5,
                        "questions": [
                            {
                                "question": "What distinguishes Method Overriding from Method Overloading in Java?",
                                "a": "Overriding occurs in the same class; Overloading requires inheritance.",
                                "b": "Overriding involves runtime dynamic dispatch with identical method signature in a subclass.",
                                "c": "Overloading changes the return type only.",
                                "d": "There is no difference.",
                                "correct": "B",
                                "explanation": "Method Overriding happens at runtime (Dynamic Binding) when a child class redefines a parent method with exact matching arguments.",
                                "sub_concept": "Dynamic Binding & Overriding"
                            }
                        ]
                    },
                    {
                        "name": "Exception Handling & Custom Exceptions",
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
                    },
                    {
                        "name": "Java Collections Framework & Generics",
                        "difficulty": 4,
                        "importance": 1.4,
                        "questions": [
                            {
                                "question": "Which Map implementation in Java Collections provides O(1) average time complexity and does NOT maintain insertion order?",
                                "a": "TreeMap", "b": "HashMap", "c": "LinkedHashMap", "d": "ConcurrentSkipListMap",
                                "correct": "B",
                                "explanation": "HashMap relies on hashing for O(1) average lookup and does not guarantee element ordering.",
                                "sub_concept": "HashMap Collections"
                            }
                        ]
                    },
                    {
                        "name": "Multithreading, Concurrency & Stream API",
                        "difficulty": 5,
                        "importance": 1.5,
                        "questions": [
                            {
                                "question": "Which Java 8 feature allows functional-style operations (map, filter, reduce) on element streams?",
                                "a": "Reflection API", "b": "Java Streams API", "c": "Servlet API", "d": "JDBC API",
                                "correct": "B",
                                "explanation": "The Java 8 Stream API provides declarative processing pipeline primitives (map, filter, flatMap, reduce).",
                                "sub_concept": "Stream API"
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
                                "question": "What is the time complexity of Binary Search on a sorted array of N elements?",
                                "a": "O(N)", "b": "O(log N)", "c": "O(1)", "d": "O(N log N)",
                                "correct": "B",
                                "explanation": "Binary search halves the remaining search space with each comparison step, leading to logarithmic O(log N) time complexity.",
                                "sub_concept": "Binary Search Complexity"
                            }
                        ]
                    },
                    {
                        "name": "Stacks & Queues",
                        "difficulty": 2,
                        "importance": 1.2,
                        "questions": [
                            {
                                "question": "Which data structure operates on a Last-In, First-Out (LIFO) principle?",
                                "a": "Queue", "b": "Stack", "c": "LinkedList", "d": "PriorityQueue",
                                "correct": "B",
                                "explanation": "Stacks follow LIFO semantics where elements pushed last are popped first.",
                                "sub_concept": "LIFO Semantics"
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
                attempts_count = 2
                acc = 65.0
                recent = 68.0
                status = "Average"
                weakness = 35.0
                confidence = 65.0

                if "Advanced" in t_data["name"] or t_data["difficulty"] >= 4:
                    attempts_count = 3
                    acc = 42.0
                    recent = 40.0
                    status = "Weak"
                    weakness = 60.0
                    confidence = 40.0
                elif t_data["difficulty"] == 1:
                    attempts_count = 4
                    acc = 92.0
                    recent = 95.0
                    status = "Strong"
                    weakness = 8.0
                    confidence = 92.0

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
        print("[OK] Database successfully seeded with Python & Java Basic to Advanced courses!")

    except Exception as e:
        db.rollback()
        print(f"Error seeding database: {e}")
        raise e
    finally:
        db.close()

if __name__ == "__main__":
    seed_database()
