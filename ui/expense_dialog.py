"""Expense Dialog for adding/editing expenses."""

import tkinter as tk
from tkinter import messagebox
from datetime import datetime
from database import add_expense, update_expense, get_categories
from ui.styles import Styles
from config import DATE_FORMAT
from utils.validators import validate_amount, validate_date

class ExpenseDialog:
    """Dialog for adding/editing expenses."""
    
    def __init__(self, parent, expense_data=None, on_save=None):
        """Initialize dialog."""
        self.parent = parent
        self.expense_data = expense_data
        self.on_save = on_save
        self.categories = get_categories()
        
        self.window = tk.Toplevel(parent)
        self.window.title("Add Expense" if not expense_data else "Edit Expense")
        self.window.geometry("400x350")
        self.window.resizable(False, False)
        
        Styles.configure_styles(self.window)
        
        self.create_widgets()
        
        if expense_data:
            self.populate_fields()
        
        self.window.grab_set()
    
    def create_widgets(self):
        """Create dialog widgets."""
        # Main frame
        main_frame = Styles.create_themed_frame(self.window)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)
        
        # Date
        date_label = Styles.create_themed_label(main_frame, "Date:")
        date_label.grid(row=0, column=0, sticky=tk.W, pady=(0, 5))
        
        self.date_entry = Styles.create_themed_entry(main_frame)
        self.date_entry.insert(0, datetime.now().strftime(DATE_FORMAT))
        self.date_entry.grid(row=0, column=1, sticky=tk.EW, pady=(0, 5))
        
        # Amount
        amount_label = Styles.create_themed_label(main_frame, "Amount:")
        amount_label.grid(row=1, column=0, sticky=tk.W, pady=(0, 5))
        
        self.amount_entry = Styles.create_themed_entry(main_frame)
        self.amount_entry.grid(row=1, column=1, sticky=tk.EW, pady=(0, 5))
        
        # Category
        cat_label = Styles.create_themed_label(main_frame, "Category:")
        cat_label.grid(row=2, column=0, sticky=tk.W, pady=(0, 5))
        
        self.cat_var = tk.StringVar()
        self.cat_combo = tk.OptionMenu(main_frame, self.cat_var, *[c[1] for c in self.categories])
        self.cat_combo.grid(row=2, column=1, sticky=tk.EW, pady=(0, 5))
        if self.categories:
            self.cat_var.set(self.categories[0][1])
        
        # Description
        desc_label = Styles.create_themed_label(main_frame, "Description:")
        desc_label.grid(row=3, column=0, sticky=tk.NW, pady=(0, 5))
        
        self.desc_text = tk.Text(
            main_frame,
            height=4,
            width=30,
            **Styles.get_entry_style()
        )
        self.desc_text.grid(row=3, column=1, sticky=tk.EW, pady=(0, 15))
        
        # Buttons
        button_frame = Styles.create_themed_frame(main_frame)
        button_frame.grid(row=4, column=0, columnspan=2, sticky=tk.EW)
        
        save_btn = Styles.create_themed_button(
            button_frame,
            "Save",
            self.save,
            style='primary',
            width=10
        )
        save_btn.pack(side=tk.RIGHT, padx=(5, 0))
        
        cancel_btn = Styles.create_themed_button(
            button_frame,
            "Cancel",
            self.window.destroy,
            width=10
        )
        cancel_btn.pack(side=tk.RIGHT, padx=5)
        
        main_frame.columnconfigure(1, weight=1)
    
    def populate_fields(self):
        """Populate fields with expense data."""
        exp_id, date, amount, cat_id, desc, cat_name, color = self.expense_data
        
        self.date_entry.delete(0, tk.END)
        self.date_entry.insert(0, date)
        
        self.amount_entry.delete(0, tk.END)
        self.amount_entry.insert(0, str(amount))
        
        self.cat_var.set(cat_name)
        
        self.desc_text.insert(1.0, desc)
    
    def save(self):
        """Save expense."""
        try:
            # Validate
            date = self.date_entry.get().strip()
            amount_str = self.amount_entry.get().strip()
            category = self.cat_var.get()
            description = self.desc_text.get(1.0, tk.END).strip()
            
            if not date or not amount_str or not category:
                messagebox.showerror("Error", "Please fill all required fields")
                return
            
            if not validate_date(date):
                messagebox.showerror("Error", "Invalid date format (YYYY-MM-DD)")
                return
            
            if not validate_amount(amount_str):
                messagebox.showerror("Error", "Invalid amount")
                return
            
            amount = float(amount_str)
            
            # Get category ID
            cat_id = None
            for c in self.categories:
                if c[1] == category:
                    cat_id = c[0]
                    break
            
            # Save
            if self.expense_data:
                exp_id = self.expense_data[0]
                update_expense(exp_id, date, amount, cat_id, description)
                messagebox.showinfo("Success", "Expense updated")
            else:
                add_expense(date, amount, cat_id, description)
                messagebox.showinfo("Success", "Expense added")
            
            if self.on_save:
                self.on_save()
            
            self.window.destroy()
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed: {str(e)}")