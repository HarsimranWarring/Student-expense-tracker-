"""UI Styles and Theming."""

import tkinter as tk
from config import DARK_BG, DARK_FG, DARK_ENTRY_BG, DARK_BUTTON_BG

class Styles:
    """UI styling constants and helper methods."""
    
    TITLE_FONT = ("Helvetica", 18, "bold")
    HEADING_FONT = ("Helvetica", 14, "bold")
    NORMAL_FONT = ("Helvetica", 10)
    SMALL_FONT = ("Helvetica", 9)
    
    @staticmethod
    def get_frame_style():
        """Get frame style."""
        return {"bg": DARK_BG}
    
    @staticmethod
    def get_label_style():
        """Get label style."""
        return {"bg": DARK_BG, "fg": DARK_FG}
    
    @staticmethod
    def get_entry_style():
        """Get entry style."""
        return {"bg": DARK_ENTRY_BG, "fg": DARK_FG, "insertbackground": DARK_FG}
    
    @staticmethod
    def create_themed_frame(parent):
        """Create themed frame."""
        return tk.Frame(parent, **Styles.get_frame_style())
    
    @staticmethod
    def create_themed_label(parent, text, font=None):
        """Create themed label."""
        if font is None:
            font = Styles.NORMAL_FONT
        return tk.Label(parent, text=text, font=font, **Styles.get_label_style())
    
    @staticmethod
    def create_themed_entry(parent, width=20):
        """Create themed entry."""
        return tk.Entry(parent, width=width, **Styles.get_entry_style())
    
    @staticmethod
    def create_themed_button(parent, text, command, style='normal', width=10):
        """Create themed button."""
        if style == 'primary':
            return tk.Button(
                parent,
                text=text,
                command=command,
                width=width,
                bg=DARK_BUTTON_BG,
                fg="white",
                relief=tk.FLAT,
                padx=10,
                pady=5,
                font=Styles.NORMAL_FONT
            )
        else:
            return tk.Button(
                parent,
                text=text,
                command=command,
                width=width,
                bg=DARK_ENTRY_BG,
                fg=DARK_FG,
                relief=tk.FLAT,
                padx=10,
                pady=5,
                font=Styles.NORMAL_FONT
            )
    
    @staticmethod
    def configure_styles(root):
        """Configure root window styles."""
        root.configure(bg=DARK_BG)
        root.option_add("*Background", DARK_BG)
        root.option_add("*Foreground", DARK_FG)