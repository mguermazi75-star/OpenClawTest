"""
Data models for the poultry farm system
"""

from dataclasses import dataclass
from typing import Optional, List
from datetime import datetime


@dataclass
class DailyEntry:
    """Daily farm data entry"""
    id: Optional[int] = None
    date: str = ""
    mortality: int = 0  # Chicken deaths
    production: int = 0  # Eggs produced
    eggs_sold: int = 0  # Eggs sold
    egg_price: float = 0.0  # Price per egg in EUR
    notes: str = ""
    
    @property
    def remaining_eggs(self) -> int:
        """Calculate remaining (unsold) eggs"""
        return self.production - self.eggs_sold


@dataclass
class Expense:
    """Expense record"""
    id: Optional[int] = None
    date: str = ""
    category: str = ""
    amount: float = 0.0
    description: str = ""


@dataclass
class Client:
    """Client/customer for billing"""
    id: Optional[int] = None
    name: str = ""
    phone: str = ""
    address: str = ""


@dataclass
class Invoice:
    """Invoice header"""
    id: Optional[int] = None
    invoice_number: str = ""
    client_id: int = 0
    client_name: str = ""
    date: str = ""
    total_amount: float = 0.0
    status: str = "unpaid"


@dataclass
class InvoiceItem:
    """Individual item on an invoice"""
    id: Optional[int] = None
    invoice_id: int = 0
    description: str = ""
    quantity: int = 0
    unit_price: float = 0.0
    
    @property
    def total(self) -> float:
        """Calculate line total"""
        return self.quantity * self.unit_price


# Type aliases for lists
ExpenseList = List[Expense]
ClientList = List[Client]
InvoiceList = List[Invoice]
InvoiceItemList = List[InvoiceItem]
