"""
Billing view - Client & Invoice management
"""

import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from controllers import BillingController
from models import Client
from utils import PDFGenerator
from datetime import datetime
import os


def create_billing_view(parent):
    """Create and return billing form frame"""
    frame = ttk.Frame(parent)
    
    # ==================== CLIENT MANAGEMENT ====================
    client_frame = ttk.LabelFrame(frame, text="👤 Client Management", padding=15)
    client_frame.pack(fill=X, padx=20, pady=10)
    
    # Client form
    ttk.Label(client_frame, text="Name:").grid(row=0, column=0, sticky=W, pady=5)
    client_name = ttk.Entry(client_frame, width=25)
    client_name.grid(row=0, column=1, padx=5, sticky=W)
    
    ttk.Label(client_frame, text="Phone:").grid(row=0, column=2, sticky=W, padx=5)
    client_phone = ttk.Entry(client_frame, width=20)
    client_phone.grid(row=0, column=3, padx=5, sticky=W)
    
    ttk.Label(client_frame, text="Address:").grid(row=1, column=0, sticky=W, pady=5)
    client_address = ttk.Entry(client_frame, width=25)
    client_address.grid(row=1, column=1, padx=5, sticky=W)
    
    client_message = ttk.Label(client_frame, text="", bootstyle="success")
    client_message.grid(row=1, column=3, padx=5)
    
    def add_client():
        name = client_name.get()
        phone = client_phone.get()
        address = client_address.get()
        
        if not name:
            client_message.config(text="❌ Name required", bootstyle="danger")
            return
        
        BillingController.add_client(Client(name=name, phone=phone, address=address))
        
        client_message.config(text="✅ Client added!", bootstyle="success")
        client_name.delete(0, END)
        client_phone.delete(0, END)
        client_address.delete(0, END)
        
        load_clients()
    
    ttk.Button(client_frame, text="➕ Add Client", bootstyle="success", 
               command=add_client).grid(row=1, column=2, padx=5)
    
    # ==================== INVOICE CREATION ====================
    invoice_frame = ttk.LabelFrame(frame, text="🧾 Create Invoice", padding=15)
    invoice_frame.pack(fill=X, padx=20, pady=10)
    
    # Client selection
    ttk.Label(invoice_frame, text="Select Client:").grid(row=0, column=0, sticky=W, pady=5)
    client_combo = ttk.Combobox(invoice_frame, width=25)
    client_combo.grid(row=0, column=1, padx=5, sticky=W)
    
    # Date
    ttk.Label(invoice_frame, text="Date:").grid(row=0, column=2, sticky=W, padx=5)
    invoice_date = ttk.DateEntry(invoice_frame)
    invoice_date.grid(row=0, column=3, padx=5, sticky=W)
    
    # Item form
    ttk.Label(invoice_frame, text="Description:").grid(row=1, column=0, sticky=W, pady=5)
    item_desc = ttk.Entry(invoice_frame, width=25)
    item_desc.grid(row=1, column=1, padx=5, sticky=W)
    
    ttk.Label(invoice_frame, text="Qty:").grid(row=1, column=2, sticky=W, padx=5)
    item_qty = ttk.Entry(invoice_frame, width=10)
    item_qty.grid(row=1, column=3, padx=5, sticky=W)
    
    ttk.Label(invoice_frame, text="Unit Price (€):").grid(row=2, column=0, sticky=W, pady=5)
    item_price = ttk.Entry(invoice_frame, width=25)
    item_price.grid(row=2, column=1, padx=5, sticky=W)
    
    current_items = []
    
    def add_item():
        desc = item_desc.get()
        qty = item_qty.get()
        price = item_price.get()
        
        if not desc or not qty or not price:
            return
        
        try:
            qty = int(qty)
            price = float(price)
            total = qty * price
        except ValueError:
            return
        
        current_items.append({'description': desc, 'qty': qty, 'unit_price': price})
        
        invoice_items.insert("", END, values=(desc, qty, f"€{price:.2f}", f"€{total:.2f}"))
        
        item_desc.delete(0, END)
        item_qty.delete(0, END)
        item_price.delete(0, END)
    
    ttk.Button(invoice_frame, text="➕ Add Item", bootstyle="primary",
               command=add_item).grid(row=2, column=2, columnspan=2, padx=5, pady=5)
    
    # Invoice items list
    invoice_items = ttk.Treeview(
        invoice_frame, 
        columns=("Description", "Qty", "Unit Price", "Total"), 
        show="headings", 
        height=6
    )
    invoice_items.heading("Description", text="Description")
    invoice_items.heading("Qty", text="Qty")
    invoice_items.heading("Unit Price", text="Unit Price")
    invoice_items.heading("Total", text="Total")
    invoice_items.column("Description", width=200)
    invoice_items.column("Qty", width=80)
    invoice_items.column("Unit Price", width=100)
    invoice_items.column("Total", width=100)
    invoice_items.grid(row=3, column=0, columnspan=4, pady=10, sticky="ew")
    
    invoice_message = ttk.Label(invoice_frame, text="", bootstyle="success")
    invoice_message.grid(row=4, column=0, columnspan=4)
    
    # Invoice buttons
    btn_frame = ttk.Frame(invoice_frame)
    btn_frame.grid(row=5, column=0, columnspan=4, pady=10)
    
    def save_invoice():
        client = client_combo.get()
        date = invoice_date.entry.get()
        
        if not client or not current_items:
            invoice_message.config(text="❌ Select client and add items!", bootstyle="danger")
            return
        
        # Get client ID
        clients = BillingController.get_all_clients()
        client_obj = next((c for c in clients if c.name == client), None)
        
        if not client_obj:
            invoice_message.config(text="❌ Client not found!", bootstyle="danger")
            return
        
        invoice_num = BillingController.create_invoice(
            client_obj.id,
            current_items,
            date
        )
        
        invoice_message.config(text=f"✅ Invoice {invoice_num} saved!", bootstyle="success")
        
        # Clear
        for item in invoice_items.get_children():
            invoice_items.delete(item)
        current_items.clear()
    
    def generate_pdf():
        client = client_combo.get()
        date = invoice_date.entry.get()
        
        if not client or not current_items:
            invoice_message.config(text="❌ Select client and add items!", bootstyle="danger")
            return
        
        filename = f"Invoice_{client}_{datetime.now().strftime('%Y%m%d')}.pdf"
        
        PDFGenerator.generate_simple_invoice(client, current_items, filename)
        
        invoice_message.config(text=f"✅ PDF saved as {filename}", bootstyle="success")
        
        # Open PDF
        if os.name != 'nt':
            os.system(f"xdg-open {filename}")
    
    ttk.Button(btn_frame, text="💾 Save Invoice", bootstyle="success", 
               command=save_invoice).pack(side=LEFT, padx=5)
    ttk.Button(btn_frame, text="📄 Generate PDF", bootstyle="primary", 
               command=generate_pdf).pack(side=LEFT, padx=5)
    
    # Load clients
    def load_clients():
        clients = BillingController.get_all_clients()
        client_combo['values'] = [c.name for c in clients]
    
    load_clients()
    frame.load_clients = load_clients
    
    return frame
