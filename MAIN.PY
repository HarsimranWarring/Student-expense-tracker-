"""
Student Expense Tracker - Main Application Entry Point
GUI-based expense tracking application using Tkinter and SQLite
"""

import tkinter as tk
from tkinter import messagebox
from database import init_db
from ui.main_window import MainWindow
from config import APP_TITLE, APP_WIDTH, APP_HEIGHT

def main():
    """Initialize and run the application."""
    try:
        # Initialize database
        init_db()
        
        # Create root window
        root = tk.Tk()
        root.title(APP_TITLE)
        root.geometry(f"{APP_WIDTH}x{APP_HEIGHT}")
        root.minsize(900, 600)
        
        # Set window icon (if available)
        try:
            root.iconbitmap('assets/icon.ico')
        except:
            pass
        
        # Initialize main window
        app = MainWindow(root)
        
        # Run application
        root.mainloop()
        
    except Exception as e:
        messagebox.showerror("Error", f"Failed to start application: {str(e)}")

if __name__ == "__main__":
    main()
