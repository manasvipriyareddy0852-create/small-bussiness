"""
Expense Tracking module for BizTrack AI
Handles expense management and tracking
"""

import pandas as pd
from datetime import datetime
from database import get_connection, log_activity

EXPENSE_CATEGORIES = [
    'Rent',
    'Utilities',
    'Marketing',
    'Salaries',
    'Transportation',
    'Supplies',
    'Equipment',
    'Insurance',
    'Taxes',
    'Miscellaneous'
]

def add_expense(category, description, amount, user_id=None):
    """Add a new expense"""
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute('''
            INSERT INTO expenses (category, description, amount, expense_date)
            VALUES (?, ?, ?, ?)
        ''', (category, description, amount, datetime.now()))
        conn.commit()
        conn.close()

        if user_id:
            log_activity(user_id, "Add Expense", f"Added ${amount:.2f} for {category}")
        return True, "Expense added successfully!"
    except Exception as e:
        conn.close()
        return False, str(e)

def get_all_expenses():
    """Get all expenses as DataFrame"""
    conn = get_connection()
    df = pd.read_sql_query('''
        SELECT expense_id as "ID", category as "Category",
               description as "Description", amount as "Amount",
               expense_date as "Date"
        FROM expenses ORDER BY expense_date DESC
    ''', conn)
    conn.close()
    return df

def get_expenses_by_date_range(start_date, end_date):
    """Get expenses filtered by date range"""
    conn = get_connection()
    df = pd.read_sql_query('''
        SELECT expense_id as "ID", category as "Category",
               description as "Description", amount as "Amount",
               expense_date as "Date"
        FROM expenses
        WHERE DATE(expense_date) BETWEEN DATE(?) AND DATE(?)
        ORDER BY expense_date DESC
    ''', conn, params=(start_date, end_date))
    conn.close()
    return df

def get_expenses_by_category(category):
    """Get expenses filtered by category"""
    conn = get_connection()
    df = pd.read_sql_query('''
        SELECT expense_id as "ID", category as "Category",
               description as "Description", amount as "Amount",
               expense_date as "Date"
        FROM expenses
        WHERE category = ?
        ORDER BY expense_date DESC
    ''', conn, params=(category,))
    conn.close()
    return df

def delete_expense(expense_id, user_id=None):
    """Delete an expense"""
    conn = get_connection()
    cursor = conn.cursor()

    # Get expense info before deletion
    cursor.execute('SELECT category, amount FROM expenses WHERE expense_id = ?',
                   (expense_id,))
    expense = cursor.fetchone()

    if user_id:
        log_activity(user_id, "Delete Expense", f"Deleted expense")

    cursor.execute('DELETE FROM expenses WHERE expense_id = ?', (expense_id,))
    conn.commit()
    conn.close()
    return True, "Expense deleted successfully!"

def get_expense_stats():
    """Get expense statistics"""
    conn = get_connection()
    cursor = conn.cursor()

    today = datetime.now().date()
    month_start = today.replace(day=1)

    # Total expenses
    cursor.execute('SELECT COALESCE(SUM(amount), 0) FROM expenses')
    total_expenses = cursor.fetchone()[0]

    # This month's expenses
    cursor.execute('''
        SELECT COALESCE(SUM(amount), 0) FROM expenses
        WHERE DATE(expense_date) >= DATE(?)
    ''', (month_start,))
    monthly_expenses = cursor.fetchone()[0]

    # Today's expenses
    cursor.execute('''
        SELECT COALESCE(SUM(amount), 0) FROM expenses
        WHERE DATE(expense_date) = DATE(?)
    ''', (today,))
    today_expenses = cursor.fetchone()[0]

    conn.close()
    return {
        'total_expenses': total_expenses,
        'monthly_expenses': monthly_expenses,
        'today_expenses': today_expenses
    }

def get_expenses_by_category_summary():
    """Get expenses grouped by category"""
    conn = get_connection()
    df = pd.read_sql_query('''
        SELECT category as "Category",
               COUNT(*) as "Transactions",
               SUM(amount) as "Total Amount",
               AVG(amount) as "Average"
        FROM expenses
        GROUP BY category
        ORDER BY SUM(amount) DESC
    ''', conn)
    conn.close()
    return df

def get_monthly_expenses_trend():
    """Get monthly expenses data for charts"""
    conn = get_connection()
    df = pd.read_sql_query('''
        SELECT strftime('%Y-%m', expense_date) as month,
               SUM(amount) as expenses,
               COUNT(*) as transactions
        FROM expenses
        GROUP BY strftime('%Y-%m', expense_date)
        ORDER BY month DESC
        LIMIT 12
    ''', conn)
    conn.close()
    return df

def get_expense_categories():
    """Get all expense categories"""
    return EXPENSE_CATEGORIES
