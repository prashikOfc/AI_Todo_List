"""
GUI styles, fonts, and colors for AI To-Do List.
"""

from tkinter import ttk

# Main Color Palette
COLOR_PRIMARY = "#1E40AF"        # Blue
COLOR_PRIMARY_HOVER = "#1D4ED8"
COLOR_BG = "#F1F5F9"             # Soft slate background
COLOR_CARD_BG = "#FFFFFF"        # White panel background
COLOR_BORDER = "#CBD5E1"         # Slate border
COLOR_TEXT_MAIN = "#0F172A"      # Main text
COLOR_TEXT_MUTED = "#64748B"     # Subtitle text

# Colors for Priority Tags (Background, Text)
PRIORITY_COLORS = {
    "HIGH PRIORITY": {
        "bg": "#FEE2E2",
        "fg": "#991B1B",
    },
    "MEDIUM PRIORITY": {
        "bg": "#FEF3C7",
        "fg": "#92400E",
    },
    "LOW PRIORITY": {
        "bg": "#D1FAE5",
        "fg": "#065F46",
    },
    "COMPLETED": {
        "bg": "#E2E8F0",
        "fg": "#475569",
    },
}

# Fonts
FONT_FAMILY = "Segoe UI"
FONT_TITLE = (FONT_FAMILY, 16, "bold")
FONT_SUBTITLE = (FONT_FAMILY, 9)
FONT_BADGE = (FONT_FAMILY, 8, "bold")
FONT_HEADING = (FONT_FAMILY, 11, "bold")
FONT_BODY = (FONT_FAMILY, 9)
FONT_BODY_BOLD = (FONT_FAMILY, 9, "bold")
FONT_CARD_NUM = (FONT_FAMILY, 18, "bold")
FONT_CARD_LABEL = (FONT_FAMILY, 8, "bold")
FONT_CODE = ("Consolas", 9)


def apply_theme(root):
    """Set up the styling for Tkinter and TTK widgets."""
    root.configure(bg=COLOR_BG)

    style = ttk.Style(root)
    if "clam" in style.theme_names():
        style.theme_use("clam")

    # Frames
    style.configure("TFrame", background=COLOR_BG)

    # Labels
    style.configure("TLabel", background=COLOR_BG, foreground=COLOR_TEXT_MAIN, font=FONT_BODY)

    # Primary Button (+ Add Task)
    style.configure(
        "Primary.TButton",
        background=COLOR_PRIMARY,
        foreground="#FFFFFF",
        font=FONT_BODY_BOLD,
        borderwidth=0,
        padding=(10, 6),
    )
    style.map(
        "Primary.TButton",
        background=[("active", COLOR_PRIMARY_HOVER)],
    )

    # Action Buttons (Refresh, Clear)
    style.configure(
        "Action.TButton",
        background="#FFFFFF",
        foreground=COLOR_TEXT_MAIN,
        font=FONT_BODY,
        borderwidth=1,
        padding=(8, 4),
    )

    # Status Buttons
    style.configure(
        "Progress.TButton",
        background="#D97706",
        foreground="#FFFFFF",
        font=FONT_BODY_BOLD,
        borderwidth=0,
        padding=(8, 4),
    )
    style.map("Progress.TButton", background=[("active", "#B45309")])

    style.configure(
        "Success.TButton",
        background="#059669",
        foreground="#FFFFFF",
        font=FONT_BODY_BOLD,
        borderwidth=0,
        padding=(8, 4),
    )
    style.map("Success.TButton", background=[("active", "#047857")])

    style.configure(
        "Danger.TButton",
        background="#DC2626",
        foreground="#FFFFFF",
        font=FONT_BODY_BOLD,
        borderwidth=0,
        padding=(8, 4),
    )
    style.map("Danger.TButton", background=[("active", "#B91C1C")])

    # Treeview Table
    style.configure(
        "Treeview",
        background="#FFFFFF",
        foreground=COLOR_TEXT_MAIN,
        fieldbackground="#FFFFFF",
        font=FONT_BODY,
        rowheight=26,
        borderwidth=0,
    )
    style.configure(
        "Treeview.Heading",
        background="#F8FAFC",
        foreground=COLOR_TEXT_MAIN,
        font=FONT_BODY_BOLD,
        padding=(6, 4),
    )

    return style


apply_styles = apply_theme
