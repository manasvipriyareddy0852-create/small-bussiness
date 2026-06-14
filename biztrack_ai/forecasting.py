"""
Forecasting module for BizTrack AI
Provides basic demand forecasting and restock recommendations
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from database import get_connection
import inventory

def get_product_demand_history(product_id, days=60):
    """Get daily sales history for a product"""
    conn = get_connection()
    df = pd.read_sql_query('''
        SELECT DATE(sale_date) as date, SUM(quantity_sold) as quantity
        FROM sales
        WHERE product_id = ?
        AND DATE(sale_date) >= DATE('now', '-' || ? || ' days')
        GROUP BY DATE(sale_date)
        ORDER BY date
    ''', conn, params=(product_id, days))
    conn.close()
    return df

def forecast_demand(product_id, forecast_days=7):
    """
    Simple moving average forecast for product demand
    Returns predicted daily demand
    """
    history = get_product_demand_history(product_id, days=30)

    if len(history) < 7:
        # Not enough data, use simple average
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT COALESCE(AVG(quantity_sold), 0)
            FROM (
                SELECT SUM(quantity_sold) as quantity_sold
                FROM sales
                WHERE product_id = ?
                GROUP BY DATE(sale_date)
            )
        ''', (product_id,))
        avg_daily = cursor.fetchone()[0]
        conn.close()
        return avg_daily * forecast_days

    # Calculate moving average
    recent_avg = history['quantity'].tail(7).mean()
    return recent_avg * forecast_days

def get_restock_recommendations():
    """Get restock recommendations for all products"""
    conn = get_connection()
    df = pd.read_sql_query('''
        SELECT product_id, name, category, quantity, reorder_level,
               selling_price, cost_price
        FROM products
    ''', conn)
    conn.close()

    recommendations = []
    for _, row in df.iterrows():
        product_id = row['product_id']
        current_stock = row['quantity']
        reorder_level = row['reorder_level']

        # Calculate forecast
        predicted_demand = forecast_demand(product_id, forecast_days=14)

        # Determine if restocking needed
        days_of_stock = current_stock / (predicted_demand / 14) if predicted_demand > 0 else 999

        restock_needed = current_stock < reorder_level or days_of_stock < 7
        recommended_order = max(0, int(predicted_demand * 2 - current_stock))

        recommendations.append({
            'product_id': product_id,
            'name': row['name'],
            'category': row['category'],
            'current_stock': current_stock,
            'reorder_level': reorder_level,
            'predicted_demand_14d': round(predicted_demand, 1),
            'days_of_stock': round(days_of_stock, 1) if days_of_stock < 999 else 'High',
            'restock_needed': restock_needed,
            'recommended_order': recommended_order if restock_needed else 0,
            'unit_cost': row['cost_price'],
            'order_cost': recommended_order * row['cost_price'] if restock_needed else 0
        })

    return pd.DataFrame(recommendations)

def get_demand_forecast_chart_data():
    """Get forecast data for all products for visualization"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT product_id, name
        FROM products
        ORDER BY product_id
    ''')
    products = cursor.fetchall()
    conn.close()

    chart_data = []
    for product_id, name in products[:10]:  # Top 10 products
        demand = forecast_demand(product_id, forecast_days=7)
        daily_demand = demand / 7
        chart_data.append({
            'product': name,
            'predicted_daily': round(daily_demand, 1),
            'predicted_weekly': round(demand, 1)
        })

    return pd.DataFrame(chart_data)

def get_sales_velocity():
    """Calculate sales velocity for each product"""
    conn = get_connection()
    df = pd.read_sql_query('''
        SELECT p.product_id, p.name, p.category,
               p.quantity as current_stock,
               COALESCE(SUM(s.quantity_sold), 0) as total_sold,
               COUNT(DISTINCT DATE(s.sale_date)) as days_with_sales
        FROM products p
        LEFT JOIN sales s ON p.product_id = s.product_id
        WHERE s.sale_date IS NULL OR DATE(s.sale_date) >= DATE('now', '-30 days')
        GROUP BY p.product_id
        ORDER BY total_sold DESC
    ''', conn)
    conn.close()

    # Calculate velocity (units per day)
    df['velocity'] = df.apply(
        lambda x: x['total_sold'] / x['days_with_sales'] if x['days_with_sales'] > 0 else 0,
        axis=1
    )
    df['days_until_empty'] = df.apply(
        lambda x: int(x['current_stock'] / x['velocity']) if x['velocity'] > 0 else 999,
        axis=1
    )

    return df

def get_seasonal_trends():
    """Analyze seasonal trends in sales"""
    conn = get_connection()
    df = pd.read_sql_query('''
        SELECT strftime('%w', sale_date) as day_of_week,
               AVG(total_amount) as avg_sale_amount,
               COUNT(*) as transaction_count
        FROM sales
        GROUP BY strftime('%w', sale_date)
        ORDER BY day_of_week
    ''', conn)
    conn.close()

    day_names = ['Sunday', 'Monday', 'Tuesday', 'Wednesday',
                 'Thursday', 'Friday', 'Saturday']
    df['day_name'] = df['day_of_week'].astype(int).map(lambda x: day_names[x])

    return df

def predict_stockout_risk():
    """Predict products at risk of stockout"""
    velocity_df = get_sales_velocity()

    at_risk = velocity_df[velocity_df['days_until_empty'] < 14].copy()
    at_risk = at_risk.sort_values('days_until_empty')

    return at_risk[['product_id', 'name', 'category', 'current_stock',
                    'velocity', 'days_until_empty']]

def get_category_growth():
    """Analyze growth by category"""
    conn = get_connection()
    df = pd.read_sql_query('''
        SELECT p.category,
               strftime('%Y-%m', s.sale_date) as month,
               SUM(s.total_amount) as revenue
        FROM sales s
        JOIN products p ON s.product_id = p.product_id
        GROUP BY p.category, strftime('%Y-%m', s.sale_date)
        ORDER BY month DESC, revenue DESC
    ''', conn)
    conn.close()

    return df
