# Poultry Farm Management System

A modern Python GUI application for managing poultry farm operations, replacing the existing Excel spreadsheet.

## Features

### 📊 Dashboard
- Overview of current flock status
- Key Performance Indicators (KPIs)
- Quick stats: total chickens, mortality rate, production

### 📝 Daily Data Entry
- **Stock Entry**: Daily chicken inventory
- **Mortality Tracking**: Record daily deaths
- **Production Tracking**: Daily egg production

### 💰 Expense Management
- Feed (Aliments)
- Electricity (STEG)
- Egg cartons (Alvéoles)
- Workers (Ouvriers)
- Miscellaneous (Divers)
- Vehicle expenses (Gas, Maintenance)
- Utilities (Water)

### 🧾 Billing & Invoicing
- Generate PDF invoices for egg sales
- Client management
- Invoice history
- Print/export functionality

### 📈 Reports
- Weekly production reports
- Monthly summaries
- Profit/Loss calculations
- Expense breakdowns

## Tech Stack

- **Python 3**
- **ttkbootstrap** - Modern UI design
- **reportlab** - PDF invoice generation
- **sqlite3** - Local database storage

## Installation

```bash
pip install ttkbootstrap reportlab
```

## Usage

```bash
python app.py
```

## Data Structure

### Columns (from original Excel)
| French | English |
|--------|---------|
| Stock | Chicken inventory |
| Sortie | Sales/Output |
| Mortalité | Mortality |
| Effectif restant | Remaining count |
| Production | Production |
| Frais | Expenses |
| Recette | Revenue |

## Project Status

- [x] Excel file analyzed
- [x] Project structure created
- [ ] Daily entry forms
- [ ] Expense tracking
- [ ] Billing/invoicing
- [ ] Reports
- [ ] Database integration

---

*Developed on `dev/alablah` branch - awaiting merge to main*
