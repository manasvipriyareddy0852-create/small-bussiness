# BizTrack AI

Smart Inventory & Bookkeeping for Small Businesses

## Installation

```bash
pip install -r requirements.txt
```

## Run the Application

```bash
streamlit run app.py
```

## Demo Accounts

After generating sample data in Settings:
- **Owner**: owner@biztrack.ai / demo123
- **Staff**: staff@biztrack.ai / demo123

## Features

- Dashboard with KPIs and charts
- Inventory management with CRUD operations
- Sales tracking with automatic inventory updates
- Expense tracking with categories
- Report generation (CSV/Excel)
- Demand forecasting and restock recommendations
- AI-powered business insights
- Dark mode support
- User authentication with roles (Owner/Staff)

## Project Structure

```
biztrack_ai/
  app.py              # Main Streamlit application
  database.py         # SQLite database setup
  auth.py             # Authentication module
  inventory.py        # Inventory management
  sales.py            # Sales management
  expenses.py         # Expense tracking
  reports.py          # Report generation
  forecasting.py      # Demand forecasting
  insights.py         # AI business insights
  sample_data.py      # Demo data generator
  utils.py            # Utilities and theming
  data/               # SQLite database storage
```
