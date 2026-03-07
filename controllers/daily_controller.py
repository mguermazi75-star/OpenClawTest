"""
Controller for daily entries - Business logic
"""

from models import get_connection, DailyEntry
from typing import List, Optional
from datetime import datetime


class DailyController:
    """Business logic for daily entries"""
    
    @staticmethod
    def save_entry(entry: DailyEntry) -> bool:
        """Save a daily entry to database"""
        conn = get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO daily_entries (date, mortality, production, eggs_sold, egg_price, notes)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (entry.date, entry.mortality, entry.production, entry.eggs_sold, entry.egg_price, entry.notes))
        
        conn.commit()
        conn.close()
        return True
    
    @staticmethod
    def get_all_entries(limit: int = 100) -> List[DailyEntry]:
        """Get all daily entries"""
        conn = get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT id, date, mortality, production, eggs_sold, egg_price, notes
            FROM daily_entries
            ORDER BY date DESC
            LIMIT ?
        ''', (limit,))
        
        rows = cursor.fetchall()
        conn.close()
        
        entries = []
        for row in rows:
            entries.append(DailyEntry(
                id=row[0],
                date=row[1],
                mortality=row[2],
                production=row[3],
                eggs_sold=row[4] or 0,
                egg_price=row[5] or 0.0,
                notes=row[6] or ""
            ))
        
        return entries
    
    @staticmethod
    def get_latest_entry() -> Optional[DailyEntry]:
        """Get most recent entry"""
        conn = get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT id, date, mortality, production, eggs_sold, egg_price, notes
            FROM daily_entries
            ORDER BY date DESC
            LIMIT 1
        ''')
        
        row = cursor.fetchone()
        conn.close()
        
        if row:
            return DailyEntry(
                id=row[0],
                date=row[1],
                mortality=row[2],
                production=row[3],
                eggs_sold=row[4] or 0,
                egg_price=row[5] or 0.0,
                notes=row[6] or ""
            )
        return None
    
    @staticmethod
    def get_entries_for_week(limit: int = 7) -> List[DailyEntry]:
        """Get entries for last N days"""
        conn = get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT id, date, mortality, production, eggs_sold, egg_price, notes
            FROM daily_entries
            ORDER BY date DESC
            LIMIT ?
        ''', (limit,))
        
        rows = cursor.fetchall()
        conn.close()
        
        return [
            DailyEntry(
                id=row[0],
                date=row[1],
                mortality=row[2],
                production=row[3],
                eggs_sold=row[4] or 0,
                egg_price=row[5] or 0.0,
                notes=row[6] or ""
            )
            for row in rows
        ]
    
    @staticmethod
    def get_monthly_totals() -> dict:
        """Get monthly totals"""
        conn = get_connection()
        cursor = conn.cursor()
        
        month = datetime.now().strftime("%Y-%m")
        
        cursor.execute(f'''
            SELECT 
                COALESCE(SUM(production), 0) as total_production,
                COALESCE(SUM(mortality), 0) as total_mortality,
                COALESCE(SUM(eggs_sold), 0) as total_sold
            FROM daily_entries 
            WHERE date LIKE '{month}%'
        ''')
        
        row = cursor.fetchone()
        conn.close()
        
        return {
            'production': row[0],
            'mortality': row[1],
            'eggs_sold': row[2]
        }
    
    @staticmethod
    def delete_entry(entry_id: int) -> bool:
        """Delete an entry"""
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('DELETE FROM daily_entries WHERE id = ?', (entry_id,))
        conn.commit()
        conn.close()
        return True
    
    @staticmethod
    def delete_entry_by_date(date: str) -> bool:
        """Delete an entry by date"""
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('DELETE FROM daily_entries WHERE date = ?', (date,))
        conn.commit()
        conn.close()
        return True
