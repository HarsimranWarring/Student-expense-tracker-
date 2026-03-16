"""
Configuration and constants for Student Expense Tracker
"""

import os
from pathlib import Path

# Application settings
APP_TITLE = "Student Expense Tracker"
APP_WIDTH = 1200
APP_HEIGHT = 700

# Database settings
DB_DIR = Path("data")
DB_FILE = DB_DIR / "expenses.db"
BACKUP_DIR = DB_DIR / "backups"

# Create directories
DB_DIR.mkdir(exist_ok=True)
BACKUP_DIR.mkdir(exist_ok=True)

# Date formats
DATE_FORMAT = "%Y-%m-%d"
DISPLAY_DATE_FORMAT = "%d/%m/%Y"

# Currency settings
CURRENCY_SYMBOL = "₹"
DECIMAL_PLACES = 2

# Default categories
DEFAULT_CATEGORIES = [
    {"name": "Food", "color": "#FF6B6B"},
    {"name": "Transport", "color": "#4ECDC4"},
    {"name": "Entertainment", "color": "#45B7D1"},
    {"name": "Utilities", "color": "#FFA07A"},
    {"name": "Health", "color": "#98D8C8"},
    {"name": "Shopping", "color": "#F7DC6F"},
    {"name": "Education", "color": "#BB8FCE"},
    {"name": "Other", "color": "#95A5A6"},
]

# UI Themes
DARK_BG = "#1E1E1E"
DARK_FG = "#FFFFFF"
DARK_ENTRY_BG = "#2D2D2D"
DARK_ENTRY_FG = "#FFFFFF"
DARK_BUTTON_BG = "#0088CC"
DARK_BUTTON_FG = "#FFFFFF"

# Budget alert levels
BUDGET_OK = "#27AE60"       # Green
BUDGET_WARNING = "#F39C12"  # Orange
BUDGET_EXCEEDED = "#E74C3C" # Red
