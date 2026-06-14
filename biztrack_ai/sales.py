"""
Sales Management module for BizTrack AI
Handles sales recording and revenue tracking
"""

import pandas as pd
from datetime import datetime, timedelta
from database import get_connection, log_activity

def record_sale(product_id, product_name, quantity_sold, unit_price, user_id=None):
    """Record a new sale and update inventory"""
    conn = get_connection()
    cursor = conn.cursor()

    # Check inventory
    cursor.execute('SELECT quantity FROM products WHERE product_id = ?', (product_id,))
    result = cursor.fetchone()

    if not result:
        conn.close()
        return False, "Product not found!"

    current_stock = result[0]
    if current_stock < quantity_sold:
        conn.close()
        return False, f"Insufficient inventory! Only {current_stock} units available."

    try:
        total_amount = quantity_sold * unit_price

        # Record the sale
        cursor.execute('''
            INSERT INTO sales (product_id, product_name, quantity_sold, unit_price, total_amount, sale_date)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (product_id, product_name, quantity_sold, unit_price, total_amount, datetime.now()))

        # Update inventory
        new_quantity = current_stock - quantity_sold
        cursor.execute('UPDATE products SET quantity = ? WHERE product_id = ?',
                       (new_quantity, product_id))

        conn.commit()
        conn.close()

        if user_id:
            log_activity(user_id, "Record Sale", f"Sold {quantity_sold}x {product_name} (${total_amount:.2f})")
        return True, f"Sale recorded! Total: ${total_amount:.2f}"
    except Exception as e:
        conn.close()
        return False, str(e)

def get_all_sales():
    """Get all sales as DataFrame"""
    conn = get_connection()
    df = pd.read_sql_query('''
        SELECT sale_id as "Sale ID", product_name as "Product",
               quantity_sold as "Quantity", unit_price as "Unit Price",
               total_amount as "Total", sale_date as "Date"
        FROM sales ORDER BY sale_date DESC
    ''', conn)
    conn.close()
    return df

def get_sales_by_date_range(start_date, end_date):
    """Get sales filtered by date range"""
    conn = get_connection()
    df = pd.read_sql_query('''
        SELECT sale_id as "Sale ID", product_name as "Product",
               quantity_sold as "Quantity", unit_price as "Unit Price",
               total_amount as "Total", sale_date as "Date"
        FROM sales
        WHERE DATE(sale_date) BETWEEN DATE(?) AND DATE(?)
        ORDER BY sale_date DESC
    ''', conn, params=(start_date, end_date))
    conn.close()
    return df

def get_sales_stats():
    """Get sales statistics"""
    conn = get_connection()
    cursor = conn.cursor()

    today = datetime.now().date()
    month_start = today.replace(day=1)

    # Today's sales
    cursor.execute('''
        SELECT COALESCE(SUM(total_amount), 0) FROM sales
        WHERE DATE(sale_date) = DATE(?)
    ''', (today,))
    today_sales = cursor.fetchone()[0]

    # Monthly revenue
    cursor.execute('''
        SELECT COALESCE(SUM(total_amount), 0) FROM sales
        WHERE DATE(sale_date) >= DATE(?)
    ''', (month_start,))
    monthly_revenue = cursor.fetchone()[0]

    # Total sales count
    cursor.execute('SELECT COUNT(*) FROM sales')
    total_sales = cursor.fetchone()[0]

    # Total revenue
    cursor.execute('SELECT COALESCE(SUM(total_amount), 0) FROM sales')
    total_revenue = cursor.fetchone()[0]

    conn.close()
    return {
        'today_sales': today_sales,
        'monthly_revenue': monthly_revenue,
        'total_sales': total_sales,
        'total_revenue': total_revenue
    }

def get_monthly_sales_trend():
    """Get monthly sales data for charts"""
    conn = get_connection()
    df = pd.read_sql_query('''
        SELECT strftime('%Y-%m', sale_date) as month,
               SUM(total_amount) as revenue,
               COUNT(*) as transactions,
               SUM(quantity_sold) as units_sold
        FROM sales
        GROUP BY strftime('%Y-%m', sale_date)
        ORDER BY month DESC
        LIMIT 12
    ''', conn)
    conn.close()
    return df

def get_top_selling_products(limit=10):
    """Get top selling products"""
    conn = get_connection()
    df = pd.read_sql_query('''
        SELECT product_name as "Product",
               SUM(quantity_sold) as "Units Sold",
               SUM(total_amount) as "Revenue"
        FROM sales
        GROUP BY product_name
        ORDER BY revenue DESC
        LIMIT ?
    ''', conn, params=(limit,))
    conn.close()
    return df

def get_product_sales_history(product_id, days=30):
    """Get sales history for a specific product"""
    conn = get_connection()
    df = pd.read_sql_query('''
        SELECT sale_date, quantity_sold, total_amount
        FROM sales
        WHERE product_id = ?
        AND DATE(sale_date) >= DATE('now', '-' || ? || ' days')
        ORDER BY sale_date DESC
    ''', conn, params=(product_id, days))
    conn.close()
    return df

def delete_sale(sale_id, user_id=None):
    """Delete a sale record (admin only)"""
    conn = get_connection()
    cursor = conn.cursor()

    # Get sale info
    cursor.execute('SELECT product_id, quantity_sold, product_name FROM sales WHERE sale_id = ?',
                   (sale_id,))
    sale = cursor.fetchone()

    if sale:
        product_id, quantity, product_name = sale
        # Restore inventory
        cursor.execute('''
            UPDATE products SET quantity = quantity + ?
            WHERE product_id = ?
        ''', (quantity, product_id))

        cursor.execute('DELETE FROM sales WHERE sale_id = ?', (sale_id,))
        conn.commit()

        if user_id:
            log_activity(user_id, "Delete Sale", f"Deleted sale of {product_name}")

    conn.close()
    return True, "Sale deleted and inventory restored!"

def get_recent_transactions(limit=10):
    """Get recent transactions for dashboard feed"""
    conn = get_connection()
    df = pd.read_sql_query('''
        SELECT sale_date as "Time", product_name as "Product",
               quantity_sold as "Qty", total_amount as "Amount"
        FROM sales
        ORDER BY sale_date DESC
        LIMIT ?
    ''', conn, params=(limit,))
    conn.close()
    return df
