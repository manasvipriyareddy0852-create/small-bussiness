"""
Inventory Management module for BizTrack AI
Handles CRUD operations for products
"""

import pandas as pd
from datetime import datetime
from database import get_connection, log_activity

def add_product(name, category, supplier, cost_price, selling_price, quantity, reorder_level, user_id=None):
    """Add a new product to inventory"""
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute('''
            INSERT INTO products (name, category, supplier, cost_price, selling_price, quantity, reorder_level)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (name, category, supplier, cost_price, selling_price, quantity, reorder_level))
        conn.commit()
        product_id = cursor.lastrowid
        conn.close()
        if user_id:
            log_activity(user_id, "Add Product", f"Added {name} (${selling_price})")
        return True, product_id
    except Exception as e:
        conn.close()
        return False, str(e)

def update_product(product_id, name, category, supplier, cost_price, selling_price, quantity, reorder_level, user_id=None):
    """Update an existing product"""
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute('''
            UPDATE products
            SET name=?, category=?, supplier=?, cost_price=?, selling_price=?, quantity=?, reorder_level=?
            WHERE product_id=?
        ''', (name, category, supplier, cost_price, selling_price, quantity, reorder_level, product_id))
        conn.commit()
        conn.close()
        if user_id:
            log_activity(user_id, "Update Product", f"Updated {name}")
        return True, "Product updated successfully!"
    except Exception as e:
        conn.close()
        return False, str(e)

def delete_product(product_id, user_id=None):
    """Delete a product"""
    conn = get_connection()
    cursor = conn.cursor()

    # Get product name before deletion
    cursor.execute('SELECT name FROM products WHERE product_id = ?', (product_id,))
    result = cursor.fetchone()
    product_name = result[0] if result else "Unknown"

    cursor.execute('DELETE FROM products WHERE product_id = ?', (product_id,))
    conn.commit()
    conn.close()

    if user_id:
        log_activity(user_id, "Delete Product", f"Deleted {product_name}")
    return True, "Product deleted successfully!"

def get_all_products():
    """Get all products as a DataFrame"""
    conn = get_connection()
    df = pd.read_sql_query('''
        SELECT product_id as "ID", name as "Name", category as "Category",
               supplier as "Supplier", cost_price as "Cost Price",
               selling_price as "Selling Price", quantity as "Quantity",
               reorder_level as "Reorder Level", date_added as "Date Added"
        FROM products ORDER BY product_id DESC
    ''', conn)
    conn.close()
    return df

def get_product_by_id(product_id):
    """Get a single product by ID"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM products WHERE product_id = ?', (product_id,))
    product = cursor.fetchone()
    conn.close()
    return product

def get_low_stock_products():
    """Get products below reorder level"""
    conn = get_connection()
    df = pd.read_sql_query('''
        SELECT product_id as "ID", name as "Product", category as "Category",
               quantity as "Stock", reorder_level as "Reorder Level"
        FROM products
        WHERE quantity < reorder_level
        ORDER BY quantity ASC
    ''', conn)
    conn.close()
    return df

def search_products(search_term="", category="All"):
    """Search products by name and filter by category"""
    conn = get_connection()
    query = '''
        SELECT product_id as "ID", name as "Name", category as "Category",
               supplier as "Supplier", cost_price as "Cost Price",
               selling_price as "Selling Price", quantity as "Quantity",
               reorder_level as "Reorder Level", date_added as "Date Added"
        FROM products WHERE 1=1
    '''
    params = []

    if search_term:
        query += " AND name LIKE ?"
        params.append(f"%{search_term}%")

    if category != "All":
        query += " AND category = ?"
        params.append(category)

    query += " ORDER BY product_id DESC"

    df = pd.read_sql_query(query, conn, params=params)
    conn.close()
    return df

def get_categories():
    """Get all unique categories"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT DISTINCT category FROM products ORDER BY category')
    categories = [row[0] for row in cursor.fetchall()]
    conn.close()
    return categories

def get_inventory_stats():
    """Get inventory statistics"""
    conn = get_connection()
    cursor = conn.cursor()

    # Total products
    cursor.execute('SELECT COUNT(*) FROM products')
    total_products = cursor.fetchone()[0]

    # Total inventory value (cost)
    cursor.execute('SELECT SUM(cost_price * quantity) FROM products')
    inventory_value = cursor.fetchone()[0] or 0

    # Total inventory (selling value)
    cursor.execute('SELECT SUM(selling_price * quantity) FROM products')
    retail_value = cursor.fetchone()[0] or 0

    # Low stock count
    cursor.execute('SELECT COUNT(*) FROM products WHERE quantity < reorder_level')
    low_stock_count = cursor.fetchone()[0]

    # Total quantity
    cursor.execute('SELECT SUM(quantity) FROM products')
    total_quantity = cursor.fetchone()[0] or 0

    conn.close()
    return {
        'total_products': total_products,
        'inventory_value': inventory_value,
        'retail_value': retail_value,
        'low_stock_count': low_stock_count,
        'total_quantity': total_quantity
    }

def get_inventory_distribution():
    """Get inventory distribution by category"""
    conn = get_connection()
    df = pd.read_sql_query('''
        SELECT category, SUM(quantity) as quantity, COUNT(*) as products
        FROM products
        GROUP BY category
        ORDER BY quantity DESC
    ''', conn)
    conn.close()
    return df
