import tkinter as tk
from expense_tracker_gui import ExpenseTracker

if __name__ == "__main__":
    root = tk.Tk()
    app = ExpenseTracker(root)
    root.protocol("WM_DELETE_WINDOW", app.on_closing)
    root.mainloop()
