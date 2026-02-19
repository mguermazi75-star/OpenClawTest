"""
Daily Entry view - Form for daily stock/mortality/production
"""

import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from ttkbootstrap.widgets import DateEntry
from controllers import DailyController
from models import DailyEntry


def create_daily_entry_view(parent):
    """Create and return daily entry form frame"""
    frame = ttk.Frame(parent)
    
    # Form frame
    form_frame = ttk.LabelFrame(frame, text="📝 Daily Data Entry", padding=20)
    form_frame.pack(fill=X, padx=20, pady=20)
    
    # Date
    ttk.Label(form_frame, text="📅 Date:").grid(row=0, column=0, sticky=W, pady=10)
    date_entry = DateEntry(form_frame)
    date_entry.grid(row=0, column=1, padx=10, sticky=W)
    
    # Stock
    ttk.Label(form_frame, text="🐔 Current Stock:").grid(row=1, column=0, sticky=W, pady=10)
    stock_entry = ttk.Entry(form_frame, width=30)
    stock_entry.grid(row=1, column=1, padx=10, sticky=W)
    
    # Mortality
    ttk.Label(form_frame, text="☠️ Mortality:").grid(row=2, column=0, sticky=W, pady=10)
    mortality_entry = ttk.Entry(form_frame, width=30)
    mortality_entry.grid(row=2, column=1, padx=10, sticky=W)
    
    # Production
    ttk.Label(form_frame, text="🥚 Production:").grid(row=3, column=0, sticky=W, pady=10)
    production_entry = ttk.Entry(form_frame, width=30)
    production_entry.grid(row=3, column=1, padx=10, sticky=W)
    
    # Notes
    ttk.Label(form_frame, text="📋 Notes:").grid(row=4, column=0, sticky=W, pady=10)
    notes_entry = ttk.Entry(form_frame, width=30)
    notes_entry.grid(row=4, column=1, padx=10, sticky=W)
    
    # Message label
    message_label = ttk.Label(form_frame, text="", bootstyle="success")
    message_label.grid(row=6, column=0, columnspan=2, pady=10)
    
    def save_entry():
        """Save the daily entry"""
        date = date_entry.entry.get()
        stock = stock_entry.get()
        mortality = mortality_entry.get()
        production = production_entry.get()
        notes = notes_entry.get()
        
        if not date:
            message_label.config(text="❌ Please select a date!", bootstyle="danger")
            return
        
        entry = DailyEntry(
            date=date,
            stock=int(stock) if stock else 0,
            mortality=int(mortality) if mortality else 0,
            production=int(production) if production else 0,
            notes=notes
        )
        
        DailyController.save_entry(entry)
        
        message_label.config(text="✅ Entry saved!", bootstyle="success")
        
        # Clear form
        stock_entry.delete(0, END)
        mortality_entry.delete(0, END)
        production_entry.delete(0, END)
        notes_entry.delete(0, END)
        
        # Refresh history
        refresh_history()
    
    # Save button
    ttk.Button(
        form_frame,
        text="💾 Save Entry",
        bootstyle="success",
        command=save_entry
    ).grid(row=5, column=0, columnspan=2, pady=20)
    
    # History frame
    history_frame = ttk.LabelFrame(frame, text="📜 Entry History", padding=10)
    history_frame.pack(fill=BOTH, expand=True, padx=20, pady=10)
    
    # Treeview
    columns = ("Date", "Stock", "Mortality", "Production", "Notes")
    tree = ttk.Treeview(history_frame, columns=columns, show="headings")
    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, width=150)
    tree.pack(fill=BOTH, expand=True)
    
    def refresh_history():
        """Refresh the history treeview"""
        for item in tree.get_children():
            tree.delete(item)
        
        entries = DailyController.get_all_entries()
        for entry in entries:
            tree.insert("", END, values=(
                entry.date, 
                entry.stock, 
                entry.mortality, 
                entry.production,
                entry.notes
            ))
    
    # Initial load
    refresh_history()
    
    # Store refresh function for external calls
    frame.refresh_history = refresh_history
    
    return frame
