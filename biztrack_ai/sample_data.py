"""
Sample Data Generator for BizTrack AI
Generates demo data for testing and demonstration
"""

import random
from datetime import datetime, timedelta
import database
import auth
import inventory
import sales
import expenses

# Sample data configurations
PRODUCT_NAMES = [
    "Wireless Mouse", "USB Keyboard", "Monitor Stand", "Laptop Sleeve", "Webcam HD",
    "Desk Lamp", "Mouse Pad XL", "USB Hub 7-Port", "Headphones Pro", "Speaker Set",
    "Cable Organizer", "Phone Stand", "Laptop Cooler", "Webcam Cover", "Cable Ties Pack",
    "Screen Cleaner", "Keyboard Cover", "Mouse Grip Tape", "Wrist Rest", "Desk Mat",
    "Monitor Light Bar", "Webcam Ring Light", "Phone Charger", "USB-C Cable", "HDMI Cable",
    "Ethernet Cable", "Power Strip", "Extension Cord", "Battery Pack", "Flash Drive 64GB",
    "SSD 500GB", "Memory Card 128GB", "Card Reader", "Wireless Charger", "Bluetooth Speaker",
    "Gaming Mouse", "Mechanical Keyboard", "Controller Stand", "Headphone Stand", "Router Stand",
    "Cable Sleeve", "Wire Clips", "Desk Grommet", "Tray Organizer", "Drawer Divider",
    "Label Maker", "Sticky Notes Pack", "Whiteboard Markers", "Clipboard Set", "Calculator"
]

SUPPLIERS = [
    "TechSupply Co.", "Global Imports", "Direct Distribution", "Wholesale Plus",
    "TechWarehouse", "Prime Suppliers", "Metro Wholesale", "BestSource Inc."
]

CATEGORIES = [
    "Electronics", "Computer Accessories", "Office Supplies", "Peripherals",
    "Storage", "Audio/Video", "Networking", "Organization"
]

EXPENSE_DESCRIPTIONS = {
    "Rent": ["Monthly office rent", "Warehouse rent", "Store rental"],
    "Utilities": ["Electric bill", "Water bill", "Internet service", "Phone service"],
    "Marketing": ["Facebook ads", "Google ads", "Print flyers", "Social media campaign"],
    "Salaries": ["Staff salaries", "Contractor payment", "Part-time wages"],
    "Transportation": ["Delivery fees", "Gas expenses", "Vehicle maintenance"],
    "Supplies": ["Office supplies", "Packaging materials", "Cleaning supplies"],
    "Equipment": ["New computer", "POS system", "Security cameras"],
    "Insurance": ["Liability insurance", "Property insurance", "Health insurance"],
    "Taxes": ["Sales tax payment", "Property tax", "Income tax"],
    "Miscellaneous": ["Unexpected expense", "Misc purchase", "Emergency repair"]
}

def generate_sample_data():
    """Generate all sample data"""
    # Check if data already exists
    conn = database.get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT COUNT(*) FROM products')
    if cursor.fetchone()[0] > 0:
        conn.close()
        return False, "Sample data already exists!"
    conn.close()

    # Create demo owner account
    auth.signup("Demo Owner", "owner@biztrack.ai", "demo123", "owner")

    # Create demo staff account
    auth.signup("Demo Staff", "staff@biztrack.ai", "demo123", "staff")

    # Generate 50 products
    for i, name in enumerate(PRODUCT_NAMES[:50]):
        category = random.choice(CATEGORIES)
        supplier = random.choice(SUPPLIERS)
        cost_price = round(random.uniform(5, 100), 2)
        selling_price = round(cost_price * random.uniform(1.3, 2.0), 2)
        quantity = random.randint(5, 100)
        reorder_level = random.randint(5, 20)

        inventory.add_product(name, category, supplier, cost_price, selling_price, quantity, reorder_level)

    # Generate 100 sales over the past 3 months
    conn = database.get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT product_id, name, selling_price FROM products')
    products = cursor.fetchall()
    conn.close()

    end_date = datetime.now()
    start_date = end_date - timedelta(days=90)

    for _ in range(100):
        product = random.choice(products)
        product_id, product_name, unit_price = product
        quantity_sold = random.randint(1, 5)

        # Generate random date within range
        random_days = random.randint(0, 90)
        sale_date = end_date - timedelta(days=random_days)

        # Add sale directly to database for historical dates
        conn = database.get_connection()
        cursor = conn.cursor()
        total_amount = quantity_sold * unit_price
        cursor.execute('''
            INSERT INTO sales (product_id, product_name, quantity_sold, unit_price, total_amount, sale_date)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (product_id, product_name, quantity_sold, unit_price, total_amount, sale_date))
        conn.commit()
        conn.close()

    # Generate 50 expenses over the past 3 months
    categories = list(EXPENSE_DESCRIPTIONS.keys())

    for _ in range(50):
        category = random.choice(categories)
        description = random.choice(EXPENSE_DESCRIPTIONS[category])
        amount = round(random.uniform(50, 2000), 2)

        # Generate random date
        random_days = random.randint(0, 90)
        expense_date = datetime.now() - timedelta(days=random_days)

        # Add expense directly
        conn = database.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO expenses (category, description, amount, expense_date)
            VALUES (?, ?, ?, ?)
        ''', (category, description, amount, expense_date))
        conn.commit()
        conn.close()

    return True, "Sample data generated successfully! 50 products, 100 sales, 50 expenses created."

def clear_all_data():
    """Clear all data from database (for testing)"""
    conn = database.get_connection()
    cursor = conn.cursor()

    cursor.execute('DELETE FROM sales')
    cursor.execute('DELETE FROM expenses')
    cursor.execute('DELETE FROM products')
    cursor.execute('DELETE FROM users')
    cursor.execute('DELETE FROM activity_logs')

    conn.commit()
    conn.close()
    return True, "All data cleared successfully!"
