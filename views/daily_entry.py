"""
Daily Entry view - Form for daily production/mortality and expenses
"""

import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from ttkbootstrap.widgets import DateEntry
from controllers import DailyController, ExpenseController
from models import DailyEntry, Expense

# Global callback for dashboard refresh
_refresh_callback = None

def set_refresh_callback(callback):
    """Set callback to refresh dashboard after saving"""
    global _refresh_callback
    _refresh_callback = callback


def create_daily_entry_view(parent, on_save_callback=None):
    """Create and return daily entry form frame"""
    global _refresh_callback
    _refresh_callback = on_save_callback
    frame = ttk.Frame(parent)
    frame.pack(fill=BOTH, expand=True)
    
    # Main container - two columns
    main_container = ttk.Frame(frame)
    main_container.pack(fill=BOTH, expand=True, padx=20, pady=20)
    
    # Left side - Forms
    left_frame = ttk.Frame(main_container)
    left_frame.pack(side=LEFT, fill=BOTH, expand=True, padx=(0, 10))
    
    # ===== PRODUCTION SECTION =====
    prod_frame = ttk.LabelFrame(left_frame, text="Daily Production", padding=15)
    prod_frame.pack(fill=X, pady=(0, 10))
    
    # Date
    ttk.Label(prod_frame, text="Date:").grid(row=0, column=0, sticky=W, pady=5)
    date_entry = DateEntry(prod_frame)
    date_entry.grid(row=0, column=1, padx=5, sticky=W, pady=5)
    
    # Mortality
    ttk.Label(prod_frame, text="Mortality:").grid(row=1, column=0, sticky=W, pady=5)
    mortality_entry = ttk.Entry(prod_frame, width=20)
    mortality_entry.grid(row=1, column=1, padx=5, sticky=W, pady=5)
    
    # Eggs Produced
    ttk.Label(prod_frame, text="Eggs Produced:").grid(row=2, column=0, sticky=W, pady=5)
    production_entry = ttk.Entry(prod_frame, width=20)
    production_entry.grid(row=2, column=1, padx=5, sticky=W, pady=5)
    
    # Eggs Sold
    ttk.Label(prod_frame, text="Eggs Sold:").grid(row=3, column=0, sticky=W, pady=5)
    eggs_sold_entry = ttk.Entry(prod_frame, width=20)
    eggs_sold_entry.grid(row=3, column=1, padx=5, sticky=W, pady=5)
    
    # Egg Price
    ttk.Label(prod_frame, text="Egg Price (EUR):").grid(row=4, column=0, sticky=W, pady=5)
    egg_price_entry = ttk.Entry(prod_frame, width=20)
    egg_price_entry.grid(row=4, column=1, padx=5, sticky=W, pady=5)
    
    # Notes
    ttk.Label(prod_frame, text="Notes:").grid(row=5, column=0, sticky=W, pady=5)
    notes_entry = ttk.Entry(prod_frame, width=20)
    notes_entry.grid(row=5, column=1, padx=5, sticky=W, pady=5)
    
    # ===== EXPENSES SECTION =====
    exp_frame = ttk.LabelFrame(left_frame, text="Daily Expenses", padding=15)
    exp_frame.pack(fill=X, pady=10)
    
    # Expense Category
    ttk.Label(exp_frame, text="Category:").grid(row=0, column=0, sticky=W, pady=5)
    category_combo = ttk.Combobox(exp_frame, values=[
        "Feed", "Medicine", "Utilities", "Labor", "Transport", "Maintenance", "Other"
    ], width=18)
    category_combo.grid(row=0, column=1, padx=5, sticky=W, pady=5)
    category_combo.current(0)
    
    # Expense Amount
    ttk.Label(exp_frame, text="Amount (EUR):").grid(row=1, column=0, sticky=W, pady=5)
    expense_amount_entry = ttk.Entry(exp_frame, width=20)
    expense_amount_entry.grid(row=1, column=1, padx=5, sticky=W, pady=5)
    
    # Expense Description
    ttk.Label(exp_frame, text="Description:").grid(row=2, column=0, sticky=W, pady=5)
    expense_desc_entry = ttk.Entry(exp_frame, width=20)
    expense_desc_entry.grid(row=2, column=1, padx=5, sticky=W, pady=5)
    
    # Message label
    message_label = ttk.Label(left_frame, text="", bootstyle="success")
    message_label.pack(pady=5)
    
    # Save button
    ttk.Button(
        left_frame,
        text="Save All",
        bootstyle="success",
        command=lambda: save_all()
    ).pack(pady=5)
    
    # Right side - History
    right_frame = ttk.LabelFrame(main_container, text="Entry History", padding=10)
    right_frame.pack(side=RIGHT, fill=BOTH, expand=True, padx=(10, 0))
    
    # Buttons frame
    btn_frame = ttk.Frame(right_frame)
    btn_frame.pack(fill=X, pady=(0, 5))
    
    ttk.Button(btn_frame, text="Delete", bootstyle="danger", 
               command=lambda: delete_entry()).pack(side=RIGHT)
    ttk.Button(btn_frame, text="Refresh", bootstyle="secondary",
               command=lambda: refresh_history()).pack(side=RIGHT, padx=(0, 5))
    
    # Treeview
    columns = ("Date", "Mortality", "Produced", "Sold", "Rem.", "Price", "Expense", "Notes")
    tree = ttk.Treeview(right_frame, columns=columns, show="headings", height=15)
    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, width=70)
    tree.pack(fill=BOTH, expand=True)
    
    # Scrollbar
    scrollbar = ttk.Scrollbar(right_frame, orient=VERTICAL, command=tree.yview)
    tree.configure(yscrollcommand=scrollbar.set)
    scrollbar.pack(side=RIGHT, fill=Y)
    
    def save_all():
        """Save both production entry and expense"""
        date = date_entry.entry.get()
        
        if not date:
            message_label.config(text="Please select a date!", bootstyle="danger")
            return
        
        # Save production entry
        entry = DailyEntry(
            date=date,
            mortality=int(mortality_entry.get()) if mortality_entry.get() else 0,
            production=int(production_entry.get()) if production_entry.get() else 0,
            eggs_sold=int(eggs_sold_entry.get()) if eggs_sold_entry.get() else 0,
            egg_price=float(egg_price_entry.get()) if egg_price_entry.get() else 0.0,
            notes=notes_entry.get()
        )
        DailyController.save_entry(entry)
        
        # Save expense if amount entered
        expense_amount = expense_amount_entry.get()
        if expense_amount:
            expense = Expense(
                date=date,
                category=category_combo.get(),
                amount=float(expense_amount),
                description=expense_desc_entry.get()
            )
            ExpenseController.save_expense(expense)
        
        message_label.config(text="Entry saved!", bootstyle="success")
        
        # Clear form
        mortality_entry.delete(0, END)
        production_entry.delete(0, END)
        eggs_sold_entry.delete(0, END)
        egg_price_entry.delete(0, END)
        notes_entry.delete(0, END)
        expense_amount_entry.delete(0, END)
        expense_desc_entry.delete(0, END)
        
        # Refresh history
        refresh_history()
        
        # Trigger dashboard refresh if callback is set
        if _refresh_callback:
            _refresh_callback()
    
    def delete_entry():
        """Delete selected entry"""
        selected = tree.selection()
        if not selected:
            message_label.config(text="Select an entry to delete", bootstyle="warning")
            return
        
        # Get the entry date from selected row
        item = tree.item(selected[0])
        date = item['values'][0]
        
        # Delete from database
        DailyController.delete_entry_by_date(date)
        
        message_label.config(text="Entry deleted!", bootstyle="success")
        refresh_history()
        
        # Trigger dashboard refresh if callback is set
        if _refresh_callback:
            _refresh_callback()
    
    def refresh_history():
        """Refresh the history treeview"""
        for item in tree.get_children():
            tree.delete(item)
        
        # Get daily entries
        entries = DailyController.get_all_entries(30)
        
        # Get expenses by date
        expenses = ExpenseController.get_all_expenses(30)
        expenses_by_date = {}
        for exp in expenses:
            if exp.date not in expenses_by_date:
                expenses_by_date[exp.date] = 0
            expenses_by_date[exp.date] += exp.amount
        
        for entry in entries:
            remaining = entry.production - entry.eggs_sold
            exp_amount = expenses_by_date.get(entry.date, 0)
            tree.insert("", END, values=(
                entry.date, 
                entry.mortality, 
                entry.production,
                entry.eggs_sold,
                remaining,
                f"€{entry.egg_price:.2f}",
                f"€{exp_amount:.2f}" if exp_amount > 0 else "-",
                entry.notes[:15] + "..." if len(entry.notes) > 15 else entry.notes
            ))
    
    # Initial load
    refresh_history()
    
    # Store refresh function for external calls
    frame.refresh_history = refresh_history
    
    return frame
