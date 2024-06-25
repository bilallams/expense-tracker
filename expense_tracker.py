import pandas as pd
from tkinter import messagebox

class ExpenseTrackerLogic:
    def __init__(self, root):
        self.root = root
        self.data_file = "expenses.csv"
        self.load_data()

    def load_data(self):
        try:
            self.df = pd.read_csv(self.data_file, parse_dates=["Date"])
        except FileNotFoundError:
            self.df = pd.DataFrame(columns=["Date", "Amount", "Description"])

    def save_data(self):
        self.df.to_csv(self.data_file, index=False)
        
    def add_expense(self):
        date = self.date_entry.get()
        amount = self.amount_entry.get()
        description = self.description_entry.get()
        
        try:
            date = pd.to_datetime(date)
            amount = float(amount)
        except ValueError:
            messagebox.showerror("Invalid input", "Please enter valid date and amount.")
            return
        
        new_expense = pd.DataFrame([{"Date": date, "Amount": amount, "Description": description}])
        self.df = pd.concat([self.df, new_expense], ignore_index=True)
        self.save_data()
        messagebox.showinfo("Success", "Expense added successfully!")
        
        self.date_entry.delete(0, tk.END)
        self.amount_entry.delete(0, tk.END)
        self.description_entry.delete(0, tk.END)
