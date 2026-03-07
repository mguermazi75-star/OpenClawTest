#!/usr/bin/env python3
"""
Poultry Farm Management System - Main Application
A modern GUI application replacing Excel for farm management
"""

import ttkbootstrap as ttk
from ttkbootstrap.constants import *

# Import utils
from utils import APP_TITLE, APP_THEME, APP_SIZE, APP_MIN_SIZE

# Import models
from models import init_db

# Import views
from views import (
    create_dashboard_view,
    create_daily_entry_view,
    create_expenses_view,
    create_billing_view,
    create_reports_view
)
from views.daily_entry import set_refresh_callback


class PoultryFarmApp(ttk.Window):
    def __init__(self):
        super().__init__(themename=APP_THEME)
        
        self.title(APP_TITLE)
        self.geometry(APP_SIZE)
        self.minsize(*APP_MIN_SIZE)
        
        # Initialize database
        init_db()
        
        # Setup UI
        self.create_menu()
        self.create_widgets()
        
        # Center window
        self.center_window()
    
    def center_window(self):
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f'{width}x{height}+{x}+{y}')
    
    def create_menu(self):
        """Create top menu bar"""
        menubar = ttk.Menu(self)
        self.config(menu=menubar)
        
        # File menu
        file_menu = ttk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="📁 File", menu=file_menu)
        file_menu.add_command(label="💾 Export Data")
        file_menu.add_command(label="📥 Import Data")
        file_menu.add_separator()
        file_menu.add_command(label="❌ Exit", command=self.quit)
        
        # Help menu
        help_menu = ttk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="❓ Help", menu=help_menu)
        help_menu.add_command(label="📖 About")
    
    def create_widgets(self):
        """Create main UI widgets"""
        
        # Title
        title_frame = ttk.Frame(self)
        title_frame.pack(fill=X, padx=20, pady=10)
        
        ttk.Label(
            title_frame,
            text=APP_TITLE,
            font=("Helvetica", 24, "bold"),
            bootstyle="primary"
        ).pack(side=LEFT)
        
        # Notebook (Tabs)
        self.nb = ttk.Notebook(self)
        self.nb.pack(fill=BOTH, expand=True, padx=10, pady=10)
        
        # Create tabs
        self.dashboard_tab = ttk.Frame(notebook)
        self.daily_tab = ttk.Frame(notebook)
        self.expenses_tab = ttk.Frame(notebook)
        self.billing_tab = ttk.Frame(notebook)
        self.reports_tab = ttk.Frame(notebook)
        
        self.nb.add(self.dashboard_tab, text="📊 Dashboard")
        self.nb.add(self.daily_tab, text="📝 Daily Entry")
        self.nb.add(self.expenses_tab, text="💰 Expenses")
        self.nb.add(self.billing_tab, text="🧾 Billing")
        self.nb.add(self.reports_tab, text="📈 Reports")
        
        # Build each tab
        create_dashboard_view(self.dashboard_tab)
        create_daily_entry_view(self.daily_tab, self.refresh_dashboard)
        create_expenses_view(self.expenses_tab)
        create_billing_view(self.billing_tab)
        create_reports_view(self.reports_tab)
    
    def refresh_dashboard(self):
        """Refresh the dashboard tab"""
        # Clear existing dashboard
        for widget in self.dashboard_tab.winfo_children():
            widget.destroy()
        # Rebuild dashboard
        create_dashboard_view(self.dashboard_tab)
        # Switch to dashboard tab
        self.nb.select(0)


def main():
    try:
        app = PoultryFarmApp()
        app.mainloop()
    except Exception as e:
        print(f"Error starting app: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
