"""
Dashboard view - Main dashboard with KPIs and Charts
Improved design with modern cards and charts
"""

import ttkbootstrap as ttk
from ttkbootstrap.constants import *
import tkinter as tk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from controllers import DailyController, ExpenseController


# Color scheme
COLORS = {
    'stock': '#4F46E5',      # Indigo
    'mortality': '#DC2626',  # Red
    'production': '#16A34A', # Green
    'egg_price': '#0891B2',  # Cyan
    'expenses': '#D97706',  # Amber
    'bg': '#F8FAFC',         # Light gray background
    'card_bg': '#FFFFFF',    # White card background
    'text': '#1E293B',       # Dark text
    'text_light': '#64748B'  # Light text
}


def create_dashboard_view(parent):
    """Create and return dashboard frame"""
    frame = ttk.Frame(parent, style='Custom.TFrame')
    frame.pack(fill=BOTH, expand=True)
    
    # Configure styles
    style = ttk.Style()
    style.configure('Custom.TFrame', background=COLORS['bg'])
    
    # Header
    header_frame = ttk.Frame(frame, style='Custom.TFrame', padding=20)
    header_frame.pack(fill=X)
    
    ttk.Label(
        header_frame,
        text="Poultry Farm Dashboard",
        font=("Helvetica", 24, "bold"),
        foreground=COLORS['text'],
        style='Custom.TLabel'
    ).pack(side=LEFT)
    
    ttk.Label(
        header_frame,
        text="Real-time Overview",
        font=("Helvetica", 12),
        foreground=COLORS['text_light'],
        style='Custom.TLabel'
    ).pack(side=LEFT, padx=20)
    
    # Get data
    latest_entry = DailyController.get_latest_entry()
    monthly_expenses = ExpenseController.get_monthly_expenses()
    
    current_stock = latest_entry.stock if latest_entry else 0
    today_mortality = latest_entry.mortality if latest_entry else 0
    today_production = latest_entry.production if latest_entry else 0
    today_egg_price = latest_entry.egg_price if latest_entry else 0.0
    
    # Stats cards - Row 1
    stats_row1 = ttk.Frame(frame, style='Custom.TFrame', padding=(20, 0, 20, 10))
    stats_row1.pack(fill=X)
    
    create_modern_card(
        stats_row1, "Current Stock", str(current_stock), 
        COLORS['stock'], "Chickens", 0
    )
    create_modern_card(
        stats_row1, "Today's Mortality", str(today_mortality), 
        COLORS['mortality'], "Deaths", 1
    )
    create_modern_card(
        stats_row1, "Today's Production", str(today_production), 
        COLORS['production'], "Eggs", 2
    )
    
    # Stats cards - Row 2
    stats_row2 = ttk.Frame(frame, style='Custom.TFrame', padding=(20, 0, 20, 20))
    stats_row2.pack(fill=X)
    
    create_modern_card(
        stats_row2, "Egg Unit Price", f"€{today_egg_price:.2f}", 
        COLORS['egg_price'], "Per egg", 0
    )
    create_modern_card(
        stats_row2, "Monthly Expenses", f"€{monthly_expenses:.2f}", 
        COLORS['expenses'], "This month", 1
    )
    # Empty space for alignment
    ttk.Frame(stats_row2, width=200).grid(row=0, column=2, padx=10)
    
    # Charts section
    charts_container = ttk.LabelFrame(
        frame, 
        text=" Performance Trends (Last 30 Days)",
        padding=15,
        style='Custom.TLabelframe'
    )
    charts_container.pack(fill=BOTH, expand=True, padx=20, pady=(0, 20))
    
    create_charts_frame(charts_container)
    
    # Recent activity table
    activity_container = ttk.LabelFrame(
        frame,
        text=" Recent Entries",
        padding=15,
        style='Custom.TLabelframe'
    )
    activity_container.pack(fill=BOTH, expand=True, padx=20, pady=(0, 20))
    
    create_activity_table(activity_container)
    
    return frame


def create_modern_card(parent, title: str, value: str, color: str, subtitle: str, column: int):
    """Create a modern styled stat card"""
    # Card container with border/shadow effect
    card = ttk.Frame(parent, style='Card.TFrame', borderwidth=1, relief=SOLID)
    card.grid(row=0, column=column, padx=10, sticky="ew")
    parent.grid_columnconfigure(column, weight=1)
    
    # Color accent bar at top (using tkinter Frame for background color)
    accent = tk.Frame(card, height=4, bg=color)
    accent.pack(fill=X)
    
    # Content
    content = ttk.Frame(card, padding=15)
    content.pack(fill=BOTH, expand=True)
    
    # Title
    ttk.Label(
        content,
        text=title,
        font=("Helvetica", 11),
        foreground=COLORS['text_light']
    ).pack(anchor=W)
    
    # Value
    ttk.Label(
        content,
        text=value,
        font=("Helvetica", 28, "bold"),
        foreground=color
    ).pack(anchor=W, pady=5)
    
    # Subtitle
    ttk.Label(
        content,
        text=subtitle,
        font=("Helvetica", 9),
        foreground=COLORS['text_light']
    ).pack(anchor=W)
    
    return card


