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
APP_TITLE = "Poultry Farm Management"
APP_THEME = "litera"  # More professional, clean theme
APP_SIZE = "1280x800"
APP_MIN_SIZE = (1100, 700)

# Date format
DATE_FORMAT = "%Y-%m-%d"
DISPLAY_DATE_FORMAT = "%d/%m/%Y"

# Invoice settings
INVOICE_PREFIX = "INV-"
INVOICE_STATUS = ["unpaid", "paid", "cancelled"]

# Dashboard KPIs
DEFAULT_STOCK = 0
