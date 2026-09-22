"""
Date helper functions for AI To-Do List.
Uses Python's standard datetime module.
"""

from datetime import date, datetime


def get_today_str():
    """Return today's date in YYYY-MM-DD format."""
    return date.today().strftime("%Y-%m-%d")


def validate_date(date_string):
    """Check if a date string is in valid YYYY-MM-DD format."""
    if not date_string or not isinstance(date_string, str):
        return False
    try:
        parsed = datetime.strptime(date_string.strip(), "%Y-%m-%d")
        return 1900 <= parsed.year <= 9999
    except ValueError:
        return False


def calculate_days_remaining(due_date):
    """Calculate how many days are left until the due date."""
    today = date.today()
    if isinstance(due_date, str):
        due = datetime.strptime(due_date.strip(), "%Y-%m-%d").date()
    elif isinstance(due_date, datetime):
        due = due_date.date()
    else:
        due = due_date
    return (due - today).days


def format_days_remaining(days):
    """Format the number of days into a readable string."""
    if days < 0:
        return "Overdue"
    elif days == 0:
        return "Due today"
    elif days == 1:
        return "1 day"
    else:
        return f"{days} days"
