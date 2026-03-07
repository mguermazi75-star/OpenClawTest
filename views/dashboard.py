"""
Dashboard view - Main dashboard with KPIs and Charts
Professional, clean design
"""

import ttkbootstrap as ttk
from ttkbootstrap.constants import *
import tkinter as tk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from controllers import DailyController, ExpenseController


# Professional color scheme
COLORS = {
    'primary': '#2563EB',     # Blue
    'success': '#16A34A',    # Green  
    'danger': '#DC2626',      # Red
    'warning': '#D97706',     # Amber
    'info': '#0891B2',        # Cyan
    'dark': '#1E293B',        # Dark slate
    'light': '#F1F5F9',       # Light gray
    'border': '#E2E8F0',      # Border gray
}


def create_dashboard_view(parent):
    """Create and return dashboard frame"""
    frame = ttk.Frame(parent, style='TFrame')
    frame.pack(fill=BOTH, expand=True)
    
    # Header
    header = ttk.Frame(frame)
    header.pack(fill=X, padx=25, pady=(20, 15))
    
    ttk.Label(
        header,
        text="Dashboard",
        font=("Segoe UI", 22, "bold"),
        foreground=COLORS['dark']
    ).pack(side=LEFT)
    
    ttk.Label(
        header,
        text="Farm Overview",
        font=("Segoe UI", 11),
        foreground="#64748B"
    ).pack(side=LEFT, padx=15)
    
    # Get data
    latest_entry = DailyController.get_latest_entry()
    monthly_expenses = ExpenseController.get_monthly_expenses()
    
    today_mortality = latest_entry.mortality if latest_entry else 0
    today_production = latest_entry.production if latest_entry else 0
    today_eggs_sold = latest_entry.eggs_sold if latest_entry else 0
    today_egg_price = latest_entry.egg_price if latest_entry else 0.0
    today_remaining = today_production - today_eggs_sold
    
    # Calculate remaining chickens (initial 30000 - cumulative mortality)
    total_mortality = sum(e.mortality for e in DailyController.get_entries_for_week(365))
    remaining_chickens = 30000 - total_mortality
    
    # Stats cards row
    stats_row = ttk.Frame(frame)
    stats_row.pack(fill=X, padx=20, pady=(0, 15))
    
    for i in range(7):
        stats_row.grid_columnconfigure(i, weight=1)
    
    create_card(stats_row, "Chickens", str(remaining_chickens), COLORS['primary'], 0)
    create_card(stats_row, "Mortality", str(today_mortality), COLORS['danger'], 1)
    create_card(stats_row, "Produced", str(today_production), COLORS['success'], 2)
    create_card(stats_row, "Sold", str(today_eggs_sold), COLORS['info'], 3)
    create_card(stats_row, "In Stock", str(today_remaining), COLORS['success'], 4)
    create_card(stats_row, "Price", f"€{today_egg_price:.2f}", COLORS['warning'], 5)
    create_card(stats_row, "Expenses", f"€{monthly_expenses:.0f}", COLORS['danger'], 6)
    
    # Charts section
    charts_frame = ttk.LabelFrame(frame, text=" Performance Trends", padding=15)
    charts_frame.pack(fill=BOTH, expand=True, padx=20, pady=(0, 15))
    
    create_charts(charts_frame)
    
    # Recent entries
    table_frame = ttk.LabelFrame(frame, text=" Recent Entries", padding=15)
    table_frame.pack(fill=BOTH, expand=True, padx=20, pady=(0, 20))
    
    create_table(table_frame)
    
    return frame


def create_card(parent, title: str, value: str, color: str, column: int):
    """Create a clean stat card"""
    card = ttk.Frame(parent, relief=FLAT, borderwidth=1, style='TFrame')
    card.grid(row=0, column=column, padx=6, sticky="ew")
    
    # Inner container with border
    inner = ttk.Frame(card, relief=SOLID, borderwidth=1, style='TFrame')
    inner.pack(fill=BOTH, expand=True, padx=1, pady=1)
    
    # Accent bar
    accent = tk.Frame(inner, bg=color, height=3)
    accent.pack(fill=X)
    
    # Content
    content = ttk.Frame(inner, padding=(12, 10))
    content.pack(fill=BOTH, expand=True)
    
    ttk.Label(
        content,
        text=title,
        font=("Segoe UI", 9),
        foreground="#64748B"
    ).pack(anchor=W)
    
    ttk.Label(
        content,
        text=value,
        font=("Segoe UI", 18, "bold"),
        foreground=color
    ).pack(anchor=W, pady=(4, 0))
    
    return card


