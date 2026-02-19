#!/usr/bin/env python3
"""
Poultry Farm Management System
A modern GUI application replacing Excel for farm management
"""

import ttkbootstrap as ttk
from ttkbootstrap.constants import *
import sqlite3
from datetime import datetime
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib import colors
import os

# Database setup
DB_NAME = "poultry_farm.db"

def init_db():
    """Initialize SQLite database with required tables"""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    # Daily entries table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS daily_entries (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT NOT NULL,
            stock INTEGER,
            mortality INTEGER,
            production INTEGER,
            notes TEXT
        )
    ''')
    
    # Expenses table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT NOT NULL,
            category TEXT NOT NULL,
            amount REAL,
            description TEXT
        )
    ''')
    
    # Clients table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS clients (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            phone TEXT,
            address TEXT
        )
    ''')
    
    # Invoices table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS invoices (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            invoice_number TEXT NOT NULL,
            client_id INTEGER,
            date TEXT NOT NULL,
            total_amount REAL,
            status TEXT DEFAULT 'unpaid',
            FOREIGN KEY (client_id) REFERENCES clients(id)
        )
    ''')
    
    # Invoice items table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS invoice_items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            invoice_id INTEGER,
            description TEXT,
            quantity INTEGER,
            unit_price REAL,
            total REAL,
            FOREIGN KEY (invoice_id) REFERENCES invoices(id)
        )
    ''')
    
    conn.commit()
    conn.close()

class PoultryFarmApp(ttk.Window):
    def __init__(self):
        super().__init__(themename="cosmo")
        
        self.title("🐔 Poultry Farm Management")
        self.geometry("1200x700")
        self.minsize(1000, 600)
        
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
            text="🐔 Poultry Farm Management System",
            font=("Helvetica", 24, "bold"),
            bootstyle="primary"
        ).pack(side=LEFT)
        
        # Notebook (Tabs)
        notebook = ttk.Notebook(self)
        notebook.pack(fill=BOTH, expand=True, padx=10, pady=10)
        
        # Create tabs
        self.dashboard_tab = ttk.Frame(notebook)
        self.daily_tab = ttk.Frame(notebook)
        self.expenses_tab = ttk.Frame(notebook)
        self.billing_tab = ttk.Frame(notebook)
        self.reports_tab = ttk.Frame(notebook)
        
        notebook.add(self.dashboard_tab, text="📊 Dashboard")
        notebook.add(self.daily_tab, text="📝 Daily Entry")
        notebook.add(self.expenses_tab, text="💰 Expenses")
        notebook.add(self.billing_tab, text="🧾 Billing")
        notebook.add(self.reports_tab, text="📈 Reports")
        
        # Build each tab
        self.build_dashboard()
        self.build_daily_entry()
        self.build_expenses()
        self.build_billing()
        self.build_reports()
    
    # ==================== DASHBOARD ====================
    def build_dashboard(self):
        """Build dashboard with KPIs"""
        # Stats cards row
        stats_frame = ttk.Frame(self.dashboard_tab)
        stats_frame.pack(fill=X, padx=20, pady=20)
        
        # Get latest data
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        
        # Current stock
        cursor.execute("SELECT stock FROM daily_entries ORDER BY date DESC LIMIT 1")
        stock_result = cursor.fetchone()
        current_stock = stock_result[0] if stock_result else 0
        
        # Today's mortality
        today = datetime.now().strftime("%Y-%m-%d")
        cursor.execute("SELECT mortality FROM daily_entries WHERE date = ?", (today,))
        mortality_result = cursor.fetchone()
        today_mortality = mortality_result[0] if mortality_result else 0
        
        # Today's production
        cursor.execute("SELECT production FROM daily_entries WHERE date = ?", (today,))
        prod_result = cursor.fetchone()
        today_production = prod_result[0] if prod_result else 0
        
        # Total expenses this month
        cursor.execute("""
            SELECT SUM(amount) FROM expenses 
            WHERE date LIKE ?
        """, (f"{datetime.now().strftime('%Y-%m')}%",))
        exp_result = cursor.fetchone()
        monthly_expenses = exp_result[0] if exp_result[0] else 0
        
        conn.close()
        
        # Create stat cards
        self.create_stat_card(stats_frame, "🐔 Current Stock", str(current_stock), "primary", 0)
        self.create_stat_card(stats_frame, "☠️ Today's Mortality", str(today_mortality), "danger", 1)
        self.create_stat_card(stats_frame, "🥚 Today's Production", str(today_production), "success", 2)
        self.create_stat_card(stats_frame, "💸 Monthly Expenses", f"€{monthly_expenses:.2f}", "warning", 3)
        
        # Recent activity
        activity_frame = ttk.LabelFrame(self.dashboard_tab, text="📋 Recent Activity", bootstyle="info")
        activity_frame.pack(fill=BOTH, expand=True, padx=20, pady=10)
        
        # Activity list
        activity_tree = ttk.Treeview(activity_frame, columns=("Date", "Stock", "Mortality", "Production"), show="headings")
        activity_tree.heading("Date", text="Date")
        activity_tree.heading("Stock", text="Stock")
        activity_tree.heading("Mortality", text="Mortality")
        activity_tree.heading("Production", text="Production")
        
        activity_tree.column("Date", width=120)
        activity_tree.column("Stock", width=100)
        activity_tree.column("Mortality", width=100)
        activity_tree.column("Production", width=100)
        
        activity_tree.pack(fill=BOTH, expand=True, padx=10, pady=10)
        
        # Load recent data
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute("SELECT date, stock, mortality, production FROM daily_entries ORDER BY date DESC LIMIT 10")
        for row in cursor.fetchall():
            activity_tree.insert("", 0, values=row)
        conn.close()
    
    def create_stat_card(self, parent, title, value, style, column):
        """Create a statistics card widget"""
        card = ttk.Frame(parent, bootstyle=f"{style}", padding=15)
        card.grid(row=0, column=column, padx=10, sticky="ew")
        parent.grid_columnconfigure(column, weight=1)
        
        ttk.Label(card, text=title, font=("Helvetica", 10)).pack()
        ttk.Label(card, text=value, font=("Helvetica", 24, "bold")).pack(pady=5)
    
    # ==================== DAILY ENTRY ====================
    def build_daily_entry(self):
        """Build daily data entry form"""
        # Form frame
        form_frame = ttk.LabelFrame(self.daily_tab, text="📝 Daily Data Entry", padding=20)
        form_frame.pack(fill=X, padx=20, pady=20)
        
        # Date
        ttk.Label(form_frame, text="📅 Date:").grid(row=0, column=0, sticky=W, pady=10)
        self.daily_date = ttk.DateEntry(form_frame)
        self.daily_date.grid(row=0, column=1, padx=10, sticky=W)
        
        # Stock
        ttk.Label(form_frame, text="🐔 Current Stock:").grid(row=1, column=0, sticky=W, pady=10)
        self.daily_stock = ttk.Entry(form_frame, width=30)
        self.daily_stock.grid(row=1, column=1, padx=10, sticky=W)
        
        # Mortality
        ttk.Label(form_frame, text="☠️ Mortality:").grid(row=2, column=0, sticky=W, pady=10)
        self.daily_mortality = ttk.Entry(form_frame, width=30)
        self.daily_mortality.grid(row=2, column=1, padx=10, sticky=W)
        
        # Production
        ttk.Label(form_frame, text="🥚 Production:").grid(row=3, column=0, sticky=W, pady=10)
        self.daily_production = ttk.Entry(form_frame, width=30)
        self.daily_production.grid(row=3, column=1, padx=10, sticky=W)
        
        # Notes
        ttk.Label(form_frame, text="📋 Notes:").grid(row=4, column=0, sticky=W, pady=10)
        self.daily_notes = ttk.Entry(form_frame, width=30)
        self.daily_notes.grid(row=4, column=1, padx=10, sticky=W)
        
        # Save button
        ttk.Button(
            form_frame,
            text="💾 Save Entry",
            bootstyle="success",
            command=self.save_daily_entry
        ).grid(row=5, column=0, columnspan=2, pady=20)
        
        # History frame
        history_frame = ttk.LabelFrame(self.daily_tab, text="📜 Entry History", padding=10)
        history_frame.pack(fill=BOTH, expand=True, padx=20, pady=10)
        
        # Treeview
        columns = ("Date", "Stock", "Mortality", "Production", "Notes")
        self.daily_tree = ttk.Treeview(history_frame, columns=columns, show="headings")
        for col in columns:
            self.daily_tree.heading(col, text=col)
            self.daily_tree.column(col, width=150)
        self.daily_tree.pack(fill=BOTH, expand=True)
        
        self.refresh_daily_history()
    
    def save_daily_entry(self):
        """Save daily entry to database"""
        date = self.daily_date.entry.get()
        stock = self.daily_stock.get()
        mortality = self.daily_mortality.get()
        production = self.daily_production.get()
        notes = self.daily_notes.get()
        
        if not date:
            ttk.messagebox.showerror("Error", "Please select a date!")
            return
        
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO daily_entries (date, stock, mortality, production, notes)
            VALUES (?, ?, ?, ?, ?)
        ''', (date, stock or 0, mortality or 0, production or 0, notes))
        
        conn.commit()
        conn.close()
        
        ttk.messagebox.showinfo("Success", "Daily entry saved!")
        
        # Clear form
        self.daily_stock.delete(0, END)
        self.daily_mortality.delete(0, END)
        self.daily_production.delete(0, END)
        self.daily_notes.delete(0, END)
        
        self.refresh_daily_history()
        self.build_dashboard()
    
    def refresh_daily_history(self):
        """Refresh daily entry history"""
        for item in self.daily_tree.get_children():
            self.daily_tree.delete(item)
        
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute("SELECT date, stock, mortality, production, notes FROM daily_entries ORDER BY date DESC")
        for row in cursor.fetchall():
            self.daily_tree.insert("", END, values=row)
        conn.close()
    
    # ==================== EXPENSES ====================
    def build_expenses(self):
        """Build expenses entry form"""
        # Form frame
        form_frame = ttk.LabelFrame(self.expenses_tab, text="💰 Add Expense", padding=20)
        form_frame.pack(fill=X, padx=20, pady=20)
        
        # Date
        ttk.Label(form_frame, text="📅 Date:").grid(row=0, column=0, sticky=W, pady=10)
        self.exp_date = ttk.DateEntry(form_frame)
        self.exp_date.grid(row=0, column=1, padx=10, sticky=W)
        
        # Category
        ttk.Label(form_frame, text="📂 Category:").grid(row=1, column=0, sticky=W, pady=10)
        self.exp_category = ttk.Combobox(
            form_frame,
            values=[
                "Aliments (Feed)",
                "STEG (Electricity)",
                "Alvéoles (Cartons)",
                "Ouvriers (Workers)",
                "Divers (Misc)",
                "Gasoil Mercedes",
                "Entretien Mercedes",
                "Gasoil C15",
                "Entretien C15",
                "Eau (Water)",
                "Fiente (Manure)",
                "ADNENE"
            ],
            width=28
        )
        self.exp_category.grid(row=1, column=1, padx=10, sticky=W)
        
        # Amount
        ttk.Label(form_frame, text="💵 Amount (€):").grid(row=2, column=0, sticky=W, pady=10)
        self.exp_amount = ttk.Entry(form_frame, width=30)
        self.exp_amount.grid(row=2, column=1, padx=10, sticky=W)
        
        # Description
        ttk.Label(form_frame, text="📝 Description:").grid(row=3, column=0, sticky=W, pady=10)
        self.exp_description = ttk.Entry(form_frame, width=30)
        self.exp_description.grid(row=3, column=1, padx=10, sticky=W)
        
        # Save button
        ttk.Button(
            form_frame,
            text="💾 Save Expense",
            bootstyle="success",
            command=self.save_expense
        ).grid(row=4, column=0, columnspan=2, pady=20)
        
        # History frame
        history_frame = ttk.LabelFrame(self.expenses_tab, text="📜 Expense History", padding=10)
        history_frame.pack(fill=BOTH, expand=True, padx=20, pady=10)
        
        columns = ("Date", "Category", "Amount", "Description")
        self.exp_tree = ttk.Treeview(history_frame, columns=columns, show="headings")
        for col in columns:
            self.exp_tree.heading(col, text=col)
            self.exp_tree.column(col, width=150)
        self.exp_tree.pack(fill=BOTH, expand=True)
        
        self.refresh_expenses()
    
    def save_expense(self):
        """Save expense to database"""
        date = self.exp_date.entry.get()
        category = self.exp_category.get()
        amount = self.exp_amount.get()
        description = self.exp_description.get()
        
        if not date or not category or not amount:
            ttk.messagebox.showerror("Error", "Please fill all required fields!")
            return
        
        try:
            amount = float(amount)
        except ValueError:
            ttk.messagebox.showerror("Error", "Amount must be a number!")
            return
        
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO expenses (date, category, amount, description)
            VALUES (?, ?, ?, ?)
        ''', (date, category, amount, description))
        
        conn.commit()
        conn.close()
        
        ttk.messagebox.showinfo("Success", "Expense saved!")
        
        self.exp_amount.delete(0, END)
        self.exp_description.delete(0, END)
        
        self.refresh_expenses()
    
    def refresh_expenses(self):
        """Refresh expenses history"""
        for item in self.exp_tree.get_children():
            self.exp_tree.delete(item)
        
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute("SELECT date, category, amount, description FROM expenses ORDER BY date DESC")
        for row in cursor.fetchall():
            self.exp_tree.insert("", END, values=row)
        conn.close()
    
    # ==================== BILLING ====================
    def build_billing(self):
        """Build billing/invoicing section"""
        # Client management frame
        client_frame = ttk.LabelFrame(self.billing_tab, text="👤 Client Management", padding=15)
        client_frame.pack(fill=X, padx=20, pady=10)
        
        # Client form
        ttk.Label(client_frame, text="Name:").grid(row=0, column=0, sticky=W, pady=5)
        self.client_name = ttk.Entry(client_frame, width=25)
        self.client_name.grid(row=0, column=1, padx=5, sticky=W)
        
        ttk.Label(client_frame, text="Phone:").grid(row=0, column=2, sticky=W, padx=5)
        self.client_phone = ttk.Entry(client_frame, width=20)
        self.client_phone.grid(row=0, column=3, padx=5, sticky=W)
        
        ttk.Label(client_frame, text="Address:").grid(row=1, column=0, sticky=W, pady=5)
        self.client_address = ttk.Entry(client_frame, width=25)
        self.client_address.grid(row=1, column=1, padx=5, sticky=W)
        
        ttk.Button(client_frame, text="➕ Add Client", bootstyle="success", 
                   command=self.add_client).grid(row=1, column=3, padx=5)
        
        # Invoice creation frame
        invoice_frame = ttk.LabelFrame(self.billing_tab, text="🧾 Create Invoice", padding=15)
        invoice_frame.pack(fill=X, padx=20, pady=10)
        
        # Client selection
        ttk.Label(invoice_frame, text="Select Client:").grid(row=0, column=0, sticky=W, pady=5)
        self.invoice_client = ttk.Combobox(invoice_frame, width=25)
        self.invoice_client.grid(row=0, column=1, padx=5, sticky=W)
        
        # Date
        ttk.Label(invoice_frame, text="Date:").grid(row=0, column=2, sticky=W, padx=5)
        self.invoice_date = ttk.DateEntry(invoice_frame)
        self.invoice_date.grid(row=0, column=3, padx=5, sticky=W)
        
        # Items
        ttk.Label(invoice_frame, text="Description:").grid(row=1, column=0, sticky=W, pady=5)
        self.inv_description = ttk.Entry(invoice_frame, width=25)
        self.inv_description.grid(row=1, column=1, padx=5, sticky=W)
        
        ttk.Label(invoice_frame, text="Qty:").grid(row=1, column=2, sticky=W, padx=5)
        self.inv_qty = ttk.Entry(invoice_frame, width=10)
        self.inv_qty.grid(row=1, column=3, padx=5, sticky=W)
        
        ttk.Label(invoice_frame, text="Unit Price (€):").grid(row=2, column=0, sticky=W, pady=5)
        self.inv_price = ttk.Entry(invoice_frame, width=25)
        self.inv_price.grid(row=2, column=1, padx=5, sticky=W)
        
        ttk.Button(invoice_frame, text="➕ Add Item", bootstyle="primary",
                   command=self.add_invoice_item).grid(row=2, column=2, columnspan=2, padx=5)
        
        # Invoice items list
        self.invoice_items = ttk.Treeview(invoice_frame, columns=("Description", "Qty", "Unit Price", "Total"), show="headings", height=6)
        self.invoice_items.heading("Description", text="Description")
        self.invoice_items.heading("Qty", text="Qty")
        self.invoice_items.heading("Unit Price", text="Unit Price")
        self.invoice_items.heading("Total", text="Total")
        self.invoice_items.column("Description", width=200)
        self.invoice_items.column("Qty", width=80)
        self.invoice_items.column("Unit Price", width=100)
        self.invoice_items.column("Total", width=100)
        self.invoice_items.grid(row=3, column=0, columnspan=4, pady=10, sticky="ew")
        
        # Invoice buttons
        btn_frame = ttk.Frame(invoice_frame)
        btn_frame.grid(row=4, column=0, columnspan=4, pady=10)
        
        ttk.Button(btn_frame, text="💾 Save Invoice", bootstyle="success", 
                   command=self.save_invoice).pack(side=LEFT, padx=5)
        ttk.Button(btn_frame, text="📄 Generate PDF", bootstyle="primary", 
                   command=self.generate_pdf).pack(side=LEFT, padx=5)
        
        # Load clients
        self.load_clients()
    
    def add_client(self):
        """Add a new client"""
        name = self.client_name.get()
        phone = self.client_phone.get()
        address = self.client_address.get()
        
        if not name:
            ttk.messagebox.showerror("Error", "Client name is required!")
            return
        
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO clients (name, phone, address) VALUES (?, ?, ?)", 
                     (name, phone, address))
        conn.commit()
        conn.close()
        
        ttk.messagebox.showinfo("Success", "Client added!")
        self.client_name.delete(0, END)
        self.client_phone.delete(0, END)
        self.client_address.delete(0, END)
        
        self.load_clients()
    
    def load_clients(self):
        """Load clients into combobox"""
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM clients")
        clients = [row[0] for row in cursor.fetchall()]
        conn.close()
        
        self.invoice_client['values'] = clients
    
    def add_invoice_item(self):
        """Add item to current invoice"""
        desc = self.inv_description.get()
        qty = self.inv_qty.get()
        price = self.inv_price.get()
        
        if not desc or not qty or not price:
            ttk.messagebox.showerror("Error", "Please fill all fields!")
            return
        
        try:
            qty = int(qty)
            price = float(price)
            total = qty * price
        except ValueError:
            ttk.messagebox.showerror("Error", "Qty must be integer and price must be number!")
            return
        
        self.invoice_items.insert("", END, values=(desc, qty, f"€{price:.2f}", f"€{total:.2f}"))
        
        self.inv_description.delete(0, END)
        self.inv_qty.delete(0, END)
        self.inv_price.delete(0, END)
    
    def save_invoice(self):
        """Save invoice to database"""
        client_name = self.invoice_client.get()
        date = self.invoice_date.entry.get()
        
        if not client_name or not date:
            ttk.messagebox.showerror("Error", "Please select client and date!")
            return
        
        # Get client ID
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM clients WHERE name = ?", (client_name,))
        client_result = cursor.fetchone()
        
        if not client_result:
            conn.close()
            ttk.messagebox.showerror("Error", "Client not found!")
            return
        
        client_id = client_result[0]
        
        # Generate invoice number
        invoice_num = f"INV-{datetime.now().strftime('%Y%m%d%H%M%S')}"
        
        # Calculate total
        total = 0
        for item in self.invoice_items.get_children():
            values = self.invoice_items.item(item)['values']
            total += float(values[3].replace('€', ''))
        
        # Insert invoice
        cursor.execute("INSERT INTO invoices (invoice_number, client_id, date, total_amount) VALUES (?, ?, ?, ?)",
                      (invoice_num, client_id, date, total))
        invoice_id = cursor.lastrowid
        
        # Insert items
        for item in self.invoice_items.get_children():
            values = self.invoice_items.item(item)['values']
            cursor.execute("INSERT INTO invoice_items (invoice_id, description, quantity, unit_price, total) VALUES (?, ?, ?, ?, ?)",
                          (invoice_id, values[0], values[1], float(values[2].replace('€', '')), float(values[3].replace('€', ''))))
        
        conn.commit()
        conn.close()
        
        ttk.messagebox.showinfo("Success", f"Invoice {invoice_num} saved!")
        
        # Clear form
        for item in self.invoice_items.get_children():
            self.invoice_items.delete(item)
    
    def generate_pdf(self):
        """Generate PDF invoice"""
        client_name = self.invoice_client.get()
        date = self.invoice_date.entry.get()
        
        if not client_name or not self.invoice_items.get_children():
            ttk.messagebox.showerror("Error", "Please select client and add items!")
            return
        
        # Generate filename
        filename = f"Invoice_{client_name}_{datetime.now().strftime('%Y%m%d')}.pdf"
        
        # Create PDF
        c = canvas.Canvas(filename, pagesize=A4)
        width, height = A4
        
        # Header
        c.setFont("Helvetica-Bold", 24)
        c.drawString(50, height - 50, "INVOICE")
        
        # Client info
        c.setFont("Helvetica", 12)
        c.drawString(50, height - 100, f"Client: {client_name}")
        c.drawString(50, height - 120, f"Date: {date}")
        
        # Items header
        y = height - 160
        c.setFont("Helvetica-Bold", 10)
        c.drawString(50, y, "Description")
        c.drawString(300, y, "Qty")
        c.drawString(360, y, "Unit Price")
        c.drawString(450, y, "Total")
        
        # Items
        c.setFont("Helvetica", 10)
        y -= 20
        total = 0
        for item in self.invoice_items.get_children():
            values = self.invoice_items.item(item)['values']
            c.drawString(50, y, values[0])
            c.drawString(300, y, str(values[1]))
            c.drawString(360, y, values[2])
            c.drawString(450, y, values[3])
            total += float(values[3].replace('€', ''))
            y -= 20
        
        # Total
        y -= 30
        c.setFont("Helvetica-Bold", 12)
        c.drawString(350, y, "TOTAL:")
        c.drawString(450, y, f"€{total:.2f}")
        
        c.save()
        
        ttk.messagebox.showinfo("Success", f"PDF saved as {filename}")
        os.system(f"xdg-open {filename}" if os.name != 'nt' else filename)
    
    # ==================== REPORTS ====================
    def build_reports(self):
        """Build reports section"""
        # Report controls
        control_frame = ttk.Frame(self.reports_tab)
        control_frame.pack(fill=X, padx=20, pady=20)
        
        ttk.Label(control_frame, text="📈 Generate Report:", font=("Helvetica", 12, "bold")).pack(side=LEFT, padx=10)
        
        ttk.Button(control_frame, text="📊 Weekly Summary", bootstyle="primary",
                  command=self.weekly_report).pack(side=LEFT, padx=5)
        
        ttk.Button(control_frame, text="📅 Monthly Summary", bootstyle="primary",
                  command=self.monthly_report).pack(side=LEFT, padx=5)
        
        ttk.Button(control_frame, text="💰 Expense Report", bootstyle="warning",
                  command=self.expense_report).pack(side=LEFT, padx=5)
        
        # Report output
        report_frame = ttk.LabelFrame(self.reports_tab, text="📋 Report Output", padding=15)
        report_frame.pack(fill=BOTH, expand=True, padx=20, pady=10)
        
        self.report_text = ttk.Text(report_frame, font=("Consolas", 10), height=20)
        self.report_text.pack(fill=BOTH, expand=True)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(self.report_text)
        scrollbar.pack(side=RIGHT, fill=Y)
        self.report_text.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.report_text.yview)
    
    def weekly_report(self):
        """Generate weekly production report"""
        self.report_text.delete(1.0, END)
        self.report_text.insert(END, "📊 WEEKLY PRODUCTION REPORT\n")
        self.report_text.insert(END, "=" * 40 + "\n\n")
        
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        
        # Last 7 days
        cursor.execute("""
            SELECT date, stock, mortality, production 
            FROM daily_entries 
            ORDER BY date DESC 
            LIMIT 7
        """)
        
        results = cursor.fetchall()
        
        if results:
            total_production = sum(r[3] for r in results)
            total_mortality = sum(r[2] for r in results)
            
            for row in results:
                self.report_text.insert(END, f"Date: {row[0]} | Stock: {row[1]} | Mortality: {row[2]} | Production: {row[3]}\n")
            
            self.report_text.insert(END, f"\n📈 Total Production (7 days): {total_production}\n")
            self.report_text.insert(END, f"☠️ Total Mortality (7 days): {total_mortality}\n")
        else:
            self.report_text.insert(END, "No data available!\n")
        
        conn.close()
    
    def monthly_report(self):
        """Generate monthly report"""
        self.report_text.delete(1.0, END)
        self.report_text.insert(END, "📅 MONTHLY SUMMARY REPORT\n")
        self.report_text.insert(END, "=" * 40 + "\n\n")
        
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        
        month = datetime.now().strftime("%Y-%m")
        
        # Production
        cursor.execute(f"""
            SELECT SUM(production), SUM(mortality), AVG(stock)
            FROM daily_entries 
            WHERE date LIKE '{month}%'
        """)
        
        result = cursor.fetchone()
        
        if result and result[0]:
            self.report_text.insert(END, f"Month: {month}\n\n")
            self.report_text.insert(END, f"🥚 Total Production: {result[0]}\n")
            self.report_text.insert(END, f"☠️ Total Mortality: {result[1]}\n")
            self.report_text.insert(END, f"🐔 Average Stock: {result[2]:.0f}\n")
        else:
            self.report_text.insert(END, "No data available for this month!\n")
        
        conn.close()
    
    def expense_report(self):
        """Generate expense report"""
        self.report_text.delete(1.0, END)
        self.report_text.insert(END, "💰 EXPENSE REPORT\n")
        self.report_text.insert(END, "=" * 40 + "\n\n")
        
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        
        # By category
        cursor.execute("""
            SELECT category, SUM(amount) as total
            FROM expenses
            GROUP BY category
            ORDER BY total DESC
        """)
        
        categories = cursor.fetchall()
        
        if categories:
            grand_total = 0
            self.report_text.insert(END, "By Category:\n")
            self.report_text.insert(END, "-" * 30 + "\n")
            
            for cat, total in categories:
                self.report_text.insert(END, f"{cat}: €{total:.2f}\n")
                grand_total += total
            
            self.report_text.insert(END, "-" * 30 + "\n")
            self.report_text.insert(END, f"💵 GRAND TOTAL: €{grand_total:.2f}\n")
        else:
            self.report_text.insert(END, "No expenses recorded!\n")
        
        conn.close()


def main():
    app = PoultryFarmApp()
    app.mainloop()


if __name__ == "__main__":
    main()
