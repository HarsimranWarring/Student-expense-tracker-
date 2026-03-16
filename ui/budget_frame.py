class BudgetFrame:
    def __init__(self, master, on_update=None):
        self.master = master
        self.on_update = on_update
        self.frame = tk.Frame(master)
        self.frame.pack()

        self.label = tk.Label(self.frame, text="Budget Management")
        self.label.pack()

        self.budget_entry = tk.Entry(self.frame)
        self.budget_entry.pack()

        self.set_budget_button = tk.Button(self.frame, text="Set Budget", command=self.set_budget)
        self.set_budget_button.pack()

    def set_budget(self):
        budget = self.budget_entry.get()
        print(f"Budget set to: {budget}")
        # Additional logic to manage the budget goes here.
