"""
Reports view - Report generation UI
"""

import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from controllers import ReportController


def create_reports_view(parent):
    """Create and return reports frame"""
    frame = ttk.Frame(parent)
    frame.pack(fill=BOTH, expand=True)
    
    # Controls
    control_frame = ttk.Frame(frame)
    control_frame.pack(fill=X, padx=20, pady=20)
    
    ttk.Label(control_frame, text="📈 Generate Report:", font=("Helvetica", 12, "bold")).pack(side=LEFT, padx=10)
    
    ttk.Button(control_frame, text="📊 Weekly Summary", bootstyle="primary",
              command=lambda: generate_report("weekly")).pack(side=LEFT, padx=5)
    
    ttk.Button(control_frame, text="📅 Monthly Summary", bootstyle="primary",
              command=lambda: generate_report("monthly")).pack(side=LEFT, padx=5)
    
    ttk.Button(control_frame, text="💰 Expense Report", bootstyle="warning",
              command=lambda: generate_report("expense")).pack(side=LEFT, padx=5)
    
    ttk.Button(control_frame, text="📈 Profit/Loss", bootstyle="info",
              command=lambda: generate_report("profit")).pack(side=LEFT, padx=5)
    
    # Report output
    report_frame = ttk.LabelFrame(frame, text="📋 Report Output", padding=15)
    report_frame.pack(fill=BOTH, expand=True, padx=20, pady=10)
    
    report_text = ttk.Text(report_frame, font=("Consolas", 10), height=20)
    report_text.pack(fill=BOTH, expand=True)
    
    scrollbar = ttk.Scrollbar(report_text)
    scrollbar.pack(side=RIGHT, fill=Y)
    report_text.config(yscrollcommand=scrollbar.set)
    scrollbar.config(command=report_text.yview)
    
    def generate_report(report_type: str):
        """Generate and display report"""
        report_text.delete(1.0, END)
        
        if report_type == "weekly":
            data = ReportController.generate_weekly_report()
            
            if not data.get('success'):
                report_text.insert(END, "📊 WEEKLY PRODUCTION REPORT\n")
                report_text.insert(END, "=" * 40 + "\n\n")
                report_text.insert(END, f"❌ {data.get('message', 'No data')}\n")
                return
            
            report_text.insert(END, "📊 WEEKLY PRODUCTION REPORT\n")
            report_text.insert(END, "=" * 40 + "\n\n")
            
            for entry in data['entries']:
                report_text.insert(END, 
                    f"Date: {entry['date']} | Stock: {entry['stock']} | "
                    f"Mortality: {entry['mortality']} | Production: {entry['production']}\n")
            
            report_text.insert(END, f"\n📈 Total Production (7 days): {data['total_production']}\n")
            report_text.insert(END, f"☠️ Total Mortality (7 days): {data['total_mortality']}\n")
            
        elif report_type == "monthly":
            data = ReportController.generate_monthly_report()
            
            if not data.get('success'):
                report_text.insert(END, "📅 MONTHLY SUMMARY REPORT\n")
                report_text.insert(END, "=" * 40 + "\n\n")
                report_text.insert(END, f"❌ {data.get('message', 'No data')}\n")
                return
            
            report_text.insert(END, "📅 MONTHLY SUMMARY REPORT\n")
            report_text.insert(END, "=" * 40 + "\n\n")
            report_text.insert(END, f"Month: {data['month']}\n\n")
            report_text.insert(END, f"🥚 Total Production: {data['total_production']}\n")
            report_text.insert(END, f"☠️ Total Mortality: {data['total_mortality']}\n")
            report_text.insert(END, f"🐔 Average Stock: {data['avg_stock']:.0f}\n")
            report_text.insert(END, f"📝 Days Recorded: {data['days_recorded']}\n")
            
        elif report_type == "expense":
            data = ReportController.generate_expense_report()
            
            if not data.get('success'):
                report_text.insert(END, "💰 EXPENSE REPORT\n")
                report_text.insert(END, "=" * 40 + "\n\n")
                report_text.insert(END, f"❌ {data.get('message', 'No data')}\n")
                return
            
            report_text.insert(END, "💰 EXPENSE REPORT\n")
            report_text.insert(END, "=" * 40 + "\n\n")
            report_text.insert(END, "By Category:\n")
            report_text.insert(END, "-" * 30 + "\n")
            
            for cat in data['categories']:
                report_text.insert(END, f"{cat['category']}: €{cat['total']:.2f}\n")
            
            report_text.insert(END, "-" * 30 + "\n")
            report_text.insert(END, f"💵 GRAND TOTAL: €{data['grand_total']:.2f}\n")
            
        elif report_type == "profit":
            data = ReportController.generate_profit_loss_report()
            
            report_text.insert(END, "📈 PROFIT/LOSS REPORT\n")
            report_text.insert(END, "=" * 40 + "\n\n")
            report_text.insert(END, f"Month: {data['month']}\n\n")
            report_text.insert(END, f"💚 Revenue: €{data['revenue']:.2f}\n")
            report_text.insert(END, f"❤️ Expenses: €{data['expenses']:.2f}\n")
            report_text.insert(END, "-" * 30 + "\n")
            
            profit = data['profit']
            if profit >= 0:
                report_text.insert(END, f"✅ Profit: €{profit:.2f}\n")
            else:
                report_text.insert(END, f"❌ Loss: €{abs(profit):.2f}\n")
            
            report_text.insert(END, f"📊 Profit Margin: {data['profit_margin']:.1f}%\n")
    
    # Store for external access
    frame.generate_report = generate_report
    
    return frame
