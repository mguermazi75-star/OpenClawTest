"""
Controller for expenses - Business logic
"""

from models import get_connection, Expense
from typing import List, Optional, Dict
from datetime import datetime


class ExpenseController:
    """Business logic for expenses"""
    
    @staticmethod
    def save_expense(expense: Expense) -> bool:
        """Save an expense"""
        conn = get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO expenses (date, category, amount, description)
            VALUES (?, ?, ?, ?)
        ''', (expense.date, expense.category, expense.amount, expense.description))
        
        conn.commit()
        conn.close()
        return True
    
    @staticmethod
    def get_all_expenses(limit: int = 100) -> List[Expense]:
        """Get all expenses"""
        conn = get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT id, date, category, amount, description
            FROM expenses
            ORDER BY date DESC
            LIMIT ?
        ''', (limit,))
        
        rows = cursor.fetchall()
        conn.close()
        
        return [
            Expense(
                id=row[0],
                date=row[1],
                category=row[2],
                amount=row[3],
                description=row[4] or ""
            )
            for row in rows
        ]
    
    @staticmethod
    def get_monthly_expenses() -> float:
        """Get total expenses for current month"""
        conn = get_connection()
        cursor = conn.cursor()
        
        month = datetime.now().strftime("%Y-%m")
        
        cursor.execute('''
            SELECT COALESCE(SUM(amount), 0)
            FROM expenses
            WHERE date LIKE ?
        ''', (f"{month}%",))
        
        result = cursor.fetchone()[0]
        conn.close()
        return float(result) if result else 0.0
    
    @staticmethod
    def get_expenses_by_category() -> List[Dict]:
        """Get expenses grouped by category"""
        conn = get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT category, SUM(amount) as total
            FROM expenses
            GROUP BY category
            ORDER BY total DESC
        ''')
        
        rows = cursor.fetchall()
        conn.close()
        
        return [
            {'category': row[0], 'total': row[1]}
            for row in rows
        ]
    
    @staticmethod
    def get_expenses_for_month(month: str = None) -> List[Expense]:
        """Get expenses for a specific month (YYYY-MM)"""
        if month is None:
            month = datetime.now().strftime("%Y-%m")
        
        conn = get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT id, date, category, amount, description
            FROM expenses
            WHERE date LIKE ?
            ORDER BY date DESC
        ''', (f"{month}%",))
        
        rows = cursor.fetchall()
        conn.close()
        
        return [
            Expense(
                id=row[0],
                date=row[1],
                category=row[2],
                amount=row[3],
                description=row[4] or ""
            )
            for row in rows
        ]
    
    @staticmethod
    def delete_expense(expense_id: int) -> bool:
        """Delete an expense"""
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('DELETE FROM expenses WHERE id = ?', (expense_id,))
        conn.commit()
        conn.close()
        return True
