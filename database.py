"""
Database operations for the AI To-Do List application.
Uses Python's built-in sqlite3 with simple parameterized queries.
"""

import os
import sqlite3
from datetime import date, timedelta
from priority_engine import predict_priority
from utils.helpers import get_today_str, calculate_days_remaining

DATABASE_NAME = os.path.join(os.path.dirname(os.path.abspath(__file__)), "todo.db")


def get_connection(db_path=DATABASE_NAME):
    """Return a new SQLite database connection."""
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn


def create_database(db_path=DATABASE_NAME):
    """Create the tasks table if it does not already exist."""
    conn = get_connection(db_path)
    cursor = conn.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT,
            due_date TEXT NOT NULL,
            importance TEXT NOT NULL,
            difficulty TEXT NOT NULL,
            status TEXT NOT NULL,
            priority TEXT NOT NULL,
            created_at TEXT NOT NULL
        )
        """
    )

    conn.commit()
    conn.close()


def add_task(title, description, due_date, importance, difficulty, status, priority, created_at=None, db_path=DATABASE_NAME):
    """Insert a new task into the database."""
    if created_at is None:
        created_at = get_today_str()

    conn = get_connection(db_path)
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO tasks
        (title, description, due_date, importance, difficulty, status, priority, created_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            title.strip(),
            description.strip() if description else "",
            due_date.strip(),
            importance.strip(),
            difficulty.strip(),
            status.strip(),
            priority.strip(),
            created_at.strip(),
        ),
    )

    task_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return task_id


def get_all_tasks(db_path=DATABASE_NAME):
    """Fetch all tasks from the database sorted by priority and due date."""
    conn = get_connection(db_path)
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT * FROM tasks
        ORDER BY 
            CASE priority
                WHEN 'HIGH PRIORITY' THEN 1
                WHEN 'MEDIUM PRIORITY' THEN 2
                WHEN 'LOW PRIORITY' THEN 3
                ELSE 4
            END,
            due_date ASC,
            id DESC
        """
    )

    rows = cursor.fetchall()
    tasks = [dict(row) for row in rows]
    conn.close()
    return tasks


def get_task(task_id, db_path=DATABASE_NAME):
    """Fetch a single task by its ID."""
    conn = get_connection(db_path)
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM tasks WHERE id = ?", (task_id,))
    row = cursor.fetchone()
    conn.close()
    return dict(row) if row else None


def update_task(task_id, title, description, due_date, importance, difficulty, status, priority, db_path=DATABASE_NAME):
    """Update an existing task in the database."""
    conn = get_connection(db_path)
    cursor = conn.cursor()

    cursor.execute(
        """
        UPDATE tasks
        SET title = ?, description = ?, due_date = ?, importance = ?, difficulty = ?, status = ?, priority = ?
        WHERE id = ?
        """,
        (
            title.strip(),
            description.strip() if description else "",
            due_date.strip(),
            importance.strip(),
            difficulty.strip(),
            status.strip(),
            priority.strip(),
            task_id,
        ),
    )

    updated = cursor.rowcount > 0
    conn.commit()
    conn.close()
    return updated


def delete_task(task_id, db_path=DATABASE_NAME):
    """Delete a task by its ID."""
    conn = get_connection(db_path)
    cursor = conn.cursor()

    cursor.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
    deleted = cursor.rowcount > 0

    conn.commit()
    conn.close()
    return deleted


def update_task_status(task_id, status, priority, db_path=DATABASE_NAME):
    """Update only status and priority for a task."""
    conn = get_connection(db_path)
    cursor = conn.cursor()

    cursor.execute(
        """
        UPDATE tasks
        SET status = ?, priority = ?
        WHERE id = ?
        """,
        (status.strip(), priority.strip(), task_id),
    )

    updated = cursor.rowcount > 0
    conn.commit()
    conn.close()
    return updated


def get_task_statistics(db_path=DATABASE_NAME):
    """Calculate task summary counts for cards."""
    conn = get_connection(db_path)
    cursor = conn.cursor()

    cursor.execute("SELECT status, priority FROM tasks")
    rows = cursor.fetchall()
    conn.close()

    total = len(rows)
    completed = 0
    high_priority = 0
    medium_priority = 0
    low_priority = 0

    for row in rows:
        st = (row["status"] or "").strip().lower()
        pr = (row["priority"] or "").strip()

        if st == "completed":
            completed += 1

        if pr == "HIGH PRIORITY":
            high_priority += 1
        elif pr == "MEDIUM PRIORITY":
            medium_priority += 1
        elif pr == "LOW PRIORITY":
            low_priority += 1

    pending = total - completed

    return {
        "total": total,
        "pending": pending,
        "completed": completed,
        "high_priority": high_priority,
        "medium_priority": medium_priority,
        "low_priority": low_priority,
    }


def seed_sample_tasks_if_empty(db_path=DATABASE_NAME):
    """Insert 3 sample tasks if the database table is empty."""
    create_database(db_path)

    conn = get_connection(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) AS count FROM tasks")
    count = cursor.fetchone()["count"]
    conn.close()

    if count > 0:
        return False

    today = date.today()

    sample_tasks = [
        {
            "title": "Complete WAP Assignment",
            "description": "Finish the Web Application Programming assignment.",
            "due_date": (today + timedelta(days=2)).strftime("%Y-%m-%d"),
            "importance": "High",
            "difficulty": "Hard",
            "status": "Pending",
        },
        {
            "title": "Study DBMS",
            "description": "Prepare DBMS topics for examination.",
            "due_date": (today + timedelta(days=7)).strftime("%Y-%m-%d"),
            "importance": "Medium",
            "difficulty": "Medium",
            "status": "In Progress",
        },
        {
            "title": "Read AI Notes",
            "description": "Read introductory AI notes.",
            "due_date": (today + timedelta(days=15)).strftime("%Y-%m-%d"),
            "importance": "Low",
            "difficulty": "Easy",
            "status": "Pending",
        },
    ]

    for item in sample_tasks:
        days_left = calculate_days_remaining(item["due_date"])
        priority = predict_priority(
            days_left,
            item["importance"],
            item["difficulty"],
            item["status"],
        )
        add_task(
            title=item["title"],
            description=item["description"],
            due_date=item["due_date"],
            importance=item["importance"],
            difficulty=item["difficulty"],
            status=item["status"],
            priority=priority,
            db_path=db_path,
        )

    return True
