# AI To-Do List - Intelligent Task Prioritizer

A clean, modern, beginner-friendly desktop application that organizes tasks and automatically prioritizes them using an explainable **Rule-Based Intelligent Decision Engine**. Built strictly with Python's standard library, working completely offline without external APIs or cloud dependencies.

---

> [!IMPORTANT]
> **Academic & AI Viva Disclaimer:**  
> **This project is a rule-based intelligent system. It does not use machine learning, deep learning, or external AI APIs.**  
> Artificial intelligence concepts can also be implemented using knowledge-based and rule-based expert systems. This project demonstrates automated decision-making and inference using structured knowledge and predefined rules. No trained ML weights or statistical models are claimed.

---

## 1. Project Title
**AI To-Do List - Intelligent Task Prioritizer**

## 2. Project Description
Managing academic assignments, study schedules, and project deadlines can quickly overwhelm students. Standard to-do list applications simply order tasks chronologically or leave prioritization to manual guessing.

The **AI To-Do List** functions as a personal task prioritization assistant. It takes objective facts about each task (urgency, importance, difficulty, progress status) and passes them through an internal knowledge base of heuristic decision rules. The system calculates a weighted multi-factor score, infers an appropriate priority category (**HIGH PRIORITY**, **MEDIUM PRIORITY**, **LOW PRIORITY**, or **COMPLETED**), and generates a human-readable explanation of why that priority was assigned.

## 3. Objective
- Provide an offline, zero-dependency task prioritizer for students.
- Demonstrate core classical Artificial Intelligence (Symbolic AI / Expert Systems) concepts.
- Provide transparent, explainable recommendations (Explainable AI / XAI).
- Store and manage task persistence locally using SQLite.

## 4. Features
- **Intelligent Priority Inference**: Automatically computes priority levels based on multi-criteria heuristic scoring.
- **Explainable AI (XAI) Panel**: Shows exactly why a task received its priority along with a numerical score breakdown.
- **Real-Time Summary Cards**: Displays dynamic counts for Total Tasks, Pending Tasks, High Priority Tasks, and Completed Tasks.
- **Clean Desktop GUI**: Modern, uncluttered interface built using `tkinter` and `ttk` with custom color-coded badges.
- **Dynamic Sample Data**: Automatically pre-populates three relative academic tasks if launched with an empty database.
- **Task Lifecycle Management**: Quick status toggles (`Mark In Progress`, `Mark Completed`), editing, and safe deletion with confirmation.
- **Robust Input Validation**: Validates date formats (`YYYY-MM-DD`), non-empty titles, and catches invalid calendar dates.
- **100% Offline & Private**: Zero network requests; all data remains in a local SQLite file (`todo.db`).

## 5. Technologies
This project uses **only the standard library modules** included with standard Python distributions (Python 3.8+):

| Technology | Purpose | External Dependency? |
|---|---|---|
| **Python 3.8+** | Core programming language | None |
| **tkinter & ttk** | Graphical User Interface (GUI) widgets & styling | None (Standard Library) |
| **sqlite3** | Local relational database storage | None (Standard Library) |
| **datetime** | Date arithmetic, calendar parsing, and validation | None (Standard Library) |
| **unittest** | Unit testing suite with isolated temporary databases | None (Standard Library) |

---

## 6. System Architecture & AI Pipeline

In symbolic Artificial Intelligence and Expert Systems, intelligent behavior is achieved through the interaction between **Input Facts**, a **Knowledge Base**, and an **Inference Engine**.

```
+-------------------------------------------------------------+
|                         User Input                          |
|       (Title, Due Date, Importance, Difficulty, Status)     |
+-------------------------------------------------------------+
                              |
                              v
+-------------------------------------------------------------+
|                         Task Facts                          |
| (days_remaining: int, importance: str, difficulty, status)  |
+-------------------------------------------------------------+
                              |
                              v
+-------------------------------------------------------------+
|                      Knowledge / Rules                      |
|         (Scoring tables, urgency weights, thresholds)       |
+-------------------------------------------------------------+
                              |
                              v
+-------------------------------------------------------------+
|                       Priority Engine                       |
|           (Evaluates rules against task facts)              |
+-------------------------------------------------------------+
                              |
                              v
+-------------------------------------------------------------+
|                     Inference Mechanism                     |
|           Total Score = Sum of Factor Weights               |
+-------------------------------------------------------------+
                              |
               +--------------+--------------+
               |                             |
               v                             v
+-----------------------------+ +-----------------------------+
|      Priority Decision      | |         Explanation         |
|  "HIGH", "MEDIUM", "LOW"    | |  "High priority because..." |
+-----------------------------+ +-----------------------------+
```

