import os
from sqlalchemy.orm import Session
from app.database.session import Base, engine, SessionLocal
from app.models.db_models import (
    User, StudentProfile, Subject, Topic, Question, TopicPerformance, StudyMaterial
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

        print("Seeding Python, Java, DSA (Beginning to Advanced), DBMS subjects, topics, and Study Material...")

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
            learning_goals="Master Python, Java, DSA Beginning to Advanced, and DBMS."
        )
        db.add(demo_profile)

        # 2. Subjects & Topics Data Definitions
        subjects_data = [
            {
                "name": "Python Programming (Basic to Advanced)",
                "code": "CS101",
                "description": "Complete Python curriculum from basic syntax, data structures, and OOP to decorators, generators, context managers, and asyncio concurrency.",
                "topics": [
                    {
                        "name": "Python Syntax, Variables & Data Types",
                        "difficulty": 1,
                        "importance": 1.0,
                        "study_material": {
                            "title": "Python Basics: Syntax, Mutability & Types",
                            "markdown": "Python is a dynamically typed, high-level language. Essential data types include int, float, str, list, tuple, dict, and set. Memory is managed automatically via reference counting and garbage collection.",
                            "code": "name = 'Python'\nx, y = 10, 20\nnumbers = [1, 2, 3] # Mutable\npoint = (10, 20)    # Immutable Tuple\nprint(f'{name} {numbers[0]}')",
                            "cheat_sheet": "• Mutable: list, dict, set\n• Immutable: int, float, str, tuple, frozenset\n• Type Checking: type(obj) or isinstance(obj, Class)"
                        },
                        "questions": [
                            {
                                "question": "Which of the following built-in data types in Python is MUTABLE?",
                                "a": "tuple", "b": "str", "c": "list", "d": "int",
                                "correct": "C",
                                "explanation": "In Python, lists are mutable sequence types allowing elements to be modified in-place.",
                                "sub_concept": "Data Mutability"
                            }
                        ]
                    },
                    {
                        "name": "Control Flow, Loops & Functions",
                        "difficulty": 2,
                        "importance": 1.1,
                        "study_material": {
                            "title": "Python Control Structures & First-Class Functions",
                            "markdown": "Functions in Python are first-class objects. Control structures include if-elif-else, for loops (over iterables), and while loops with break/continue.",
                            "code": "def process_numbers(items):\n    return [x * 2 for x in items if x > 0]\n\nfor i in range(1, 10, 2):\n    print(i)",
                            "cheat_sheet": "• range(start, stop, step): Half-open interval [start, stop)\n• First-Class Functions: Can be passed as args and returned from other functions."
                        },
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
                        "name": "Decorators, Generators & Context Managers",
                        "difficulty": 4,
                        "importance": 1.5,
                        "study_material": {
                            "title": "Advanced Python: Decorators & Lazy Generators",
                            "markdown": "Decorators wrap functions to modify behavior dynamically (@functools.wraps). Generators yield values lazily to minimize memory usage.",
                            "code": "def my_decorator(func):\n    def wrapper(*args, **kwargs):\n        print('Executing...')\n        return func(*args, **kwargs)\n    return wrapper\n\ndef fibonacci():\n    a, b = 0, 1\n    while True:\n        yield a\n        a, b = b, a + b",
                            "cheat_sheet": "• Decorator Syntax: @my_decorator\n• Generators: Memory-efficient lazy evaluation via yield keyword."
                        },
                        "questions": [
                            {
                                "question": "Which keyword is used inside a Python function to turn it into a lazy generator?",
                                "a": "return", "b": "yield", "c": "await", "d": "emit",
                                "correct": "B",
                                "explanation": "The 'yield' statement suspends function execution and returns a value to the caller.",
                                "sub_concept": "Generators"
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
                        "study_material": {
                            "title": "Java Fundamentals & Memory Model",
                            "markdown": "Java is a strongly typed, object-oriented language compiled to bytecode executed on the JVM. Primitive types (int, long, double, boolean) reside on the stack.",
                            "code": "public class Main {\n    public static void main(String[] args) {\n        long counter = 100000L;\n        boolean isActive = true;\n        System.out.println(counter);\n    }\n}",
                            "cheat_sheet": "• Primitives: byte (8b), short (16b), int (32b), long (64b), float (32b), double (64b)\n• Default booleans: false\n• Default object refs: null"
                        },
                        "questions": [
                            {
                                "question": "Which primitive data type in Java is used to store 64-bit signed integers?",
                                "a": "int", "b": "long", "c": "short", "d": "double",
                                "correct": "B",
                                "explanation": "In Java, 'long' is a 64-bit signed integer.",
                                "sub_concept": "Primitive Types"
                            }
                        ]
                    },
                    {
                        "name": "Multithreading, Concurrency & Stream API",
                        "difficulty": 5,
                        "importance": 1.5,
                        "study_material": {
                            "title": "Advanced Java: Multithreading & Stream API",
                            "markdown": "Java provides concurrency primitives (synchronized, ReentrantLock, ExecutorService) and functional streams (map, filter, reduce) for declarative data pipelines.",
                            "code": "List<String> names = List.of('Alice', 'Bob', 'Charlie');\nList<String> filtered = names.stream()\n    .filter(n -> n.length() > 3)\n    .map(String::toUpperCase)\n    .collect(Collectors.toList());",
                            "cheat_sheet": "• Stream API: Lazy evaluation pipeline\n• Thread pool: ExecutorService.newFixedThreadPool(n)\n• Synchronization: synchronized block or volatile keyword"
                        },
                        "questions": [
                            {
                                "question": "Which Java 8 feature allows functional-style operations (map, filter, reduce) on element streams?",
                                "a": "Reflection API", "b": "Java Streams API", "c": "Servlet API", "d": "JDBC API",
                                "correct": "B",
                                "explanation": "The Java 8 Stream API provides declarative processing pipeline primitives.",
                                "sub_concept": "Stream API"
                            }
                        ]
                    }
                ]
            },
            {
                "name": "Data Structures & Algorithms (Beginning to Advanced)",
                "code": "CS202",
                "description": "Complete DSA mastery from asymptotic analysis, arrays, stacks, and binary search trees to graph theory, shortest paths, and dynamic programming.",
                "topics": [
                    {
                        "name": "DSA Foundations, Time & Space Complexity (Big-O, Omega, Theta)",
                        "difficulty": 1,
                        "importance": 1.0,
                        "study_material": {
                            "title": "Asymptotic Analysis & Big-O Notation",
                            "markdown": "Big-O measures upper bound time/space complexity as input size N approaches infinity. Essential complexities: O(1) < O(log N) < O(N) < O(N log N) < O(N^2) < O(2^N).",
                            "code": "# Binary Search: O(log N) Time, O(1) Space\ndef binary_search(arr, target):\n    low, high = 0, len(arr) - 1\n    while low <= high:\n        mid = (low + high) // 2\n        if arr[mid] == target: return mid\n        elif arr[mid] < target: low = mid + 1\n        else: high = mid - 1\n    return -1",
                            "cheat_sheet": "• O(1): Constant\n• O(log N): Binary Search\n• O(N): Linear Scan\n• O(N log N): MergeSort / HeapSort\n• O(N^2): Bubble / Selection Sort"
                        },
                        "questions": [
                            {
                                "question": "What is the time complexity of Binary Search on a sorted array of N elements?",
                                "a": "O(N)", "b": "O(log N)", "c": "O(1)", "d": "O(N log N)",
                                "correct": "B",
                                "explanation": "Binary search halves the search space with each comparison step.",
                                "sub_concept": "Binary Search"
                            }
                        ]
                    },
                    {
                        "name": "Arrays, Strings, Two-Pointers & Sliding Window",
                        "difficulty": 2,
                        "importance": 1.2,
                        "study_material": {
                            "title": "Two-Pointer & Sliding Window Techniques",
                            "markdown": "Sliding window and two-pointer techniques reduce O(N^2) nested loop checks to linear O(N) by maintaining left and right index bounds dynamically.",
                            "code": "def max_sub_array_sum(arr, k):\n    max_sum = cur_sum = sum(arr[:k])\n    for i in range(k, len(arr)):\n        cur_sum += arr[i] - arr[i - k]\n        max_sum = max(max_sum, cur_sum)\n    return max_sum",
                            "cheat_sheet": "• Sliding Window: Subarrays/substrings of size K or dynamic constraints\n• Two Pointers: Sorted array pair search or reversing sequences"
                        },
                        "questions": [
                            {
                                "question": "What is the optimal time complexity of finding a pair with a target sum in a SORTED array using two pointers?",
                                "a": "O(N^2)", "b": "O(N)", "c": "O(log N)", "d": "O(N log N)",
                                "correct": "B",
                                "explanation": "Two pointers starting at opposite ends move inward in linear O(N) time.",
                                "sub_concept": "Two-Pointers"
                            }
                        ]
                    },
                    {
                        "name": "Stacks, Queues, Linked Lists & Hash Tables",
                        "difficulty": 3,
                        "importance": 1.3,
                        "study_material": {
                            "title": "Linear Data Structures & Hashing",
                            "markdown": "Stacks follow LIFO (Last-In-First-Out) and Queues follow FIFO. Linked lists use pointers between nodes. Hash tables map keys to buckets via hash functions.",
                            "code": "class Node:\n    def __init__(self, val):\n        self.val = val\n        self.next = None",
                            "cheat_sheet": "• Stack: LIFO (push/pop O(1))\n• Queue: FIFO (enqueue/dequeue O(1))\n• Hash Table: Lookup O(1) avg"
                        },
                        "questions": [
                            {
                                "question": "Which data structure operates on a Last-In, First-Out (LIFO) principle?",
                                "a": "Queue", "b": "Stack", "c": "LinkedList", "d": "PriorityQueue",
                                "correct": "B",
                                "explanation": "Stacks follow LIFO semantics.",
                                "sub_concept": "LIFO Semantics"
                            }
                        ]
                    },
                    {
                        "name": "Binary Trees, Binary Search Trees (BST) & Heaps",
                        "difficulty": 4,
                        "importance": 1.4,
                        "study_material": {
                            "title": "Hierarchical Data Structures: Trees & Heaps",
                            "markdown": "A BST maintains left < parent < right property. Min/Max Heaps keep the root as min/max element for priority queue operations in O(log N).",
                            "code": "import heapq\nheap = []\nheapq.heappush(heap, 10)\nheapq.heappush(heap, 5)\nmin_val = heapq.heappop(heap) # Returns 5",
                            "cheat_sheet": "• BST Inorder Traversal: Yields sorted order\n• Heap Insert/Extract: O(log N)\n• Top-K Problems: Min-Heap of size K"
                        },
                        "questions": [
                            {
                                "question": "What is the worst-case search time complexity in an UNBALANCED Binary Search Tree (BST)?",
                                "a": "O(1)", "b": "O(log N)", "c": "O(N)", "d": "O(N^2)",
                                "correct": "C",
                                "explanation": "An unbalanced BST degrades into a single linked list chain giving O(N) search.",
                                "sub_concept": "BST Degradation"
                            }
                        ]
                    },
                    {
                        "name": "Graph Algorithms (BFS, DFS, Dijkstra & Shortest Path)",
                        "difficulty": 5,
                        "importance": 1.5,
                        "study_material": {
                            "title": "Graph Traversal & Shortest Path Algorithms",
                            "markdown": "Graphs consist of vertices V and edges E. BFS uses a queue for shortest path in unweighted graphs; DFS uses recursion/stack; Dijkstra's algorithm uses a priority queue for weighted graphs.",
                            "code": "from collections import deque\ndef bfs(graph, start):\n    visited = {start}\n    q = deque([start])\n    while q:\n        node = q.popleft()\n        for neighbor in graph[node]:\n            if neighbor not in visited:\n                visited.add(neighbor)\n                q.append(neighbor)",
                            "cheat_sheet": "• BFS: Shortest path in unweighted graph O(V + E)\n• DFS: Cycle detection, topological sort O(V + E)\n• Dijkstra: Non-negative weighted shortest path O((V + E) log V)"
                        },
                        "questions": [
                            {
                                "question": "Which algorithm is optimal for finding the single-source shortest path in a graph with non-negative edge weights?",
                                "a": "BFS", "b": "Dijkstra's Algorithm", "c": "Bellman-Ford", "d": "Kruskal's Algorithm",
                                "correct": "B",
                                "explanation": "Dijkstra's algorithm efficiently computes shortest paths in non-negative weighted graphs.",
                                "sub_concept": "Shortest Path"
                            }
                        ]
                    },
                    {
                        "name": "Dynamic Programming & Backtracking",
                        "difficulty": 5,
                        "importance": 1.5,
                        "study_material": {
                            "title": "Dynamic Programming & Constraint Backtracking",
                            "markdown": "DP breaks complex problems into overlapping subproblems with optimal substructure. Memoization (top-down) or Tabulation (bottom-up) stores intermediate results.",
                            "code": "# Fibonacci DP Tabulation: O(N) Time, O(1) Space\ndef fib(n):\n    if n <= 1: return n\n    a, b = 0, 1\n    for _ in range(2, n + 1):\n        a, b = b, a + b\n    return b",
                            "cheat_sheet": "• Overlapping Subproblems + Optimal Substructure = DP\n• Memoization: Recursion + Cache\n• Tabulation: Iterative Table"
                        },
                        "questions": [
                            {
                                "question": "What two key properties must a problem satisfy to be solvable using Dynamic Programming?",
                                "a": "Greedy Choice & Sorting", "b": "Overlapping Subproblems & Optimal Substructure", "c": "Divide and Conquer & Parallelism", "d": "LIFO & FIFO",
                                "correct": "B",
                                "explanation": "DP requires overlapping subproblems and optimal substructure.",
                                "sub_concept": "DP Properties"
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
                        "study_material": {
                            "title": "Relational SQL: Joins & Subqueries",
                            "markdown": "SQL joins combine records from two or more tables based on related key attributes (INNER, LEFT, RIGHT, FULL OUTER JOIN).",
                            "code": "SELECT u.full_name, p.recent_score\nFROM users u\nJOIN topic_performance p ON u.id = p.student_id\nWHERE p.accuracy > 75.0;",
                            "cheat_sheet": "• INNER JOIN: Intersection of both tables\n• LEFT JOIN: All left records + matched right records\n• GROUP BY + HAVING: Aggregate filtering"
                        },
                        "questions": [
                            {
                                "question": "Which JOIN returns all rows from the left table and matched records from the right table?",
                                "a": "INNER JOIN", "b": "LEFT OUTER JOIN", "c": "RIGHT OUTER JOIN", "d": "FULL JOIN",
                                "correct": "B",
                                "explanation": "LEFT JOIN returns all records from the left table regardless of right table matches.",
                                "sub_concept": "Outer Joins"
                            }
                        ]
                    }
                ]
            }
        ]

        # Insert subjects, topics, questions, and study materials
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

                # Seed Study Material if provided
                if "study_material" in t_data:
                    sm_info = t_data["study_material"]
                    sm = StudyMaterial(
                        topic_id=topic.id,
                        title=sm_info["title"],
                        content_markdown=sm_info["markdown"],
                        code_snippet=sm_info["code"],
                        cheat_sheet_json=sm_info["cheat_sheet"]
                    )
                    db.add(sm)

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
        print("[OK] Database successfully seeded with Python, Java, DSA Beginning to Advanced, and Study Material!")

    except Exception as e:
        db.rollback()
        print(f"Error seeding database: {e}")
        raise e
    finally:
        db.close()

if __name__ == "__main__":
    seed_database()