def create_charts_frame(parent):
    """Create charts frame with production, mortality, and egg price charts"""
    # Get data for charts
    entries = DailyController.get_entries_for_week(30)
    entries.reverse()
    
    if not entries:
        ttk.Label(
            parent,
            text="No data available yet. Add entries to see charts.",
            font=("Helvetica", 12),
            foreground=COLORS['text_light']
        ).pack(pady=50)
        return
    
    dates = [entry.date for entry in entries]
    production = [entry.production for entry in entries]
    mortality = [entry.mortality for entry in entries]
    egg_prices = [entry.egg_price for entry in entries]
    
    # Create figure with custom styling
    fig = Figure(figsize=(14, 4.5), dpi=100)
    fig.patch.set_facecolor('#FFFFFF')
    
    # Production chart (line with fill)
    ax1 = fig.add_subplot(1, 3, 1)
    ax1.fill_between(range(len(dates)), production, alpha=0.3, color=COLORS['production'])
    ax1.plot(range(len(dates)), production, marker='o', linewidth=2.5, 
             color=COLORS['production'], markersize=4, label='Production')
    ax1.set_title('Egg Production', fontsize=13, fontweight='bold', pad=10)
    ax1.set_ylabel('Eggs', fontsize=10)
    ax1.set_xticks(range(0, len(dates), max(1, len(dates)//5)))
    ax1.set_xticklabels([dates[i] for i in range(0, len(dates), max(1, len(dates)//5))], 
                        rotation=45, fontsize=8)
    ax1.grid(True, alpha=0.2, linestyle='--')
    ax1.spines['top'].set_visible(False)
    ax1.spines['right'].set_visible(False)
    ax1.set_facecolor('#FFFFFF')
    
    # Mortality chart (bar)
    ax2 = fig.add_subplot(1, 3, 2)
    ax2.bar(range(len(dates)), mortality, color=COLORS['mortality'], alpha=0.7, width=0.6)
    ax2.set_title('Mortality', fontsize=13, fontweight='bold', pad=10)
    ax2.set_ylabel('Count', fontsize=10)
    ax2.set_xticks(range(0, len(dates), max(1, len(dates)//5)))
    ax2.set_xticklabels([dates[i] for i in range(0, len(dates), max(1, len(dates)//5))], 
                        rotation=45, fontsize=8)
    ax2.grid(True, alpha=0.2, linestyle='--', axis='y')
    ax2.spines['top'].set_visible(False)
    ax2.spines['right'].set_visible(False)
    ax2.set_facecolor('#FFFFFF')
    
    # Egg Price chart (line)
    ax3 = fig.add_subplot(1, 3, 3)
    ax3.plot(range(len(dates)), egg_prices, marker='s', linewidth=2.5, 
             color=COLORS['egg_price'], markersize=4, label='Price')
    ax3.fill_between(range(len(dates)), egg_prices, alpha=0.2, color=COLORS['egg_price'])
    ax3.set_title('Egg Unit Price', fontsize=13, fontweight='bold', pad=10)
    ax3.set_ylabel('EUR', fontsize=10)
    ax3.set_xticks(range(0, len(dates), max(1, len(dates)//5)))
    ax3.set_xticklabels([dates[i] for i in range(0, len(dates), max(1, len(dates)//5))], 
                        rotation=45, fontsize=8)
    ax3.grid(True, alpha=0.2, linestyle='--')
    ax3.spines['top'].set_visible(False)
    ax3.spines['right'].set_visible(False)
    ax3.set_facecolor('#FFFFFF')
    
    fig.tight_layout(pad=2.0)
    
    # Embed in Tkinter
    canvas = FigureCanvasTkAgg(fig, master=parent)
    canvas.draw()
    canvas.get_tk_widget().pack(fill=BOTH, expand=True)
    
    return parent


def create_activity_table(parent):
    """Create styled activity table"""
    # Style the treeview
    style = ttk.Style()
    style.configure(
        "Treeview",
        font=("Helvetica", 10),
        rowheight=30
    )
    style.configure(
        "Treeview.Heading",
        font=("Helvetica", 11, "bold")
    )
    
    # Treeview
    tree = ttk.Treeview(
        parent,
        columns=("Date", "Stock", "Mortality", "Production", "Egg Price"),
        show="headings",
        style="Custom.Treeview"
    )
    
    # Configure columns
    columns = [
        ("Date", 120, "w"),
        ("Stock", 100, "e"),
        ("Mortality", 100, "e"),
        ("Production", 100, "e"),
        ("Egg Price", 100, "e")
    ]
    
    for col, width, anchor in columns:
        tree.heading(col, text=col)
        tree.column(col, width=width, anchor=anchor, minwidth=80)
    
    tree.pack(fill=BOTH, expand=True)
    
    # Load data
    entries = DailyController.get_entries_for_week(10)
    for i, entry in enumerate(entries):
        tags = ('odd',) if i % 2 else ('even',)
        tree.insert("", END, values=(
            entry.date,
            entry.stock,
            entry.mortality,
            entry.production,
            f"€{entry.egg_price:.2f}"
        ), tags=tags)
    
    # Configure row tags for striping
    style.configure("Treeview", background="#FFFFFF")
    style.configure("Treeview", fieldbackground="#FFFFFF")
    style.map("Treeview", background=[('selected', COLORS['stock'])])
    
    return parent
