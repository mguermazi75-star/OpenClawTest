"""
Dashboard view - Main dashboard with KPIs
"""

import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from controllers import DailyController, ExpenseController


def create_dashboard_view(parent):
    """Create and return dashboard frame"""
    frame = ttk.Frame(parent)
    
    # Stats cards row
    stats_frame = ttk.Frame(frame)
    stats_frame.pack(fill=X, padx=20, pady=20)
    
    # Get data
    latest_entry = DailyController.get_latest_entry()
    monthly_expenses = ExpenseController.get_monthly_expenses()
    
    current_stock = latest_entry.stock if latest_entry else 0
    today_mortality = latest_entry.mortality if latest_entry else 0
    today_production = latest_entry.production if latest_entry else 0
    
    # Create stat cards
    create_stat_card(stats_frame, "🐔 Current Stock", str(current_stock), "primary", 0)
    create_stat_card(stats_frame, "☠️ Today's Mortality", str(today_mortality), "danger", 1)
    create_stat_card(stats_frame, "🥚 Today's Production", str(today_production), "success", 2)
    create_stat_card(stats_frame, "💸 Monthly Expenses", f"€{monthly_expenses:.2f}", "warning", 3)
    
    # Recent activity
    activity_frame = ttk.LabelFrame(frame, text="📋 Recent Activity", bootstyle="info")
    activity_frame.pack(fill=BOTH, expand=True, padx=20, pady=10)
    
    # Treeview
    tree = ttk.Treeview(
        activity_frame,
        columns=("Date", "Stock", "Mortality", "Production"),
        show="headings"
    )
    tree.heading("Date", text="Date")
    tree.heading("Stock", text="Stock")
    tree.heading("Mortality", text="Mortality")
    tree.heading("Production", text="Production")
    
    tree.column("Date", width=120)
    tree.column("Stock", width=100)
    tree.column("Mortality", width=100)
    tree.column("Production", width=100)
    
    tree.pack(fill=BOTH, expand=True, padx=10, pady=10)
    
    # Load data
    entries = DailyController.get_entries_for_week(10)
    for entry in entries:
        tree.insert("", 0, values=(entry.date, entry.stock, entry.mortality, entry.production))
    
    return frame


def create_stat_card(parent, title: str, value: str, style: str, column: int):
    """Create a statistics card"""
    card = ttk.Frame(parent, bootstyle=f"{style}", padding=15)
    card.grid(row=0, column=column, padx=10, sticky="ew")
    parent.grid_columnconfigure(column, weight=1)
    
    ttk.Label(card, text=title, font=("Helvetica", 10)).pack()
    ttk.Label(card, text=value, font=("Helvetica", 24, "bold")).pack(pady=5)
    
    return card
