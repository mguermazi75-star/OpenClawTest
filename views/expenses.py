"""
Expenses view - Form for expense tracking
"""

import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from ttkbootstrap.widgets import DateEntry
from controllers import ExpenseController
from models import Expense
from utils import EXPENSE_CATEGORIES


def create_expenses_view(parent):
    """Create and return expenses form frame"""
    frame = ttk.Frame(parent)
    
    # Form frame
    form_frame = ttk.LabelFrame(frame, text="💰 Add Expense", padding=20)
    form_frame.pack(fill=X, padx=20, pady=20)
    
    # Date
    ttk.Label(form_frame, text="📅 Date:").grid(row=0, column=0, sticky=W, pady=10)
    date_entry = DateEntry(form_frame)
    date_entry.grid(row=0, column=1, padx=10, sticky=W)
    
    # Category
    ttk.Label(form_frame, text="📂 Category:").grid(row=1, column=0, sticky=W, pady=10)
    category_combo = ttk.Combobox(
        form_frame,
        values=EXPENSE_CATEGORIES,
        width=28
    )
    category_combo.grid(row=1, column=1, padx=10, sticky=W)
    
    # Amount
    ttk.Label(form_frame, text="💵 Amount (€):").grid(row=2, column=0, sticky=W, pady=10)
    amount_entry = ttk.Entry(form_frame, width=30)
    amount_entry.grid(row=2, column=1, padx=10, sticky=W)
    
    # Description
    ttk.Label(form_frame, text="📝 Description:").grid(row=3, column=0, sticky=W, pady=10)
    desc_entry = ttk.Entry(form_frame, width=30)
    desc_entry.grid(row=3, column=1, padx=10, sticky=W)
    
    # Message label
    message_label = ttk.Label(form_frame, text="", bootstyle="success")
    message_label.grid(row=5, column=0, columnspan=2, pady=10)
    
    def save_expense():
        """Save the expense"""
        date = date_entry.entry.get()
        category = category_combo.get()
        amount = amount_entry.get()
        description = desc_entry.get()
        
        if not date or not category or not amount:
            message_label.config(text="❌ Please fill all required fields!", bootstyle="danger")
            return
        
        try:
            amount = float(amount)
        except ValueError:
            message_label.config(text="❌ Amount must be a number!", bootstyle="danger")
            return
        
        expense = Expense(
            date=date,
            category=category,
            amount=amount,
            description=description
        )
        
        ExpenseController.save_expense(expense)
        
        message_label.config(text="✅ Expense saved!", bootstyle="success")
        
        amount_entry.delete(0, END)
        desc_entry.delete(0, END)
        
        refresh_history()
    
    # Save button
    ttk.Button(
        form_frame,
        text="💾 Save Expense",
        bootstyle="success",
        command=save_expense
    ).grid(row=4, column=0, columnspan=2, pady=20)
    
    # History frame
    history_frame = ttk.LabelFrame(frame, text="📜 Expense History", padding=10)
    history_frame.pack(fill=BOTH, expand=True, padx=20, pady=10)
    
    # Treeview
    columns = ("Date", "Category", "Amount", "Description")
    tree = ttk.Treeview(history_frame, columns=columns, show="headings")
    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, width=180)
    tree.pack(fill=BOTH, expand=True)
    
    def refresh_history():
        """Refresh the history treeview"""
        for item in tree.get_children():
            tree.delete(item)
        
        expenses = ExpenseController.get_all_expenses()
        for exp in expenses:
            tree.insert("", END, values=(
                exp.date,
                exp.category,
                f"€{exp.amount:.2f}",
                exp.description
            ))
    
    # Initial load
    refresh_history()
    
    frame.refresh_history = refresh_history
    
    return frame