### Core AI Concepts Demonstrated:
1. **Facts**: Concrete properties of an instance (e.g., $2\text{ days remaining}$, $\text{High importance}$, $\text{Hard difficulty}$, $\text{Pending status}$).
2. **Knowledge Base**: Declarative domain rules formulated to reflect human scheduling heuristics.
3. **Inference Engine**: Evaluates facts against the rule base to deduce a classification.
4. **Explanation Facility (XAI)**: Traces the reasoning behind the deduction so the student understands the recommendation.

---

## 7. How Priority Prediction Works

When a task is created or updated:
1. The system extracts the due date and computes the remaining days:
   $$\text{days\_remaining} = \text{due\_date} - \text{today}$$
2. The progress status is checked. If $\text{status} = \text{"Completed"}$, the priority is immediately assigned as **COMPLETED** without further calculation.
3. For active tasks, the system computes points across four independent dimensions:
   - **Deadline Urgency**
   - **Importance Level**
   - **Difficulty / Effort**
   - **Current Status**
4. The points are summed into a **Total Priority Score** (ranging from $4$ to $14$).
5. Threshold rules classify the total score into high, medium, or low urgency tiers.

---

## 8. Scoring Formula & Rule Set

### A. Deadline Score ($\le 5$ pts)
Urgency increases as the deadline approaches:
| Days Remaining | Points | Rationale |
|---|---|---|
| $\le 0\text{ days}$ (Overdue or Due Today) | **5 pts** | Critical urgency; immediate action required |
| $1\text{ to }2\text{ days}$ | **5 pts** | Extremely urgent; due very soon |
| $3\text{ to }5\text{ days}$ | **4 pts** | Moderately urgent; approaching quickly |
| $6\text{ to }10\text{ days}$ | **2 pts** | Upcoming; requires monitoring |
| $> 10\text{ days}$ | **1 pt** | Distant deadline; low urgency |

### B. Importance Score ($\le 3$ pts)
Subjective significance of the task:
| Importance Level | Points |
|---|---|
| **Low** | **1 pt** |
| **Medium** | **2 pts** |
| **High** | **3 pts** |

### C. Difficulty Score ($\le 3$ pts)
Estimated effort required to complete the task:
| Difficulty Level | Points | Rationale |
|---|---|---|
| **Easy** | **1 pt** | Can be executed quickly |
| **Medium** | **2 pts** | Requires standard focus and effort |
| **Hard** | **3 pts** | Requires substantial time and cognitive effort |

### D. Status Score ($\le 3$ pts)
Current operational state:
| Status | Points | Rationale |
|---|---|---|
| **Pending** | **2 pts** | Not yet begun; needs initiation |
| **In Progress** | **3 pts** | Active work already underway; finish to clear cognitive load |
| **Completed** | **0 pts** | No further action required |

---

### Final Classification Thresholds

$$\text{Total Score} = \text{Deadline Score} + \text{Importance Score} + \text{Difficulty Score} + \text{Status Score}$$

| Total Score Range | Assigned Priority | Visual Tag |
|---|---|---|
| **$\ge 9$ points** | **HIGH PRIORITY** | Light Red background, Dark Red text |
| **$6\text{ to }8$ points** | **MEDIUM PRIORITY** | Light Amber background, Dark Amber text |
| **$\le 5$ points** | **LOW PRIORITY** | Light Green background, Dark Green text |
| **Status is "Completed"** | **COMPLETED** | Light Slate background, Dark Gray text |

---

## 9. Database Structure

The project uses a single SQLite table named `tasks` stored inside `todo.db`:

```sql
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
);
```

### Field Descriptions:
- `id`: Auto-incrementing unique identifier.
- `title`: Short task name (mandatory).
- `description`: Optional extra notes or instructions.
- `due_date`: Target completion date in `YYYY-MM-DD` ISO format.
- `importance`: Selected importance tier (`Low`, `Medium`, `High`).
- `difficulty`: Selected difficulty tier (`Easy`, `Medium`, `Hard`).
- `status`: Progress state (`Pending`, `In Progress`, `Completed`).
- `priority`: Assigned classification (`HIGH PRIORITY`, `MEDIUM PRIORITY`, `LOW PRIORITY`, `COMPLETED`).
- `created_at`: Date stamp when the task was added.

---

## 10. How to Run

### Prerequisites
- Python 3.8 or higher installed on your computer.
- No `pip install` commands are needed.

### Running the Desktop GUI
Open your terminal (PowerShell, Command Prompt, or Bash) in the project directory:

```powershell
cd C:\Users\prash\.gemini\antigravity\scratch\AI_Todo_List
python main.py
```

### Running Automated Tests
Run the standalone unit test suite:

