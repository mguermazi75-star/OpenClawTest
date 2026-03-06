"""
Dashboard view - Main dashboard with KPIs and Charts
"""

import ttkbootstrap as ttk
from ttkbootstrap.constants import *
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from controllers import DailyController, ExpenseController


def create_dashboard_view(parent):
    """Create and return dashboard frame"""
    frame = ttk.Frame(parent)
    frame.pack(fill=BOTH, expand=True)
    
    # Stats cards row
    stats_frame = ttk.Frame(frame)
    stats_frame.pack(fill=X, padx=20, pady=20)
    
    # Configure grid columns
    for i in range(5):
        stats_frame.grid_columnconfigure(i, weight=1)
    
    # Get data
    latest_entry = DailyController.get_latest_entry()
    monthly_expenses = ExpenseController.get_monthly_expenses()
    
    current_stock = latest_entry.stock if latest_entry else 0
    today_mortality = latest_entry.mortality if latest_entry else 0
    today_production = latest_entry.production if latest_entry else 0
    today_egg_price = latest_entry.egg_price if latest_entry else 0.0
    
    # Create stat cards
    create_stat_card(stats_frame, "🐔 Current Stock", str(current_stock), "primary", 0)
    create_stat_card(stats_frame, "☠️ Today's Mortality", str(today_mortality), "danger", 1)
    create_stat_card(stats_frame, "🥚 Today's Production", str(today_production), "success", 2)
    create_stat_card(stats_frame, "💶 Egg Price", f"€{today_egg_price:.2f}", "info", 3)
    create_stat_card(stats_frame, "💸 Monthly Expenses", f"€{monthly_expenses:.2f}", "warning", 4)
    
    # Charts section
    charts_label = ttk.Label(frame, text="📊 Production & Mortality Overview", font=("Helvetica", 14, "bold"))
    charts_label.pack(anchor=W, padx=20, pady=(20, 5))
    
    create_charts_frame(frame)
    
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


def create_charts_frame(parent):
    """Create charts frame with production, mortality, and egg price charts"""
    charts_frame = ttk.Frame(parent)
    charts_frame.pack(fill=BOTH, expand=True, padx=20, pady=10)
    
    # Get data for charts
    entries = DailyController.get_entries_for_week(30)  # Last 30 entries
    entries.reverse()  # Oldest first
    
    if not entries:
        ttk.Label(charts_frame, text="No data available for charts", font=("Helvetica", 12)).pack()
        return charts_frame
    
    dates = [entry.date for entry in entries]
    production = [entry.production for entry in entries]
    mortality = [entry.mortality for entry in entries]
    egg_prices = [entry.egg_price for entry in entries]
    
    # Create figure with 3 subplots
    fig = Figure(figsize=(14, 5), dpi=100)
    
    # Production line chart
    ax1 = fig.add_subplot(1, 3, 1)
    ax1.plot(dates, production, marker='o', linewidth=2, color='#28a745', label='Production')
    ax1.set_title('🥚 Egg Production', fontsize=12, fontweight='bold')
    ax1.set_xlabel('Date')
    ax1.set_ylabel('Eggs')
    ax1.tick_params(axis='x', rotation=45)
    ax1.grid(True, alpha=0.3)
    ax1.legend()
    
    # Mortality bar chart
    ax2 = fig.add_subplot(1, 3, 2)
    ax2.bar(dates, mortality, color='#dc3545', alpha=0.7, label='Mortality')
    ax2.set_title('☠️ Mortality', fontsize=12, fontweight='bold')
    ax2.set_xlabel('Date')
    ax2.set_ylabel('Count')
    ax2.tick_params(axis='x', rotation=45)
    ax2.grid(True, alpha=0.3, axis='y')
    ax2.legend()
    
    # Egg Price line chart
    ax3 = fig.add_subplot(1, 3, 3)
    ax3.plot(dates, egg_prices, marker='s', linewidth=2, color='#17a2b8', label='Egg Price (€)')
    ax3.set_title('💶 Egg Unit Price', fontsize=12, fontweight='bold')
    ax3.set_xlabel('Date')
    ax3.set_ylabel('Price (€)')
    ax3.tick_params(axis='x', rotation=45)
    ax3.grid(True, alpha=0.3)
    ax3.legend()
    
    fig.tight_layout()
    
    # Embed in Tkinter
    canvas = FigureCanvasTkAgg(fig, master=charts_frame)
    canvas.draw()
    canvas.get_tk_widget().pack(fill=BOTH, expand=True)
    
    return charts_frame
