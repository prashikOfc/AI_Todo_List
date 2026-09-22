"""
Rule-Based Intelligent Decision Engine for AI To-Do List.
Calculates priority scores using simple, explainable rules.
"""


def get_deadline_score(days_remaining):
    """Return points based on days remaining until deadline."""
    if days_remaining <= 2:
        return 5
    elif days_remaining <= 5:
        return 4
    elif days_remaining <= 10:
        return 2
    else:
        return 1


def get_importance_score(importance):
    """Return points based on task importance."""
    importance_str = str(importance).strip().capitalize()
    if importance_str == "High":
        return 3
    elif importance_str == "Medium":
        return 2
    return 1


def get_difficulty_score(difficulty):
    """Return points based on task difficulty."""
    difficulty_str = str(difficulty).strip().capitalize()
    if difficulty_str == "Hard":
        return 3
    elif difficulty_str == "Medium":
        return 2
    return 1


def get_status_score(status):
    """Return points based on task progress status."""
    status_str = str(status).strip().title()
    if status_str == "In Progress":
        return 3
    elif status_str == "Pending":
        return 2
    return 0


def get_score_breakdown(days_remaining, importance, difficulty, status):
    """Return a dictionary showing how each factor contributed to the score."""
    deadline_score = get_deadline_score(days_remaining)
    importance_score = get_importance_score(importance)
    difficulty_score = get_difficulty_score(difficulty)
    status_score = get_status_score(status)
    total_score = deadline_score + importance_score + difficulty_score + status_score

    return {
        "deadline_score": deadline_score,
        "importance_score": importance_score,
        "difficulty_score": difficulty_score,
        "status_score": status_score,
        "total_score": total_score,
    }


def predict_priority(days_remaining, importance, difficulty, status):
    """
    Predict task priority using rule-based scoring:
      - If completed -> COMPLETED
      - Total Score >= 9 -> HIGH PRIORITY
      - Total Score 6 to 8 -> MEDIUM PRIORITY
      - Total Score <= 5 -> LOW PRIORITY
    """
    if str(status).strip().capitalize() == "Completed":
        return "COMPLETED"

    score = (
        get_deadline_score(days_remaining)
        + get_importance_score(importance)
        + get_difficulty_score(difficulty)
        + get_status_score(status)
    )

    if score >= 9:
        return "HIGH PRIORITY"
    elif score >= 6:
        return "MEDIUM PRIORITY"
    else:
        return "LOW PRIORITY"


def get_priority_reason(days_remaining, importance, difficulty, status):
    """Return a clear explanation of why the task received this priority."""
    if str(status).strip().capitalize() == "Completed":
        return "Task is completed, so no urgent action is needed."

    priority = predict_priority(days_remaining, importance, difficulty, status)
    breakdown = get_score_breakdown(days_remaining, importance, difficulty, status)
    total = breakdown["total_score"]

    if days_remaining < 0:
        time_text = "the task is overdue"
    elif days_remaining == 0:
        time_text = "the task is due today"
    elif days_remaining == 1:
        time_text = "the task is due in 1 day"
    else:
        time_text = f"the task is due in {days_remaining} days"

    diff_str = str(difficulty).strip().capitalize()
    if diff_str == "Hard":
        diff_text = "is difficult"
    elif diff_str == "Medium":
        diff_text = "has medium difficulty"
    else:
        diff_text = "is easy"

    imp_str = str(importance).strip().lower()
    st_str = str(status).strip().lower()

    return (
        f"{priority.title()} because {time_text}, "
        f"has {imp_str} importance, {diff_text}, "
        f"and is currently {st_str} (score: {total}/14)."
    )


# Backward-compatible function aliases
calculate_deadline_score = get_deadline_score
calculate_importance_score = get_importance_score
calculate_difficulty_score = get_difficulty_score
calculate_status_score = get_status_score
