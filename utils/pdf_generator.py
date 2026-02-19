"""
PDF Invoice Generator using ReportLab
"""

from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from typing import List, Dict
import os


class PDFGenerator:
    """Generate PDF invoices"""
    
    def __init__(self, filename: str):
        self.filename = filename
        self.c = canvas.Canvas(filename, pagesize=A4)
        self.width, self.height = A4
        self.y_position = 0
    
    def set_position(self, y: float):
        """Set current Y position"""
        self.y_position = y
    
    def draw_header(self, company_name: str = "Poultry Farm"):
        """Draw invoice header"""
        self.c.setFont("Helvetica-Bold", 24)
        self.c.drawString(50, self.height - 50, "INVOICE")
        
        self.c.setFont("Helvetica", 10)
        self.c.drawString(50, self.height - 80, company_name)
        self.c.drawString(50, self.height - 95, f"Generated: {self._get_date()}")
    
    def draw_client(self, client_name: str, client_address: str = ""):
        """Draw client info"""
        self.y_position = self.height - 140
        self.c.setFont("Helvetica-Bold", 12)
        self.c.drawString(50, self.y_position, "Bill To:")
        
        self.y_position -= 20
        self.c.setFont("Helvetica", 11)
        self.c.drawString(50, self.y_position, client_name)
        
        if client_address:
            self.y_position -= 15
            self.c.setFont("Helvetica", 10)
            self.c.drawString(50, self.y_position, client_address)
    
    def draw_items_header(self):
        """Draw table header"""
        self.y_position -= 30
        self.c.setFont("Helvetica-Bold", 10)
        self.c.drawString(50, self.y_position, "Description")
        self.c.drawString(300, self.y_position, "Qty")
        self.c.drawString(360, self.y_position, "Unit Price")
        self.c.drawString(450, self.y_position, "Total")
        
        # Draw line
        self.y_position -= 5
        self.c.line(50, self.y_position, 520, self.y_position)
        self.y_position -= 15
    
    def draw_item(self, description: str, quantity: int, unit_price: float, total: float):
        """Draw a single line item"""
        self.c.setFont("Helvetica", 10)
        self.c.drawString(50, self.y_position, description[:30])
        self.c.drawString(300, self.y_position, str(quantity))
        self.c.drawString(360, self.y_position, f"€{unit_price:.2f}")
        self.c.drawString(450, self.y_position, f"€{total:.2f}")
        self.y_position -= 20
    
    def draw_total(self, total: float):
        """Draw total amount"""
        self.y_position -= 30
        self.c.setFont("Helvetica-Bold", 12)
        self.c.drawString(350, self.y_position, "TOTAL:")
        self.c.drawString(450, self.y_position, f"€{total:.2f}")
    
    def draw_footer(self):
        """Draw footer"""
        self.c.setFont("Helvetica", 8)
        self.c.drawString(50, 30, "Thank you for your business!")
    
    def save(self):
        """Save PDF file"""
        self.c.save()
    
    @staticmethod
    def _get_date() -> str:
        from datetime import datetime
        return datetime.now().strftime("%Y-%m-%d")
    
    @staticmethod
    def generate_simple_invoice(
        client_name: str,
        items: List[Dict],
        output_filename: str = "invoice.pdf"
    ) -> str:
        """
        Helper to generate a simple invoice quickly.
        
        Args:
            client_name: Name of the client
            items: List of dicts with keys: description, qty, unit_price
            output_filename: Output PDF filename
            
        Returns:
            Path to generated PDF
        """
        pdf = PDFGenerator(output_filename)
        
        # Header
        pdf.draw_header()
        
        # Client
        pdf.draw_client(client_name)
        
        # Items header
        pdf.draw_items_header()
        
        # Calculate total
        grand_total = 0
        
        # Items
        for item in items:
            total = item['qty'] * item['unit_price']
            grand_total += total
            pdf.draw_item(
                item['description'],
                item['qty'],
                item['unit_price'],
                total
            )
        
        # Total
        pdf.draw_total(grand_total)
        
        # Footer
        pdf.draw_footer()
        
        # Save
        pdf.save()
        
        return output_filename
