import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import pandas as pd
from expense_tracker import ExpenseTrackerLogic
import matplotlib.pyplot as plt

class ExpenseTracker(ExpenseTrackerLogic):
    def __init__(self, root):
        super().__init__(root)
        self.root = root
        self.create_ui()
        
    def create_ui(self):
        self.root.title("Suivi des Dépenses")
        
        # Date input
        self.date_label = ttk.Label(self.root, text="Date (YYYY-MM-DD):")
        self.date_label.grid(row=0, column=0, padx=10, pady=10)
        self.date_entry = ttk.Entry(self.root)
        self.date_entry.grid(row=0, column=1, padx=10, pady=10)
        
        # Amount input
        self.amount_label = ttk.Label(self.root, text="Amount:")
        self.amount_label.grid(row=1, column=0, padx=10, pady=10)
        self.amount_entry = ttk.Entry(self.root)
        self.amount_entry.grid(row=1, column=1, padx=10, pady=10)
        
        # Description input
        self.description_label = ttk.Label(self.root, text="Description:")
        self.description_label.grid(row=2, column=0, padx=10, pady=10)
        self.description_entry = ttk.Entry(self.root)
        self.description_entry.grid(row=2, column=1, padx=10, pady=10)
        
        # Buttons
        self.add_button = ttk.Button(self.root, text="Add Expense", command=self.add_expense)
        self.add_button.grid(row=3, column=0, padx=10, pady=10)
        
        self.display_button = ttk.Button(self.root, text="Display Expenses", command=self.display_expenses)
        self.display_button.grid(row=3, column=1, padx=10, pady=10)
        
        self.visualize_button = ttk.Button(self.root, text="Visualize Expenses", command=self.visualize_expenses)
        self.visualize_button.grid(row=3, column=2, padx=10, pady=10)
        
        self.save_button = ttk.Button(self.root, text="Save to CSV", command=self.save_to_csv)
        self.save_button.grid(row=4, column=1, padx=10, pady=10)
    
    def display_expenses(self):
        top = tk.Toplevel(self.root)
        top.title("Recorded Expenses")
        
        tree = ttk.Treeview(top, columns=("Date", "Amount", "Description"), show="headings")
        tree.heading("Date", text="Date")
        tree.heading("Amount", text="Amount")
        tree.heading("Description", text="Description")
        
        for _, row in self.df.iterrows():
            tree.insert("", tk.END, values=(row["Date"], row["Amount"], row["Description"]))
        
        tree.pack(fill=tk.BOTH, expand=True)
        
    def visualize_expenses(self):
        if self.df.empty:
            messagebox.showinfo("No Data", "No expenses to visualize.")
            return
        
        top = tk.Toplevel(self.root)
        top.title("Visualize Expenses")
        top.geometry("900x700")  # Set an appropriate size for the window
        
        fig, ax = plt.subplots(figsize=(8, 6))  # Set a size for the figure
        monthly_totals = self.df.groupby(self.df["Date"].dt.to_period("M")).sum(numeric_only=True)
        monthly_totals.plot(kind="bar", y="Amount", legend=False, ax=ax)
        ax.set_title("Monthly Expenses")
        ax.set_xlabel("Month")
        ax.set_ylabel("Total Amount")

        canvas = FigureCanvasTkAgg(fig, master=top)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        toolbar = NavigationToolbar2Tk(canvas, top)
        toolbar.update()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
    
    def save_to_csv(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".csv",
                                                 filetypes=[("CSV files", "*.csv"), ("All files", "*.*")])
        if file_path:
            self.df.to_csv(file_path, index=False)
            messagebox.showinfo("Success", "Expenses saved successfully!")

    def on_closing(self):
        self.save_data()
        self.root.destroy()
