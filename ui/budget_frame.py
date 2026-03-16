import tkinter as tk


class BudgetFrame(tk.Frame):  # ← Inherit from tk.Frame
    def __init__(self, master, on_update=None):
        super().__init__(master)  # ← Call parent constructor
        self.on_update = on_update
        
        self.label = tk.Label(self, text="Budget Management")
        self.label.pack()

        self.budget_entry = tk.Entry(self)
        self.budget_entry.pack()

        self.set_budget_button = tk.Button(self, text="Set Budget", command=self.set_budget)
        self.set_budget_button.pack()

    def set_budget(self):
        budget = self.budget_entry.get()
        print(f"Budget set to: {budget}")
        if self.on_update:
            self.on_update()
