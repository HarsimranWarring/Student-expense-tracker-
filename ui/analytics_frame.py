import tkinter as tk
from tkinter import ttk


class AnalyticsFrame(tk.Frame):  # ← Inherit from tk.Frame
    def __init__(self, master):
        super().__init__(master)  # ← Call parent constructor
        self.master = master
        
        # Create widgets
        label = tk.Label(self, text="Analytics Frame")
        label.pack(pady=10)
        
        # Add analytics widgets here
        info_label = tk.Label(
            self, 
            text="Analytics and reports will be displayed here",
            font=("Arial", 10)
        )
        info_label.pack(pady=20)
    
    def refresh_analytics(self):
        """Refresh analytics display."""
        pass
