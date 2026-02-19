"""
Controller for billing/invoices - Business logic
"""

from models import get_connection, Client, Invoice, InvoiceItem
from typing import List, Dict, Optional
from datetime import datetime


class BillingController:
    """Business logic for clients and invoices"""
    
    # ==================== CLIENTS ====================
    
    @staticmethod
    def add_client(client: Client) -> int:
        """Add a new client, returns client ID"""
        conn = get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO clients (name, phone, address)
            VALUES (?, ?, ?)
        ''', (client.name, client.phone, client.address))
        
        client_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return client_id
    
    @staticmethod
    def get_all_clients() -> List[Client]:
        """Get all clients"""
        conn = get_connection()
        cursor = conn.cursor()
        
        cursor.execute('SELECT id, name, phone, address FROM clients ORDER BY name')
        rows = cursor.fetchall()
        conn.close()
        
        return [
            Client(id=row[0], name=row[1], phone=row[2] or "", address=row[3] or "")
            for row in rows
        ]
    
    @staticmethod
    def get_client_by_id(client_id: int) -> Optional[Client]:
        """Get client by ID"""
        conn = get_connection()
        cursor = conn.cursor()
        
        cursor.execute('SELECT id, name, phone, address FROM clients WHERE id = ?', (client_id,))
        row = cursor.fetchone()
        conn.close()
        
        if row:
            return Client(id=row[0], name=row[1], phone=row[2] or "", address=row[3] or "")
        return None
    
    @staticmethod
    def delete_client(client_id: int) -> bool:
        """Delete a client"""
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('DELETE FROM clients WHERE id = ?', (client_id,))
        conn.commit()
        conn.close()
        return True
    
    # ==================== INVOICES ====================
    
    @staticmethod
    def create_invoice(
        client_id: int,
        items: List[Dict],
        date: str = None
    ) -> str:
        """
        Create a new invoice with items.
        
        Args:
            client_id: ID of the client
            items: List of dicts with description, qty, unit_price
            date: Invoice date (defaults to today)
            
        Returns:
            Invoice number
        """
        if date is None:
            date = datetime.now().strftime("%Y-%m-%d")
        
        # Generate invoice number
        invoice_number = f"INV-{datetime.now().strftime('%Y%m%d%H%M%S')}"
        
        # Calculate total
        total = sum(item['qty'] * item['unit_price'] for item in items)
        
        conn = get_connection()
        cursor = conn.cursor()
        
        # Insert invoice
        cursor.execute('''
            INSERT INTO invoices (invoice_number, client_id, date, total_amount)
            VALUES (?, ?, ?, ?)
        ''', (invoice_number, client_id, date, total))
        
        invoice_id = cursor.lastrowid
        
        # Insert items
        for item in items:
            item_total = item['qty'] * item['unit_price']
            cursor.execute('''
                INSERT INTO invoice_items 
                (invoice_id, description, quantity, unit_price, total)
                VALUES (?, ?, ?, ?, ?)
            ''', (invoice_id, item['description'], item['qty'], 
                 item['unit_price'], item_total))
        
        conn.commit()
        conn.close()
        
        return invoice_number
    
    @staticmethod
    def get_all_invoices() -> List[Invoice]:
        """Get all invoices with client names"""
        conn = get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT i.id, i.invoice_number, i.client_id, c.name, i.date, 
                   i.total_amount, i.status
            FROM invoices i
            LEFT JOIN clients c ON i.client_id = c.id
            ORDER BY i.date DESC
        ''')
        
        rows = cursor.fetchall()
        conn.close()
        
        return [
            Invoice(
                id=row[0],
                invoice_number=row[1],
                client_id=row[2],
                client_name=row[3] or "Unknown",
                date=row[4],
                total_amount=row[5],
                status=row[6]
            )
            for row in rows
        ]
    
    @staticmethod
    def get_invoice_items(invoice_id: int) -> List[InvoiceItem]:
        """Get items for an invoice"""
        conn = get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT id, invoice_id, description, quantity, unit_price
            FROM invoice_items
            WHERE invoice_id = ?
        ''', (invoice_id,))
        
        rows = cursor.fetchall()
        conn.close()
        
        return [
            InvoiceItem(
                id=row[0],
                invoice_id=row[1],
                description=row[2],
                quantity=row[3],
                unit_price=row[4]
            )
            for row in rows
        ]
    
    @staticmethod
    def update_invoice_status(invoice_id: int, status: str) -> bool:
        """Update invoice status"""
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            'UPDATE invoices SET status = ? WHERE id = ?',
            (status, invoice_id)
        )
        conn.commit()
        conn.close()
        return True
    
    @staticmethod
    def delete_invoice(invoice_id: int) -> bool:
        """Delete an invoice and its items"""
        conn = get_connection()
        cursor = conn.cursor()
        
        cursor.execute('DELETE FROM invoice_items WHERE invoice_id = ?', (invoice_id,))
        cursor.execute('DELETE FROM invoices WHERE id = ?', (invoice_id,))
        
        conn.commit()
        conn.close()
        return True
