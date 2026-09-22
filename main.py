"""
To-Do List
Clean, professional desktop To-Do List application.
Built using Python, Tkinter, and SQLite.
"""

import os
import sys
import tkinter as tk
from tkinter import ttk, messagebox

# Add project folder to sys.path
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

import database
from priority_engine import predict_priority
from utils.helpers import get_today_str, validate_date, calculate_days_remaining, format_days_remaining
from ui.styles import (
    COLOR_PRIMARY,
    COLOR_BG,
    COLOR_CARD_BG,
    COLOR_BORDER,
    COLOR_TEXT_MAIN,
    COLOR_TEXT_MUTED,
    PRIORITY_COLORS,
    FONT_TITLE,
    FONT_HEADING,
    FONT_BODY,
    FONT_BODY_BOLD,
    FONT_CARD_NUM,
    FONT_CARD_LABEL,
    apply_theme,
)


class AITodoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("To-Do List")
        self.root.geometry("1100x720")
        self.root.minsize(1050, 680)

        # Apply styles
        self.style = apply_theme(self.root)

        # Initialize database
        database.create_database()
        database.seed_sample_tasks_if_empty()

        # Track selected task
        self.selected_task_id = None

        # Build GUI sections
        self.create_header()
        self.create_summary_cards()
        self.create_main_layout()

        # Load tasks on startup
        self.refresh_tasks()

    def create_header(self):
        """Simple top header banner."""
        header_frame = tk.Frame(self.root, bg="#FFFFFF", highlightbackground=COLOR_BORDER, highlightthickness=1)
        header_frame.pack(fill="x", side="top", padx=16, pady=(12, 8))

        title_lbl = tk.Label(header_frame, text="To-Do List", font=FONT_TITLE, fg=COLOR_PRIMARY, bg="#FFFFFF")
        title_lbl.pack(anchor="center", pady=10)

    def create_summary_cards(self):
        """Build the 4 summary count cards: Total, Pending, High Priority, Completed."""
        container = tk.Frame(self.root, bg=COLOR_BG)
        container.pack(fill="x", padx=16, pady=(0, 8))

        self.cards = {}
        card_items = [
            ("total", "TOTAL", "#1E40AF"),
            ("pending", "PENDING", "#D97706"),
            ("high_priority", "HIGH PRIORITY", "#DC2626"),
            ("completed", "COMPLETED", "#059669"),
        ]

        container.grid_columnconfigure(0, weight=1)
        container.grid_columnconfigure(1, weight=1)
        container.grid_columnconfigure(2, weight=1)
        container.grid_columnconfigure(3, weight=1)

        for col, (key, title, color) in enumerate(card_items):
            card = tk.Frame(container, bg="#FFFFFF", highlightbackground=COLOR_BORDER, highlightthickness=1)
            card.grid(row=0, column=col, padx=(0 if col == 0 else 6, 0 if col == 3 else 6), sticky="nsew")

            inner = tk.Frame(card, bg="#FFFFFF")
            inner.pack(fill="both", expand=True, padx=12, pady=8)

            lbl_title = tk.Label(inner, text=title, font=FONT_CARD_LABEL, fg=COLOR_TEXT_MUTED, bg="#FFFFFF")
            lbl_title.pack(anchor="w")

            lbl_num = tk.Label(inner, text="0", font=FONT_CARD_NUM, fg=color, bg="#FFFFFF")
            lbl_num.pack(anchor="w", pady=(2, 0))

            self.cards[key] = lbl_num

    def create_main_layout(self):
        """Create the left form and right dashboard container."""
        main_frame = tk.Frame(self.root, bg=COLOR_BG)
        main_frame.pack(fill="both", expand=True, padx=16, pady=(0, 12))

        # Left panel for task input form
        left_panel = tk.Frame(
            main_frame,
            bg=COLOR_CARD_BG,
            highlightbackground=COLOR_BORDER,
            highlightthickness=1,
            width=320,
        )
        left_panel.pack(side="left", fill="y", padx=(0, 8))
        left_panel.pack_propagate(False)

        self.create_task_form(left_panel)

        # Right panel for task table and details
        right_panel = tk.Frame(main_frame, bg=COLOR_BG)
        right_panel.pack(side="right", fill="both", expand=True)

        self.create_dashboard(right_panel)

    def create_task_form(self, parent):
        """Build the task entry form."""
        form = tk.Frame(parent, bg=COLOR_CARD_BG)
        form.pack(fill="both", expand=True, padx=14, pady=12)

        heading = tk.Label(form, text="Add Task", font=FONT_HEADING, fg=COLOR_PRIMARY, bg=COLOR_CARD_BG)
        heading.pack(anchor="w", pady=(0, 10))

        # Task Title
        tk.Label(form, text="Task Title *", font=FONT_BODY_BOLD, bg=COLOR_CARD_BG, fg=COLOR_TEXT_MAIN).pack(anchor="w")
        self.entry_title = ttk.Entry(form, font=FONT_BODY)
        self.entry_title.pack(fill="x", pady=(2, 8))

        # Description
        tk.Label(form, text="Description", font=FONT_BODY, bg=COLOR_CARD_BG, fg=COLOR_TEXT_MAIN).pack(anchor="w")
        self.entry_desc = ttk.Entry(form, font=FONT_BODY)
        self.entry_desc.pack(fill="x", pady=(2, 8))

        # Due Date
        tk.Label(form, text="Due Date *", font=FONT_BODY_BOLD, bg=COLOR_CARD_BG, fg=COLOR_TEXT_MAIN).pack(anchor="w")
        self.entry_due_date = ttk.Entry(form, font=FONT_BODY)
        self.entry_due_date.insert(0, get_today_str())
        self.entry_due_date.pack(fill="x", pady=(2, 8))

        # Importance
        tk.Label(form, text="Importance", font=FONT_BODY_BOLD, bg=COLOR_CARD_BG, fg=COLOR_TEXT_MAIN).pack(anchor="w")
        self.combo_importance = ttk.Combobox(form, values=["Low", "Medium", "High"], state="readonly", font=FONT_BODY)
        self.combo_importance.set("Medium")
        self.combo_importance.pack(fill="x", pady=(2, 8))

        # Difficulty
        tk.Label(form, text="Difficulty", font=FONT_BODY_BOLD, bg=COLOR_CARD_BG, fg=COLOR_TEXT_MAIN).pack(anchor="w")
        self.combo_difficulty = ttk.Combobox(form, values=["Easy", "Medium", "Hard"], state="readonly", font=FONT_BODY)
        self.combo_difficulty.set("Medium")
        self.combo_difficulty.pack(fill="x", pady=(2, 8))

        # Status
        tk.Label(form, text="Status", font=FONT_BODY_BOLD, bg=COLOR_CARD_BG, fg=COLOR_TEXT_MAIN).pack(anchor="w")
        self.combo_status = ttk.Combobox(form, values=["Pending", "In Progress", "Completed"], state="readonly", font=FONT_BODY)
        self.combo_status.set("Pending")
        self.combo_status.pack(fill="x", pady=(2, 14))

        # Buttons
        ttk.Button(form, text="Add Task", style="Primary.TButton", command=self.add_task).pack(fill="x", pady=(0, 6))
        ttk.Button(form, text="Clear", style="Action.TButton", command=self.clear_form).pack(fill="x")

    def create_dashboard(self, parent):
        """Assemble the task table and task details panel."""
        self.create_task_table(parent)
        self.create_task_details_panel(parent)

    def create_task_table(self, parent):
        """Build the task table with scrollbars and action buttons."""
        dashboard_frame = tk.Frame(parent, bg=COLOR_CARD_BG, highlightbackground=COLOR_BORDER, highlightthickness=1)
        dashboard_frame.pack(fill="both", expand=True)

        top_bar = tk.Frame(dashboard_frame, bg=COLOR_CARD_BG)
        top_bar.pack(fill="x", padx=12, pady=(10, 6))

        tk.Label(top_bar, text="Tasks", font=FONT_HEADING, fg=COLOR_PRIMARY, bg=COLOR_CARD_BG).pack(side="left")
        self.lbl_task_count = tk.Label(top_bar, text="", font=FONT_CARD_LABEL, fg=COLOR_TEXT_MUTED, bg=COLOR_CARD_BG)
        self.lbl_task_count.pack(side="right")

        tree_container = tk.Frame(dashboard_frame, bg=COLOR_CARD_BG)
        tree_container.pack(fill="both", expand=True, padx=12, pady=(0, 8))

        columns = ("id", "title", "due_date", "days_left", "importance", "difficulty", "status", "priority")
        self.tree = ttk.Treeview(tree_container, columns=columns, show="headings", selectmode="browse")

        col_configs = [
            ("id", "ID", 45, "center"),
            ("title", "Task", 195, "w"),
            ("due_date", "Due Date", 85, "center"),
            ("days_left", "Days Left", 80, "center"),
            ("importance", "Importance", 85, "center"),
            ("difficulty", "Difficulty", 80, "center"),
            ("status", "Status", 95, "center"),
            ("priority", "Priority", 130, "center"),
        ]

        for col_id, col_text, width, anchor in col_configs:
            self.tree.heading(col_id, text=col_text, anchor=anchor)
            self.tree.column(col_id, width=width, minwidth=width - 15, anchor=anchor)

        v_scroll = ttk.Scrollbar(tree_container, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=v_scroll.set)

        self.tree.pack(side="left", fill="both", expand=True)
        v_scroll.pack(side="right", fill="y")

        # Color tags for priorities
        for prio_name, color_cfg in PRIORITY_COLORS.items():
            self.tree.tag_configure(prio_name, background=color_cfg["bg"], foreground=color_cfg["fg"])

        self.tree.bind("<<TreeviewSelect>>", self.on_task_selected)

        # Action buttons
        self.create_action_buttons(dashboard_frame)

    def create_action_buttons(self, parent):
        """Build the buttons below the table."""
        action_bar = tk.Frame(parent, bg=COLOR_CARD_BG)
        action_bar.pack(fill="x", padx=12, pady=(0, 10))

        ttk.Button(action_bar, text="Refresh", style="Action.TButton", command=self.refresh_tasks).pack(side="left", padx=(0, 6))
        ttk.Button(action_bar, text="Mark In Progress", style="Progress.TButton", command=self.mark_in_progress).pack(
            side="left", padx=(0, 6)
        )
        ttk.Button(action_bar, text="Mark Completed", style="Success.TButton", command=self.mark_completed).pack(
            side="left", padx=(0, 6)
        )
        ttk.Button(action_bar, text="Delete Task", style="Danger.TButton", command=self.delete_task).pack(side="right")

    def create_task_details_panel(self, parent):
        """Build the bottom Task Details panel."""
        self.details_panel = tk.Frame(parent, bg=COLOR_CARD_BG, highlightbackground=COLOR_BORDER, highlightthickness=1, height=145)
        self.details_panel.pack(fill="x", pady=(8, 0))
        self.details_panel.pack_propagate(False)

        header_row = tk.Frame(self.details_panel, bg=COLOR_CARD_BG)
        header_row.pack(fill="x", padx=14, pady=(8, 4))

        tk.Label(header_row, text="Task Details", font=FONT_HEADING, fg=COLOR_PRIMARY, bg=COLOR_CARD_BG).pack(side="left")
        self.lbl_selected_priority = tk.Label(header_row, text="", font=FONT_BODY_BOLD, padx=8, pady=2, bg=COLOR_CARD_BG)
        self.lbl_selected_priority.pack(side="right")

        self.details_content = tk.Frame(self.details_panel, bg=COLOR_CARD_BG)
        self.details_content.pack(fill="both", expand=True, padx=14, pady=(0, 8))

        # Initial placeholder
        self.lbl_placeholder = tk.Label(
            self.details_content,
            text="Select a task from the list above to view its details.",
            font=FONT_BODY,
            fg=COLOR_TEXT_MUTED,
            bg=COLOR_CARD_BG,
        )
        self.lbl_placeholder.pack(anchor="w", pady=14)

        # Info Frame for task attributes
        self.info_frame = tk.Frame(self.details_content, bg=COLOR_CARD_BG)

        # Row 1: Title, Due Date, Status
        self.lbl_detail_title = tk.Label(self.info_frame, text="", font=FONT_BODY_BOLD, bg=COLOR_CARD_BG, fg=COLOR_TEXT_MAIN)
        self.lbl_detail_title.grid(row=0, column=0, sticky="w", padx=(0, 20), pady=1)

        self.lbl_detail_date = tk.Label(self.info_frame, text="", font=FONT_BODY, bg=COLOR_CARD_BG, fg=COLOR_TEXT_MAIN)
        self.lbl_detail_date.grid(row=0, column=1, sticky="w", padx=(0, 20), pady=1)

        self.lbl_detail_status = tk.Label(self.info_frame, text="", font=FONT_BODY, bg=COLOR_CARD_BG, fg=COLOR_TEXT_MAIN)
        self.lbl_detail_status.grid(row=0, column=2, sticky="w", pady=1)

        # Row 2: Importance, Difficulty, Priority
        self.lbl_detail_meta = tk.Label(self.info_frame, text="", font=FONT_BODY, bg=COLOR_CARD_BG, fg=COLOR_TEXT_MUTED)
        self.lbl_detail_meta.grid(row=1, column=0, columnspan=3, sticky="w", pady=(2, 4))

        # Row 3: Why this priority? (Simple natural sentence)
        self.lbl_reason = tk.Label(
            self.info_frame,
            text="",
            font=FONT_BODY,
            fg=COLOR_TEXT_MAIN,
            bg="#F8FAFC",
            padx=8,
            pady=4,
            relief="flat",
            highlightbackground=COLOR_BORDER,
            highlightthickness=1,
        )
        self.lbl_reason.grid(row=2, column=0, columnspan=3, sticky="ew", pady=(2, 0))

    # Backward compatibility for old method name
    create_reasoning_panel = create_task_details_panel

    # -------------------------------------------------------------------------
    # APPLICATION LOGIC & ACTIONS
    # -------------------------------------------------------------------------
    def refresh_tasks(self):
        """Reload tasks from SQLite and update summary cards."""
        stats = database.get_task_statistics()
        self.cards["total"].config(text=str(stats["total"]))
        self.cards["pending"].config(text=str(stats["pending"]))
        self.cards["high_priority"].config(text=str(stats["high_priority"]))
        self.cards["completed"].config(text=str(stats["completed"]))

        tasks = database.get_all_tasks()
        self.lbl_task_count.config(text=f"{len(tasks)} tasks")

        prev_id = self.selected_task_id

        for item in self.tree.get_children():
            self.tree.delete(item)

        item_to_reselect = None

        for task in tasks:
            days_left = calculate_days_remaining(task["due_date"])
            formatted_days = format_days_remaining(days_left)

            row_id = self.tree.insert(
                "",
                "end",
                iid=str(task["id"]),
                values=(
                    task["id"],
                    task["title"],
                    task["due_date"],
                    formatted_days,
                    task["importance"],
                    task["difficulty"],
                    task["status"],
                    task["priority"],
                ),
                tags=(task["priority"],),
            )

            if prev_id and task["id"] == prev_id:
                item_to_reselect = row_id

        if item_to_reselect and self.tree.exists(item_to_reselect):
            self.tree.selection_set(item_to_reselect)
            self.tree.focus(item_to_reselect)
            self.on_task_selected()
        else:
            self.reset_details_panel()

    def on_task_selected(self, event=None):
        """Called when a user clicks a row in the table."""
        selection = self.tree.selection()
        if not selection:
            self.reset_details_panel()
            return

        task_id = int(selection[0])
        self.selected_task_id = task_id
        self.show_task_details(task_id)

    def show_task_details(self, task_id):
        """Display details for the selected task."""
        task = database.get_task(task_id)
        if not task:
            self.reset_details_panel()
            return

        days_left = calculate_days_remaining(task["due_date"])
        formatted_days = format_days_remaining(days_left)
        priority = task["priority"]
        importance = task["importance"]
        difficulty = task["difficulty"]
        status = task["status"]

        self.lbl_placeholder.pack_forget()

        # Priority badge color
        color = PRIORITY_COLORS.get(priority, {"bg": "#E2E8F0", "fg": "#0F172A"})
        self.lbl_selected_priority.config(text=f"  {priority}  ", bg=color["bg"], fg=color["fg"])

        # Title & Date & Status
        self.lbl_detail_title.config(text=f"Task: {task['title']}")
        self.lbl_detail_date.config(text=f"Due: {task['due_date']} ({formatted_days})")
        self.lbl_detail_status.config(text=f"Status: {status}")

        # Metadata
        self.lbl_detail_meta.config(
            text=f"Importance: {importance}   •   Difficulty: {difficulty}"
        )

        # Simple explanation for "Why this priority?"
        if status == "Completed":
            simple_reason = "Task is completed."
        elif days_left < 0:
            simple_reason = f"Overdue task with {importance.lower()} importance and {difficulty.lower()} difficulty."
        elif days_left <= 2:
            simple_reason = f"Due soon ({formatted_days}) and marked as {importance.lower()} importance."
        elif days_left <= 5:
            simple_reason = f"Approaching deadline with {importance.lower()} importance."
        else:
            simple_reason = f"Due in {days_left} days with {importance.lower()} importance and {difficulty.lower()} difficulty."

        self.lbl_reason.config(text=f"Why this priority?  {simple_reason}")
        self.info_frame.pack(fill="x")

    def reset_details_panel(self):
        """Clear details panel and restore placeholder."""
        self.selected_task_id = None
        self.lbl_selected_priority.config(text="", bg=COLOR_CARD_BG)
        self.info_frame.pack_forget()
        self.lbl_placeholder.pack(anchor="w", pady=14)

    # Backward compatibility
    show_task_reason = show_task_details
    reset_reasoning_panel = reset_details_panel

    def add_task(self):
        """Validate form, calculate priority, and save to SQLite."""
        title = self.entry_title.get().strip()
        description = self.entry_desc.get().strip()
        due_date = self.entry_due_date.get().strip()
        importance = self.combo_importance.get().strip()
        difficulty = self.combo_difficulty.get().strip()
        status = self.combo_status.get().strip()

        if not title:
            messagebox.showwarning("Validation Error", "Please enter a Task Title.")
            self.entry_title.focus_set()
            return

        if not due_date:
            messagebox.showwarning("Validation Error", "Please enter a Due Date (YYYY-MM-DD).")
            self.entry_due_date.focus_set()
            return

        if not validate_date(due_date):
            messagebox.showerror("Invalid Date", "Please enter a valid date in YYYY-MM-DD format.")
            self.entry_due_date.focus_set()
            return

        # Calculate priority
        days_left = calculate_days_remaining(due_date)
        priority = predict_priority(days_left, importance, difficulty, status)

        # Save into SQLite
        task_id = database.add_task(
            title=title,
            description=description,
            due_date=due_date,
            importance=importance,
            difficulty=difficulty,
            status=status,
            priority=priority,
        )

        self.selected_task_id = task_id
        self.refresh_tasks()
        self.clear_form()

        if self.tree.exists(str(task_id)):
            self.tree.selection_set(str(task_id))
            self.tree.focus(str(task_id))
            self.on_task_selected()

        messagebox.showinfo("Success", f"Task '{title}' added successfully!")

    def mark_in_progress(self):
        """Change selected task status to In Progress and recalculate priority."""
        selection = self.tree.selection()
        if not selection:
            messagebox.showwarning("Selection Required", "Please select a task first.")
            return

        task_id = int(selection[0])
        task = database.get_task(task_id)
        if not task:
            return

        days_left = calculate_days_remaining(task["due_date"])
        new_priority = predict_priority(days_left, task["importance"], task["difficulty"], "In Progress")

        database.update_task_status(task_id, "In Progress", new_priority)
        self.refresh_tasks()

    def mark_completed(self):
        """Change selected task status to Completed."""
        selection = self.tree.selection()
        if not selection:
            messagebox.showwarning("Selection Required", "Please select a task first.")
            return

        task_id = int(selection[0])
        database.update_task_status(task_id, "Completed", "COMPLETED")
        self.refresh_tasks()

    def delete_task(self):
        """Delete selected task after user confirmation."""
        selection = self.tree.selection()
        if not selection:
            messagebox.showwarning("Selection Required", "Please select a task first.")
            return

        task_id = int(selection[0])
        task = database.get_task(task_id)
        task_title = task["title"] if task else f"ID {task_id}"

        confirm = messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete:\n'{task_title}'?", icon="warning")
        if confirm:
            database.delete_task(task_id)
            self.selected_task_id = None
            self.refresh_tasks()

    def clear_form(self):
        """Reset form fields to default values."""
        self.entry_title.delete(0, tk.END)
        self.entry_desc.delete(0, tk.END)
        self.entry_due_date.delete(0, tk.END)
        self.entry_due_date.insert(0, get_today_str())
        self.combo_importance.set("Medium")
        self.combo_difficulty.set("Medium")
        self.combo_status.set("Pending")
        self.entry_title.focus_set()

    # Function aliases
    refresh_all = refresh_tasks
    on_add_task = add_task
    on_delete_task = delete_task
    on_mark_in_progress = mark_in_progress
    on_mark_completed = mark_completed


def main():
    root = tk.Tk()
    app = AITodoApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
