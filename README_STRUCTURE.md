# Poultry Farm Management System - Module Structure

## 📁 Project Structure

```
poultry_farm/
├── app.py                 # Main entry point
├── models/
│   ├── __init__.py      # Models package
│   ├── database.py        # SQLite database setup & connection
│   └── models.py         # Data classes (DailyEntry, Expense, Client, Invoice)
├── views/
│   ├── __init__.py      # Views package
│   ├── dashboard.py      # Dashboard with KPIs
│   ├── daily_entry.py   # Daily stock/mortality/production form
│   ├── expenses.py      # Expense tracking form
│   ├── billing.py       # Client & invoice management
│   └── reports.py       # Report generation views
├── controllers/
│   ├── __init__.py      # Controllers package
│   ├── daily_controller.py    # Daily entry business logic
│   ├── expense_controller.py  # Expense business logic
│   ├── billing_controller.py  # Invoice business logic
│   └── report_controller.py  # Report generation logic
└── utils/
    ├── __init__.py      # Utils package
    ├── constants.py      # Expense categories, settings
    └── pdf_generator.py # PDF invoice generation
```

## 📖 What Each File Does

### 🔧 models/ - Data Layer
| File | Description |
|------|-------------|
| `database.py` | SQLite connection, table creation, CRUD operations |
| `models.py` | Python classes: DailyEntry, Expense, Client, Invoice, InvoiceItem |

### 🎨 views/ - UI Layer
| File | Description |
|------|-------------|
| `dashboard.py` | Main dashboard with KPI cards and recent activity table |
| `daily_entry.py` | Form for daily stock/mortality/production input |
| `expenses.py` | Form for recording expenses by category |
| `billing.py` | Client management + invoice creation UI |
| `reports.py` | Report generation buttons and output display |

### 🧠 controllers/ - Business Logic
| File | Description |
|------|-------------|
| `daily_controller.py` | Save/retrieve daily entries, calculations |
| `expense_controller.py` | Save/retrieve expenses, category totals |
| `billing_controller.py` | Client CRUD, invoice creation, item management |
| `report_controller.py` | Generate weekly/monthly/expense reports |

### 🛠 utils/ - Helpers
| File | Description |
|------|-------------|
| `constants.py` | Expense categories list, app settings |
| `pdf_generator.py` | Generate PDF invoices using ReportLab |

### 🚀 app.py - Entry Point
- Creates main window
- Sets up ttkbootstrap theme
- Builds tabbed interface
- Coordinates all modules

## 🔄 Data Flow

```
User Input → views/ (UI) 
         → controllers/ (Logic) 
         → models/ (Database) 
         → utils/ (PDF export)
```