def create_charts(parent):
    """Create charts"""
    entries = DailyController.get_entries_for_week(30)
    entries.reverse()
    
    if not entries:
        ttk.Label(
            parent,
            text="No data yet. Add entries to see charts.",
            font=("Segoe UI", 11),
            foreground="#94A3B8"
        ).pack(pady=40)
        return
    
    dates = [entry.date[5:] for entry in entries]  # Show only MM-DD
    production = [entry.production for entry in entries]
    mortality = [entry.mortality for entry in entries]
    
    fig = Figure(figsize=(12, 3), dpi=100)
    fig.patch.set_facecolor('white')
    
    # Production
    ax1 = fig.add_subplot(1, 2, 1)
    ax1.fill_between(range(len(dates)), production, alpha=0.3, color=COLORS['success'])
    ax1.plot(range(len(dates)), production, marker='o', linewidth=2, 
             color=COLORS['success'], markersize=3)
    ax1.set_title('Egg Production', fontsize=11, fontweight='bold', pad=8)
    ax1.set_ylabel('Eggs', fontsize=9)
    ax1.set_xticks(range(0, len(dates), max(1, len(dates)//5)))
    ax1.set_xticklabels([dates[i] for i in range(0, len(dates), max(1, len(dates)//5))], 
                        rotation=45, fontsize=7)
    ax1.spines['top'].set_visible(False)
    ax1.spines['right'].set_visible(False)
    ax1.grid(True, alpha=0.15)
    
    # Mortality
    ax2 = fig.add_subplot(1, 2, 2)
    ax2.bar(range(len(dates)), mortality, color=COLORS['danger'], alpha=0.7, width=0.5)
    ax2.set_title('Mortality', fontsize=11, fontweight='bold', pad=8)
    ax2.set_ylabel('Count', fontsize=9)
    ax2.set_xticks(range(0, len(dates), max(1, len(dates)//5)))
    ax2.set_xticklabels([dates[i] for i in range(0, len(dates), max(1, len(dates)//5))], 
                        rotation=45, fontsize=7)
    ax2.spines['top'].set_visible(False)
    ax2.spines['right'].set_visible(False)
    ax2.grid(True, alpha=0.15, axis='y')
    
    fig.tight_layout(pad=1.5)
    
    canvas = FigureCanvasTkAgg(fig, master=parent)
    canvas.draw()
    canvas.get_tk_widget().pack(fill=BOTH, expand=True)


def create_table(parent):
    """Create data table"""
    # Style
    style = ttk.Style()
    style.configure("Treeview", font=("Segoe UI", 9), rowheight=28)
    style.configure("Treeview.Heading", font=("Segoe UI", 9, "bold"))
    
    tree = ttk.Treeview(
        parent,
        columns=("Date", "Chickens", "Mortality", "Produced", "Sold", "In Stock", "Price"),
        show="headings",
        style="Treeview"
    )
    
    cols = [
        ("Date", 90, "center"),
        ("Chickens", 75, "center"),
        ("Mortality", 70, "center"),
        ("Produced", 70, "center"),
        ("Sold", 60, "center"),
        ("In Stock", 70, "center"),
        ("Price", 70, "center")
    ]
    
    for col, w, a in cols:
        tree.heading(col, text=col)
        tree.column(col, width=w, anchor=a, minwidth=50)
    
    tree.pack(fill=BOTH, expand=True)
    
    # Load data
    entries = DailyController.get_entries_for_week(10)
    cumulative = 30000
    for i, entry in enumerate(entries):
        cumulative -= entry.mortality
        eggs_in_stock = entry.production - entry.eggs_sold
        tree.insert("", END, values=(
            entry.date,
            cumulative,
            entry.mortality,
            entry.production,
            entry.eggs_sold,
            eggs_in_stock,
            f"€{entry.egg_price:.2f}" if entry.egg_price > 0 else "-"
        ), tags=('even',) if i % 2 else ('odd',))
    
    # Alternating row colors
    style.map("Treeview", background=[('selected', COLORS['primary'])])
