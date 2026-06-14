"""
Reports module for BizTrack AI
Handles generation and export of various reports
"""

import pandas as pd
import io
from datetime import datetime
from database import get_connection
import inventory
import sales
import expenses

def get_inventory_report():
    """Generate inventory report"""
    df = inventory.get_all_products()
    return df

def get_sales_report(start_date=None, end_date=None):
    """Generate sales report"""
    if start_date and end_date:
        df = sales.get_sales_by_date_range(start_date, end_date)
    else:
        df = sales.get_all_sales()
    return df

def get_expense_report(start_date=None, end_date=None, category=None):
    """Generate expense report"""
    if start_date and end_date:
        df = expenses.get_expenses_by_date_range(start_date, end_date)
    elif category and category != "All":
        df = expenses.get_expenses_by_category(category)
    else:
        df = expenses.get_all_expenses()
    return df

def get_profit_report():
    """Generate profit & loss report"""
    conn = get_connection()
    cursor = conn.cursor()

    # Get total revenue
    cursor.execute('SELECT COALESCE(SUM(total_amount), 0) FROM sales')
    total_revenue = cursor.fetchone()[0]

    # Get total expenses
    cursor.execute('SELECT COALESCE(SUM(amount), 0) FROM expenses')
    total_expenses = cursor.fetchone()[0]

    # Get cost of goods sold
    cursor.execute('''
        SELECT COALESCE(SUM(s.quantity_sold * p.cost_price), 0)
        FROM sales s
        JOIN products p ON s.product_id = p.product_id
    ''')
    cost_of_goods = cursor.fetchone()[0]

    conn.close()

    gross_profit = total_revenue - cost_of_goods
    net_profit = gross_profit - total_expenses

    return {
        'total_revenue': total_revenue,
        'cost_of_goods': cost_of_goods,
        'gross_profit': gross_profit,
        'total_expenses': total_expenses,
        'net_profit': net_profit
    }

def get_monthly_profit_report():
    """Get monthly profit breakdown"""
    conn = get_connection()
    df = pd.read_sql_query('''
        WITH monthly_sales AS (
            SELECT strftime('%Y-%m', sale_date) as month,
                   SUM(total_amount) as revenue
            FROM sales
            GROUP BY strftime('%Y-%m', sale_date)
        ),
        monthly_expenses AS (
            SELECT strftime('%Y-%m', expense_date) as month,
                   SUM(amount) as expenses
            FROM expenses
            GROUP BY strftime('%Y-%m', expense_date)
        )
        SELECT COALESCE(s.month, e.month) as "Month",
               COALESCE(s.revenue, 0) as "Revenue",
               COALESCE(e.expenses, 0) as "Expenses",
               COALESCE(s.revenue, 0) - COALESCE(e.expenses, 0) as "Profit"
        FROM monthly_sales s
        FULL OUTER JOIN monthly_expenses e ON s.month = e.month
        ORDER BY month DESC
        LIMIT 12
    ''', conn)
    conn.close()
    return df

def export_to_csv(df):
    """Convert DataFrame to CSV for download"""
    return df.to_csv(index=False).encode('utf-8')

def export_to_excel(df, sheet_name='Report'):
    """Convert DataFrame to Excel for download"""
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, sheet_name=sheet_name, index=False)
    return output.getvalue()

def get_comprehensive_report():
    """Generate comprehensive business report"""
    # Get all data
    inventory_df = inventory.get_all_products()
    sales_df = sales.get_all_sales()
    expenses_df = expenses.get_all_expenses()
    profit_data = get_profit_report()

    # Create Excel with multiple sheets
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        # Summary sheet
        summary_data = {
            'Metric': ['Total Revenue', 'Total Expenses', 'Net Profit',
                       'Total Products', 'Inventory Value', 'Low Stock Count'],
            'Value': [f"${profit_data['total_revenue']:,.2f}",
                      f"${profit_data['total_expenses']:,.2f}",
                      f"${profit_data['net_profit']:,.2f}",
                      len(inventory_df),
                      f"${inventory.get_inventory_stats()['inventory_value']:,.2f}",
                      len(inventory.get_low_stock_products())]
        }
        summary_df = pd.DataFrame(summary_data)
        summary_df.to_excel(writer, sheet_name='Summary', index=False)

        # Other sheets
        inventory_df.to_excel(writer, sheet_name='Inventory', index=False)
        sales_df.to_excel(writer, sheet_name='Sales', index=False)
        expenses_df.to_excel(writer, sheet_name='Expenses', index=False)

    return output.getvalue()
