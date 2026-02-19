"""
Controller for reports - Business logic
"""

from models import get_connection
from typing import Dict, List
from datetime import datetime


class ReportController:
    """Business logic for generating reports"""
    
    @staticmethod
    def generate_weekly_report() -> Dict:
        """Generate weekly production report"""
        conn = get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT date, stock, mortality, production
            FROM daily_entries
            ORDER BY date DESC
            LIMIT 7
        ''')
        
        rows = cursor.fetchall()
        conn.close()
        
        if not rows:
            return {'success': False, 'message': 'No data available'}
        
        entries = [
            {
                'date': row[0],
                'stock': row[1],
                'mortality': row[2],
                'production': row[3]
            }
            for row in rows
        ]
        
        total_production = sum(e['production'] for e in entries)
        total_mortality = sum(e['mortality'] for e in entries)
        
        return {
            'success': True,
            'entries': entries,
            'total_production': total_production,
            'total_mortality': total_mortality
        }
    
    @staticmethod
    def generate_monthly_report(month: str = None) -> Dict:
        """Generate monthly report"""
        if month is None:
            month = datetime.now().strftime("%Y-%m")
        
        conn = get_connection()
        cursor = conn.cursor()
        
        cursor.execute(f'''
            SELECT 
                COALESCE(SUM(production), 0),
                COALESCE(SUM(mortality), 0),
                COALESCE(AVG(stock), 0),
                COUNT(*)
            FROM daily_entries 
            WHERE date LIKE '{month}%'
        ''')
        
        row = cursor.fetchone()
        conn.close()
        
        if row[3] == 0:
            return {'success': False, 'message': f'No data for {month}'}
        
        return {
            'success': True,
            'month': month,
            'total_production': row[0],
            'total_mortality': row[1],
            'avg_stock': round(row[2], 0),
            'days_recorded': row[3]
        }
    
    @staticmethod
    def generate_expense_report() -> Dict:
        """Generate expense report by category"""
        conn = get_connection()
        cursor = conn.cursor()
        
        # By category
        cursor.execute('''
            SELECT category, SUM(amount) as total
            FROM expenses
            GROUP BY category
            ORDER BY total DESC
        ''')
        
        categories = cursor.fetchall()
        
        # Total
        cursor.execute('SELECT COALESCE(SUM(amount), 0) FROM expenses')
        grand_total = cursor.fetchone()[0]
        
        conn.close()
        
        if not categories:
            return {'success': False, 'message': 'No expenses recorded'}
        
        return {
            'success': True,
            'categories': [
                {'category': row[0], 'total': row[1]}
                for row in categories
            ],
            'grand_total': grand_total
        }
    
    @staticmethod
    def generate_profit_loss_report(month: str = None) -> Dict:
        """Generate profit/loss report"""
        if month is None:
            month = datetime.now().strftime("%Y-%m")
        
        # Get revenue (from invoices)
        conn = get_connection()
        cursor = conn.cursor()
        
        cursor.execute(f'''
            SELECT COALESCE(SUM(total_amount), 0)
            FROM invoices
            WHERE date LIKE '{month}%' AND status = 'paid'
        ''')
        revenue = cursor.fetchone()[0]
        
        # Get expenses
        cursor.execute(f'''
            SELECT COALESCE(SUM(amount), 0)
            FROM expenses
            WHERE date LIKE '{month}%'
        ''')
        expenses = cursor.fetchone()[0]
        
        conn.close()
        
        profit = revenue - expenses
        
        return {
            'success': True,
            'month': month,
            'revenue': revenue,
            'expenses': expenses,
            'profit': profit,
            'profit_margin': (profit / revenue * 100) if revenue > 0 else 0
        }
    
    @staticmethod
    def get_mortality_rate(days: int = 7) -> float:
        """Calculate mortality rate for last N days"""
        conn = get_connection()
        cursor = conn.cursor()
        
        cursor.execute(f'''
            SELECT COALESCE(SUM(mortality), 0), COALESCE(SUM(stock), 0)
            FROM daily_entries
            ORDER BY date DESC
            LIMIT {days}
        ''')
        
        row = cursor.fetchone()
        conn.close()
        
        if row[1] > 0:
            return (row[0] / row[1]) * 100
        return 0.0
    
    @staticmethod
    def get_production_stats(days: int = 30) -> Dict:
        """Get production statistics"""
        conn = get_connection()
        cursor = conn.cursor()
        
        cursor.execute(f'''
            SELECT 
                COALESCE(AVG(production), 0),
                COALESCE(MAX(production), 0),
                COALESCE(MIN(production), 0),
                COALESCE(SUM(production), 0)
            FROM daily_entries
            ORDER BY date DESC
            LIMIT {days}
        ''')
        
        row = cursor.fetchone()
        conn.close()
        
        return {
            'avg_daily': round(row[0], 1),
            'max_daily': row[1],
            'min_daily': row[2],
            'total': row[3]
        }