```powershell
python test_suite.py
```
All 21 test cases execute within ~0.2 seconds against an isolated temporary database.

---

## 11. Example Walkthrough

### Scenario 1: Urgent Assignment
- **Title**: Complete WAP Assignment
- **Due Date**: $2\text{ days from today}$
- **Importance**: High
- **Difficulty**: Hard
- **Status**: Pending

**AI Evaluation**:
- Deadline Score = $5$ (due in 2 days)
- Importance Score = $3$ (High)
- Difficulty Score = $3$ (Hard)
- Status Score = $2$ (Pending)
- **Total Score** = $5 + 3 + 3 + 2 = 13$
- **Classification**: **HIGH PRIORITY** ($\ge 9$)
- **Generated Reason**: *"High priority because the task is due in 2 days, has high importance, is difficult, and is currently pending (total score: 13/14)."*

---

### Scenario 2: Future Reading Task
- **Title**: Read AI Notes
- **Due Date**: $15\text{ days from today}$
- **Importance**: Low
- **Difficulty**: Easy
- **Status**: Pending

**AI Evaluation**:
- Deadline Score = $1$ ($>10\text{ days}$)
- Importance Score = $1$ (Low)
- Difficulty Score = $1$ (Easy)
- Status Score = $2$ (Pending)
- **Total Score** = $1 + 1 + 1 + 2 = 5$
- **Classification**: **LOW PRIORITY** ($\le 5$)
- **Generated Reason**: *"Low priority because the task is due in 15 days, has low importance, is easy to complete, and is currently pending (total score: 5/14)."*

---

## 12. Limitations
1. **Static Rules**: The scoring weights are fixed and do not adapt over time to individual user habits.
2. **Deterministic Inputs**: The engine relies on accurate user input for difficulty and importance.
3. **Single User / Local Only**: SQLite is stored locally on disk; there is no cloud synchronization across devices.
4. **Coarse-grained Time**: Deadlines are measured in whole calendar days rather than exact hours and minutes.

---

## 13. Viva Questions & Answers for Students

### Q1: Is this project using Machine Learning?
**Answer:** No. Machine Learning algorithms (such as Decision Trees, Neural Networks, or Naive Bayes) learn patterns from historical training datasets. This project is a **Rule-Based Expert System**—a classical branch of Symbolic Artificial Intelligence. It uses human domain expertise formalized into deterministic inference rules.

### Q2: Why is a Rule-Based System considered Artificial Intelligence?
**Answer:** In AI history, intelligence is defined as rational decision-making by an agent. Rule-based expert systems (like MYCIN or DENDRAL) were among the first successful AI systems. They exhibit intelligent behavior by mapping perceived environmental facts (due dates, task difficulty) to goal-directed actions (prioritization), and providing explanations for their decisions.

### Q3: What is Explainable AI (XAI) and how is it implemented here?
**Answer:** Explainable AI refers to methods that allow human users to understand and trust the outputs created by an intelligent system. Many deep learning models are "black boxes". In this project, full explainability is achieved through the **AI Priority Reasoning Panel**, which exposes the exact mathematical score breakdown and a natural language justification for every decision.

### Q4: Why did you choose SQLite over other databases?
**Answer:** SQLite is embedded directly into the Python standard library. It requires zero setup, no server process, no network port, and stores data safely in a single self-contained file (`todo.db`). This makes the application portable, reliable, and completely offline.

### Q5: How does the system handle overdue tasks?
**Answer:** If a task's due date is earlier than today, `calculate_days_remaining()` returns a negative integer. The engine's deadline scoring rule maps any non-positive day count ($\le 0$) to the maximum urgency score of $5$ points, ensuring overdue tasks immediately bubble up to the top of the priority list.

### Q6: Can this system be converted into a Machine Learning system in the future?
**Answer:** Yes. If user interaction logs are collected over time (e.g., recorded completion times, actual stress levels, overdue rates), a supervised learning classifier (such as a Random Forest or Logistic Regression model) could be trained to predict priorities based on historical patterns.

---

## Project Structure

```
AI_Todo_List/
├── main.py                # Main Tkinter desktop application entry point
├── database.py            # SQLite database layer with parameterized queries
├── priority_engine.py     # Rule-based intelligent decision engine
├── requirements.txt       # Explanatory file stating Python standard library usage
├── README.md              # Comprehensive documentation and viva guide
├── test_suite.py          # Complete unit test suite using unittest
├── ui/
│   ├── __init__.py
│   └── styles.py          # Color schemes, ttk themes, and widget styling
└── utils/
    ├── __init__.py
    └── helpers.py         # Date parsing, days remaining calculations, formatting
```
