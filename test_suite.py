"""
Unit tests for AI To-Do List application.
Uses Python's standard unittest module and an isolated temporary database.
"""

import os
import sys
import tempfile
import unittest
from datetime import date, timedelta

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

import database
from priority_engine import (
    get_deadline_score,
    get_importance_score,
    get_difficulty_score,
    get_status_score,
    get_score_breakdown,
    predict_priority,
    get_priority_reason,
)
from utils.helpers import (
    get_today_str,
    validate_date,
    calculate_days_remaining,
    format_days_remaining,
)


class TestPriorityEngine(unittest.TestCase):
    """Test priority scoring and decision logic."""

    def test_deadline_scoring(self):
        # 0 or fewer days
        self.assertEqual(get_deadline_score(-5), 5)
        self.assertEqual(get_deadline_score(0), 5)
        # 1-2 days
        self.assertEqual(get_deadline_score(1), 5)
        self.assertEqual(get_deadline_score(2), 5)
        # 3-5 days
        self.assertEqual(get_deadline_score(3), 4)
        self.assertEqual(get_deadline_score(5), 4)
        # 6-10 days
        self.assertEqual(get_deadline_score(6), 2)
        self.assertEqual(get_deadline_score(10), 2)
        # More than 10 days
        self.assertEqual(get_deadline_score(11), 1)
        self.assertEqual(get_deadline_score(25), 1)

    def test_importance_scoring(self):
        self.assertEqual(get_importance_score("High"), 3)
        self.assertEqual(get_importance_score("Medium"), 2)
        self.assertEqual(get_importance_score("Low"), 1)

    def test_difficulty_scoring(self):
        self.assertEqual(get_difficulty_score("Hard"), 3)
        self.assertEqual(get_difficulty_score("Medium"), 2)
        self.assertEqual(get_difficulty_score("Easy"), 1)

    def test_status_scoring(self):
        self.assertEqual(get_status_score("In Progress"), 3)
        self.assertEqual(get_status_score("Pending"), 2)
        self.assertEqual(get_status_score("Completed"), 0)

    def test_score_breakdown(self):
        # 2 days (5) + High (3) + Hard (3) + Pending (2) = 13
        breakdown = get_score_breakdown(2, "High", "Hard", "Pending")
        self.assertEqual(breakdown["deadline_score"], 5)
        self.assertEqual(breakdown["importance_score"], 3)
        self.assertEqual(breakdown["difficulty_score"], 3)
        self.assertEqual(breakdown["status_score"], 2)
        self.assertEqual(breakdown["total_score"], 13)

    def test_predict_priority_categories(self):
        # High Priority: score >= 9
        self.assertEqual(predict_priority(2, "High", "Hard", "Pending"), "HIGH PRIORITY")

        # Medium Priority: score 6 to 8
        self.assertEqual(predict_priority(7, "Medium", "Medium", "Pending"), "MEDIUM PRIORITY")

        # Low Priority: score <= 5
        self.assertEqual(predict_priority(15, "Low", "Easy", "Pending"), "LOW PRIORITY")

        # Completed: always COMPLETED
        self.assertEqual(predict_priority(1, "High", "Hard", "Completed"), "COMPLETED")

    def test_priority_reason(self):
        reason = get_priority_reason(2, "High", "Hard", "Pending")
        self.assertIn("High Priority because", reason)
        self.assertIn("due in 2 days", reason)
        self.assertIn("high importance", reason)
        self.assertIn("is difficult", reason)


class TestDateHelpers(unittest.TestCase):
    """Test date parsing, validation, and remaining days calculations."""

    def test_get_today_str(self):
        self.assertEqual(get_today_str(), date.today().strftime("%Y-%m-%d"))

    def test_validate_date(self):
        self.assertTrue(validate_date("2026-10-15"))
        self.assertTrue(validate_date("2024-02-29"))  # Leap year
        self.assertFalse(validate_date("2023-02-29")) # Non-leap year
        self.assertFalse(validate_date("invalid-date"))
        self.assertFalse(validate_date(""))

    def test_calculate_days_remaining(self):
        today = date.today()
        future = (today + timedelta(days=4)).strftime("%Y-%m-%d")
        past = (today - timedelta(days=2)).strftime("%Y-%m-%d")

        self.assertEqual(calculate_days_remaining(future), 4)
        self.assertEqual(calculate_days_remaining(past), -2)

    def test_format_days_remaining(self):
        self.assertEqual(format_days_remaining(0), "Due today")
        self.assertEqual(format_days_remaining(1), "1 day")
        self.assertEqual(format_days_remaining(5), "5 days")
        self.assertEqual(format_days_remaining(-2), "Overdue")


