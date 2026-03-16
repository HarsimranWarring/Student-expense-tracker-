"""Main Application Window."""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import csv
from database import get_expenses, delete_expense, get_categories, get_db_connection
from ui.styles import Styles
from ui.expense_dialog import ExpenseDialog
from ui.budget_frame import BudgetFrame
from ui.analytics_frame import AnalyticsFrame
from utils.backup import BackupManager
from utils.helpers import DateHelper, CurrencyHelper

class MainWindow:
    """Main application window."""
    
    def __init__(self, root):
        """Initialize main window."""
        self.root = root
        self.categories = get_categories()
        
        Styles.configure_styles(root)
        
        self.create_menu()
        self.create_widgets()
        self.load_expenses()
    
    def create_menu(self):
        """Create menu bar."""
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        # File menu
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        
        file_menu.add_command(label="Export to CSV", command=self.export_csv)
        file_menu.add_command(label="Backup Data", command=self.backup_data)
        file_menu.add_command(label="Restore Data", command=self.restore_data)
        file_menu.add_separator()
        file_menu.add_command(label="Clear All", command=self.clear_all)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit)
        
        # Help menu
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="About", command=self.show_about)
    
    def create_widgets(self):
        """Create main widgets."""
        # Main frame
        main_frame = Styles.create_themed_frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Header
        header_frame = Styles.create_themed_frame(main_frame)
        header_frame.pack(fill=tk.X, padx=15, pady=15)
        
        title = Styles.create_themed_label(
            header_frame,
            "Student Expense Tracker",
            font=Styles.TITLE_FONT
        )
        title.pack(side=tk.LEFT)
        
        add_btn = Styles.create_themed_button(
            header_frame,
            "+ Add Expense",
            self.add_expense,
            style='primary',
            width=15
        )
        add_btn.pack(side=tk.RIGHT, padx=5)
        
        # Notebook
        self.notebook = ttk.Notebook(main_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=15, pady=(0, 15))
        
        # Expenses tab
        self.exp_frame = Styles.create_themed_frame(self.notebook)
        self.notebook.add(self.exp_frame, text="Expenses")
        self.create_expenses_tab()
        
        # Budget tab
        self.budget_frame = BudgetFrame(self.notebook, on_update=self.refresh_all)
        self.notebook.add(self.budget_frame, text="Budget")
        
        # Analytics tab
        self.analytics_frame = AnalyticsFrame(self.notebook)
        self.notebook.add(self.analytics_frame, text="Analytics")
    
    def create_expenses_tab(self):
        """Create expenses tab."""
        # Filter
        filter_frame = Styles.create_themed_frame(self.exp_frame)
        filter_frame.pack(fill=tk.X, padx=15, pady=15)
        
        filter_label = Styles.create_themed_label(filter_frame, "Filter by Category:")
        filter_label.pack(side=tk.LEFT, padx=(0, 10))
        
        self.filter_var = tk.StringVar(value="All")
        self.cat_combo = ttk.Combobox(
            filter_frame,
            textvariable=self.filter_var,
            values=["All"] + [c[1] for c in self.categories],
            state='readonly',
            width=20
        )
        self.cat_combo.pack(side=tk.LEFT, padx=5)
        self.cat_combo.bind('<<ComboboxSelected>>', lambda e: self.load_expenses())
        
        refresh_btn = Styles.create_themed_button(
            filter_frame,
            "Refresh",
            self.load_expenses,
            style='primary',
            width=10
        )
        refresh_btn.pack(side=tk.LEFT, padx=5)
        
        # Table
        table_frame = Styles.create_themed_frame(self.exp_frame)
        table_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=(0, 15))
        
        columns = ("Date", "Category", "Amount", "Description")
        self.tree = ttk.Treeview(table_frame, columns=columns, height=15, show='headings')
        
        self.tree.heading("Date", text="Date")
        self.tree.heading("Category", text="Category")
        self.tree.heading("Amount", text="Amount")
        self.tree.heading("Description", text="Description")
        
        self.tree.column("Date", width=100)
        self.tree.column("Category", width=150)
        self.tree.column("Amount", width=100)
        self.tree.column("Description", width=300)
        
        scrollbar = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.tree.bind('<Double-1>', self.edit_from_tree)
        self.tree.bind('<Delete>', self.delete_from_tree)
    
    def load_expenses(self):
        """Load expenses."""
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        cat_filter = self.filter_var.get()
        cat_id = None
        
        if cat_filter != "All":
            for c in self.categories:
                if c[1] == cat_filter:
                    cat_id = c[0]
                    break
        
        expenses = get_expenses(category_id=cat_id)
        
        for exp in expenses:
            exp_id, date, amount, cat_id, desc, cat_name, color = exp
            
            self.tree.insert(
                '',
                'end',
                values=(
                    DateHelper.format_date_display(date),
                    cat_name,
                    CurrencyHelper.format_currency(amount),
                    desc[:50] + "..." if len(desc) > 50 else desc
                ),
                tags=(exp_id,)
            )
    
    def add_expense(self):
        """Add expense."""
        ExpenseDialog(self.root, on_save=self.load_expenses)
    
    def edit_from_tree(self, event):
        """Edit from tree."""
        sel = self.tree.selection()
        if not sel:
            return
        
        tags = self.tree.item(sel[0], 'tags')
        if tags:
            exp_id = int(tags[0])
            expenses = get_expenses()
            for exp in expenses:
                if exp[0] == exp_id:
                    ExpenseDialog(self.root, expense_data=exp, on_save=self.load_expenses)
                    break
    
    def delete_from_tree(self, event):
        """Delete from tree."""
        sel = self.tree.selection()
        if not sel:
            return
        
        if messagebox.askyesno("Confirm", "Delete this expense?"):
            tags = self.tree.item(sel[0], 'tags')
            if tags:
                delete_expense(int(tags[0]))
                self.load_expenses()
    
    def export_csv(self):
        """Export to CSV."""
        expenses = get_expenses()
        
        if not expenses:
            messagebox.showinfo("Info", "No expenses to export")
            return
        
        path = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
        )
        
        if not path:
            return
        
        try:
            with open(path, 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(["Date", "Category", "Amount", "Description"])
                
                for exp in expenses:
                    writer.writerow([exp[1], exp[5], f"{exp[2]:.2f}", exp[4]])
            
            messagebox.showinfo("Success", f"Exported to {path}")
        except Exception as e:
            messagebox.showerror("Error", f"Export failed: {str(e)}")
    
    def backup_data(self):
        """Backup data."""
        success, msg = BackupManager.create_backup()
        if success:
            messagebox.showinfo("Success", msg)
        else:
            messagebox.showerror("Error", msg)
    
    def restore_data(self):
        """Restore data."""
        backups = BackupManager.get_available_backups()
        
        if not backups:
            messagebox.showinfo("Info", "No backups available")
            return
        
        path = filedialog.askopenfilename(
            initialdir=str(backups[0].parent) if backups else ".",
            filetypes=[("Database files", "*.db"), ("All files", "*.*")]
        )
        
        if not path:
            return
        
        if messagebox.askyesno("Confirm", "Restore from backup?"):
            success, msg = BackupManager.restore_backup(path)
            if success:
                messagebox.showinfo("Success", msg)
                self.load_expenses()
            else:
                messagebox.showerror("Error", msg)
    
    def clear_all(self):
        """Clear all expenses."""
        if messagebox.askyesno("Confirm", "Delete ALL expenses? Cannot undo!"):
            if messagebox.askyesno("Final", "Really delete all?"):
                conn = get_db_connection()
                cursor = conn.cursor()
                try:
                    cursor.execute("DELETE FROM expenses")
                    conn.commit()
                    messagebox.showinfo("Success", "All data cleared")
                    self.load_expenses()
                except Exception as e:
                    messagebox.showerror("Error", f"Failed: {str(e)}")
                finally:
                    conn.close()
    
    def show_about(self):
        """Show about dialog."""
        messagebox.showinfo(
            "About",
            "Student Expense Tracker v1.0\n\n"
            "Professional expense tracking application\n\n"
            "Features:\n"
            "• Expense tracking\n"
            "• Budget management\n"
            "• Analytics\n"
            "• Data backup\n\n"
            "Built with Python, Tkinter & SQLite"
        )
    
    def refresh_all(self):
        """Refresh all displays."""
        self.load_expenses()
        self.analytics_frame.refresh_analytics()