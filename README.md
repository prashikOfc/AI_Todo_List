# AI To-Do List

A simple desktop To-Do List application built with Python, Tkinter, and SQLite.

The application automatically assigns a priority to each task using a rule-based priority engine based on deadline, importance, difficulty, and task status.

## Features

- Add and manage tasks
- Automatic task priority calculation
- High, Medium, and Low priority levels
- Mark tasks as In Progress or Completed
- Delete tasks
- View task details and priority reasoning
- SQLite database for local data storage
- Clean desktop interface using Tkinter
- Works completely offline
- No external APIs or AI services required

## How Priority Works

The priority engine considers four factors:

| Factor | Description |
|---|---|
| Deadline | How close the task is to its due date |
| Importance | Low, Medium, or High |
| Difficulty | Easy, Medium, or Hard |
| Status | Pending, In Progress, or Completed |

The system calculates a score from these factors and assigns a priority.

### Priority Levels

- **High Priority** — Score 9 or above
- **Medium Priority** — Score 6 to 8
- **Low Priority** — Score 5 or below
- **Completed** — Assigned when the task is completed

## Technologies Used

- **Python**
- **Tkinter** — Desktop GUI
- **SQLite** — Local database
- **unittest** — Testing

No external Python packages are required.

## Project Structure

```text
AI_Todo_List/
│
├── main.py
├── database.py
├── priority_engine.py
├── test_suite.py
├── requirements.txt
├── README.md
│
├── ui/
│   ├── __init__.py
│   └── styles.py
│
└── utils/
    ├── __init__.py
    └── helpers.py
```

## How to Run

### 1. Clone the repository

```bash
git clone https://github.com/prashikOfc/AI_Todo_List.git
```

### 2. Open the project

```bash
cd AI_Todo_List
```

### 3. Run the application

```bash
python main.py
```

The To-Do List desktop application will open.

## Run Tests

To run the automated tests:

```bash
python test_suite.py
```

## AI Concept

This project does not use Machine Learning or external AI APIs.

The "AI" part is implemented as a **rule-based decision system**. It uses predefined rules to analyze task information and automatically determine the priority of each task.

This demonstrates a simple form of intelligent decision-making using Python.

## Database

The application uses SQLite to store tasks locally.

The database file is created automatically when the application runs.

## Future Improvements

- Task editing
- Search and filtering
- Task categories
- Notifications and reminders
- Custom priority rules
- Graphical statistics

## Author

**Prashik Ingle**

MCA (Artificial Intelligence) Student

GitHub: https://github.com/prashikOfc