class TestDatabaseOperations(unittest.TestCase):
    """Test SQLite CRUD operations and statistics using an isolated test DB."""

    def setUp(self):
        self.temp_db_fd, self.temp_db_path = tempfile.mkstemp(suffix=".db")
        database.create_database(self.temp_db_path)

    def tearDown(self):
        os.close(self.temp_db_fd)
        if os.path.exists(self.temp_db_path):
            try:
                os.remove(self.temp_db_path)
            except OSError:
                pass

    def test_add_and_get_task(self):
        task_id = database.add_task(
            title="Lab Assignment",
            description="Write python code",
            due_date="2026-10-01",
            importance="High",
            difficulty="Hard",
            status="Pending",
            priority="HIGH PRIORITY",
            db_path=self.temp_db_path,
        )
        self.assertGreater(task_id, 0)

        task = database.get_task(task_id, db_path=self.temp_db_path)
        self.assertIsNotNone(task)
        self.assertEqual(task["title"], "Lab Assignment")
        self.assertEqual(task["priority"], "HIGH PRIORITY")

    def test_update_task(self):
        task_id = database.add_task(
            title="Old Title",
            description="",
            due_date="2026-10-01",
            importance="Low",
            difficulty="Easy",
            status="Pending",
            priority="LOW PRIORITY",
            db_path=self.temp_db_path,
        )

        database.update_task(
            task_id=task_id,
            title="New Title",
            description="Added notes",
            due_date="2026-10-05",
            importance="High",
            difficulty="Hard",
            status="In Progress",
            priority="HIGH PRIORITY",
            db_path=self.temp_db_path,
        )

        updated = database.get_task(task_id, db_path=self.temp_db_path)
        self.assertEqual(updated["title"], "New Title")
        self.assertEqual(updated["importance"], "High")

    def test_update_status(self):
        task_id = database.add_task(
            title="Read Chapter",
            description="",
            due_date="2026-10-01",
            importance="Low",
            difficulty="Easy",
            status="Pending",
            priority="LOW PRIORITY",
            db_path=self.temp_db_path,
        )

        database.update_task_status(task_id, "Completed", "COMPLETED", db_path=self.temp_db_path)
        task = database.get_task(task_id, db_path=self.temp_db_path)
        self.assertEqual(task["status"], "Completed")
        self.assertEqual(task["priority"], "COMPLETED")

    def test_delete_task(self):
        task_id = database.add_task(
            title="Delete Me",
            description="",
            due_date="2026-10-01",
            importance="Low",
            difficulty="Easy",
            status="Pending",
            priority="LOW PRIORITY",
            db_path=self.temp_db_path,
        )

        self.assertTrue(database.delete_task(task_id, db_path=self.temp_db_path))
        self.assertIsNone(database.get_task(task_id, db_path=self.temp_db_path))

    def test_statistics(self):
        database.add_task("Task 1", "", "2026-10-01", "High", "Hard", "Pending", "HIGH PRIORITY", db_path=self.temp_db_path)
        database.add_task("Task 2", "", "2026-10-02", "Medium", "Medium", "In Progress", "HIGH PRIORITY", db_path=self.temp_db_path)
        database.add_task("Task 3", "", "2026-10-03", "Low", "Easy", "Completed", "COMPLETED", db_path=self.temp_db_path)

        stats = database.get_task_statistics(self.temp_db_path)
        self.assertEqual(stats["total"], 3)
        self.assertEqual(stats["pending"], 2)
        self.assertEqual(stats["completed"], 1)
        self.assertEqual(stats["high_priority"], 2)

    def test_seed_sample_tasks(self):
        seeded = database.seed_sample_tasks_if_empty(self.temp_db_path)
        self.assertTrue(seeded)

        tasks = database.get_all_tasks(self.temp_db_path)
        self.assertEqual(len(tasks), 3)

        # Seeding a second time does not duplicate tasks
        self.assertFalse(database.seed_sample_tasks_if_empty(self.temp_db_path))


if __name__ == "__main__":
    unittest.main()
