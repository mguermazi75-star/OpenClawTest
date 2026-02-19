"""
Constants and settings for the poultry farm system
"""

# Expense categories matching Excel file
EXPENSE_CATEGORIES = [
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
]

# App settings
APP_TITLE = "🐔 Poultry Farm Management"
APP_THEME = "cosmo"
APP_SIZE = "1200x700"
APP_MIN_SIZE = (1000, 600)

# Date format
DATE_FORMAT = "%Y-%m-%d"
DISPLAY_DATE_FORMAT = "%d/%m/%Y"

# Invoice settings
INVOICE_PREFIX = "INV-"
INVOICE_STATUS = ["unpaid", "paid", "cancelled"]

# Dashboard KPIs
DEFAULT_STOCK = 0
