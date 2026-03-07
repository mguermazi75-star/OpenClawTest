"""
Daily Entry view - Clean, professional design
"""

import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from ttkbootstrap.widgets import DateEntry
from controllers import DailyController, ExpenseController
from models import DailyEntry, Expense

_refresh_callback = None

def set_refresh_callback(callback):
    global _refresh_callback
    _refresh_callback = callback


def create_daily_entry_view(parent, on_save_callback=None):
    global _refresh_callback
    _refresh_callback = on_save_callback
    
    frame = ttk.Frame(parent)
    frame.pack(fill=BOTH, expand=True)
    
    # Header
    header = ttk.Frame(frame)
    header.pack(fill=X, padx=25, pady=(20, 10))
    
    ttk.Label(
        header,
        text="Daily Entry",
        font=("Segoe UI", 18, "bold"),
        foreground="#1E293B"
    ).pack(side=LEFT)
    
    # Main container - two columns
    main = ttk.Frame(frame)
    main.pack(fill=BOTH, expand=True, padx=20, pady=(0, 20))
    
    # Left - Forms
    left = ttk.Frame(main)
    left.pack(side=LEFT, fill=BOTH, expand=True, padx=(0, 15))
    
    # Production card
    prod_card = ttk.LabelFrame(left, text=" Production Data ", padding=15)
    prod_card.pack(fill=X, pady=(0, 10))
    
    # Date
    ttk.Label(prod_card, text="Date", font=("Segoe UI", 9)).grid(row=0, column=0, sticky=W, pady=(0, 5))
    date_entry = DateEntry(prod_card)
    date_entry.grid(row=0, column=1, sticky=W, padx=(0, 10), pady=(0, 5))
    
    # Mortality
    ttk.Label(prod_card, text="Mortality", font=("Segoe UI", 9)).grid(row=1, column=0, sticky=W, pady=5)
    mortality_entry = ttk.Entry(prod_card, width=20)
    mortality_entry.grid(row=1, column=1, sticky=W, pady=5)
    
    # Production
    ttk.Label(prod_card, text="Eggs Produced", font=("Segoe UI", 9)).grid(row=2, column=0, sticky=W, pady=5)
    production_entry = ttk.Entry(prod_card, width=20)
    production_entry.grid(row=2, column=1, sticky=W, pady=5)
    
    # Sold
    ttk.Label(prod_card, text="Eggs Sold", font=("Segoe UI", 9)).grid(row=3, column=0, sticky=W, pady=5)
    eggs_sold_entry = ttk.Entry(prod_card, width=20)
    eggs_sold_entry.grid(row=3, column=1, sticky=W, pady=5)
    
    # Price
    ttk.Label(prod_card, text="Price (EUR)", font=("Segoe UI", 9)).grid(row=4, column=0, sticky=W, pady=5)
    egg_price_entry = ttk.Entry(prod_card, width=20)
    egg_price_entry.grid(row=4, column=1, sticky=W, pady=5)
    
    # Notes
    ttk.Label(prod_card, text="Notes", font=("Segoe UI", 9)).grid(row=5, column=0, sticky=W, pady=5)
    notes_entry = ttk.Entry(prod_card, width=20)
    notes_entry.grid(row=5, column=1, sticky=W, pady=5)
    
    # Expenses card
    exp_card = ttk.LabelFrame(left, text=" Expenses ", padding=15)
    exp_card.pack(fill=X, pady=10)
    
    ttk.Label(exp_card, text="Category", font=("Segoe UI", 9)).grid(row=0, column=0, sticky=W, pady=(0, 5))
    category_combo = ttk.Combobox(exp_card, values=[
        "Aliments (Feed)", "STEG (Electricity)", "Alvéoles (Cartons)",
        "Ouvriers (Workers)", "Divers (Misc)", "Gasoil Mercedes",
        "Entretien Mercedes", "Gasoil C15", "Entretien C15",
        "Eau (Water)", "Fiente (Manure)", "ADNENE"
    ], width=18)
    category_combo.grid(row=0, column=1, sticky=W, pady=(0, 5))
    category_combo.current(0)
    
    ttk.Label(exp_card, text="Amount (EUR)", font=("Segoe UI", 9)).grid(row=1, column=0, sticky=W, pady=5)
    expense_amount_entry = ttk.Entry(exp_card, width=20)
    expense_amount_entry.grid(row=1, column=1, sticky=W, pady=5)
    
    ttk.Label(exp_card, text="Description", font=("Segoe UI", 9)).grid(row=2, column=0, sticky=W, pady=5)
    expense_desc_entry = ttk.Entry(exp_card, width=20)
    expense_desc_entry.grid(row=2, column=1, sticky=W, pady=5)
    
    # Message & Button
    msg_label = ttk.Label(left, text="", font=("Segoe UI", 9))
    msg_label.pack(pady=5)
    
    # Right - History
    right = ttk.LabelFrame(main, text=" Entry History ", padding=10)
    right.pack(side=RIGHT, fill=BOTH, expand=True)
    
    # Buttons
    btn_frame = ttk.Frame(right)
    btn_frame.pack(fill=X, pady=(0, 8))
    ttk.Button(btn_frame, text="Delete", bootstyle="danger", command=delete_entry).pack(side=RIGHT)
    ttk.Button(btn_frame, text="Refresh", bootstyle="secondary", command=refresh_history).pack(side=RIGHT, padx=(0, 5))
    
    # Treeview
    style = ttk.Style()
    style.configure("Treeview", font=("Segoe UI", 8), rowheight=25)
    style.configure("Treeview.Heading", font=("Segoe UI", 8, "bold"))
    
    tree = ttk.Treeview(
        right,
        columns=("Date", "Mort.", "Prod.", "Sold", "Rem.", "Price", "Expense"),
        show="headings",
        height=12
    )
    
    cols = [
        ("Date", 70), ("Mort.", 40), ("Prod.", 45), ("Sold", 40), 
        ("Rem.", 40), ("Price", 55), ("Expense", 60)
    ]
    for col, w in cols:
        tree.heading(col, text=col)
        tree.column(col, width=w, anchor="center")
    
    tree.pack(fill=BOTH, expand=True)
    
    scrollbar = ttk.Scrollbar(right, orient=VERTICAL, command=tree.yview)
    tree.configure(yscrollcommand=scrollbar.set)
    scrollbar.pack(side=RIGHT, fill=Y)
    
    # Define functions first
    def save_all():
        date = date_entry.entry.get()
        if not date:
            msg_label.config(text="Please select a date!", foreground="#DC2626")
            return
        
        mortality = int(mortality_entry.get()) if mortality_entry.get() else 0
        production = int(production_entry.get()) if production_entry.get() else 0
        eggs_sold = int(eggs_sold_entry.get()) if eggs_sold_entry.get() else 0
        egg_price = float(egg_price_entry.get()) if egg_price_entry.get() else 0.0
        notes = notes_entry.get()
        
        # Save production if data exists
        if production > 0 or mortality > 0:
            existing = DailyController.get_entry_by_date(date)
            if existing:
                existing.mortality += mortality
                existing.production += production
                existing.eggs_sold += eggs_sold
                if egg_price > 0:
                    existing.egg_price = egg_price
                DailyController.update_entry(existing)
            else:
                entry = DailyEntry(
                    date=date, mortality=mortality, production=production,
                    eggs_sold=eggs_sold, egg_price=egg_price, notes=notes
                )
                DailyController.save_entry(entry)
        
        # Save expense if amount entered
        expense_amount = expense_amount_entry.get()
        if expense_amount:
            expense = Expense(
                date=date, category=category_combo.get(),
                amount=float(expense_amount), description=expense_desc_entry.get()
            )
            ExpenseController.save_expense(expense)
        
        msg_label.config(text="Entry saved!", foreground="#16A34A")
        
        # Clear
        mortality_entry.delete(0, END)
        production_entry.delete(0, END)
        eggs_sold_entry.delete(0, END)
        egg_price_entry.delete(0, END)
        notes_entry.delete(0, END)
        expense_amount_entry.delete(0, END)
        expense_desc_entry.delete(0, END)
        
        refresh_history()
        if _refresh_callback:
            _refresh_callback()
    
    def delete_entry():
        selected = tree.selection()
        if not selected:
            msg_label.config(text="Select an entry first", foreground="#D97706")
            return
        
        item = tree.item(selected[0])
        date = item['values'][0]
        DailyController.delete_entry_by_date(date)
        
        msg_label.config(text="Entry deleted!", foreground="#16A34A")
        refresh_history()
        if _refresh_callback:
            _refresh_callback()
    
    def refresh_history():
        for item in tree.get_children():
            tree.delete(item)
        
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
                entry.date, entry.mortality, entry.production,
                entry.eggs_sold, remaining,
                f"€{entry.egg_price:.2f}" if entry.egg_price > 0 else "-",
                f"€{exp_amount:.0f}" if exp_amount > 0 else "-"
            ))
    
    # Now add the button after functions are defined
    ttk.Button(
        left,
        text="Save Entry",
        bootstyle="primary",
        style="primary.TButton",
        command=save_all
    ).pack(pady=5)
    
    refresh_history()
    frame.refresh_history = refresh_history
    
    return frame
