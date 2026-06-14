"""
Vyapar — Indian grocery store seed data
Populates Supabase with users, products, sales, expenses, and activity logs.

Run from terminal:
    python seed.py           # seed only if database is empty
    python seed.py --force   # clear everything and reseed
"""

import argparse
import random
from datetime import datetime, timedelta

import auth
import database

# ---------------------------------------------------------------------------
# Demo users (login with these after seeding)
# ---------------------------------------------------------------------------
USERS = [
    {"name": "Rajesh Kumar", "email": "owner@biztrack.ai", "password": "demo123", "role": "owner"},
    {"name": "Priya Sharma", "email": "staff@biztrack.ai", "password": "demo123", "role": "staff"},
    {"name": "Amit Patel", "email": "manager@biztrack.ai", "password": "demo123", "role": "staff"},
]

# ---------------------------------------------------------------------------
# Indian grocery catalog (prices in ₹)
# ---------------------------------------------------------------------------
PRODUCTS = [
    {"name": "India Gate Basmati Rice 5kg", "category": "Staples & Rice", "supplier": "Krishna Kirana Wholesale", "cost_price": 320.00, "selling_price": 450.00, "quantity": 85, "reorder_level": 25},
    {"name": "Sona Masoori Rice 10kg", "category": "Staples & Rice", "supplier": "Annapurna Traders", "cost_price": 480.00, "selling_price": 620.00, "quantity": 42, "reorder_level": 15},
    {"name": "Aashirvaad Atta 10kg", "category": "Staples & Rice", "supplier": "ITC Distributor", "cost_price": 350.00, "selling_price": 420.00, "quantity": 55, "reorder_level": 20},
    {"name": "Toor Dal 1kg", "category": "Pulses & Lentils", "supplier": "Local Mandi Supplier", "cost_price": 110.00, "selling_price": 138.00, "quantity": 38, "reorder_level": 15},
    {"name": "Moong Dal 1kg", "category": "Pulses & Lentils", "supplier": "Local Mandi Supplier", "cost_price": 95.00, "selling_price": 122.00, "quantity": 5, "reorder_level": 20},
    {"name": "Chana Dal 1kg", "category": "Pulses & Lentils", "supplier": "Krishna Kirana Wholesale", "cost_price": 72.00, "selling_price": 95.00, "quantity": 45, "reorder_level": 18},
    {"name": "Urad Dal 1kg", "category": "Pulses & Lentils", "supplier": "Annapurna Traders", "cost_price": 118.00, "selling_price": 152.00, "quantity": 28, "reorder_level": 12},
    {"name": "Fortune Sunflower Oil 1L", "category": "Oil & Ghee", "supplier": "HUL Wholesale", "cost_price": 118.00, "selling_price": 142.00, "quantity": 62, "reorder_level": 20},
    {"name": "Dhara Mustard Oil 1L", "category": "Oil & Ghee", "supplier": "Reliance Fresh Supply", "cost_price": 128.00, "selling_price": 158.00, "quantity": 7, "reorder_level": 25},
    {"name": "Amul Pure Ghee 1L", "category": "Oil & Ghee", "supplier": "Amul Distributor", "cost_price": 485.00, "selling_price": 565.00, "quantity": 3, "reorder_level": 10},
    {"name": "Tata Salt 1kg", "category": "Staples & Rice", "supplier": "Metro Cash & Carry", "cost_price": 22.00, "selling_price": 28.00, "quantity": 120, "reorder_level": 30},
    {"name": "Tata Tea Gold 500g", "category": "Beverages & Tea", "supplier": "Tata Consumer Products", "cost_price": 185.00, "selling_price": 225.00, "quantity": 34, "reorder_level": 12},
    {"name": "Bru Instant Coffee 50g", "category": "Beverages & Tea", "supplier": "HUL Wholesale", "cost_price": 168.00, "selling_price": 205.00, "quantity": 22, "reorder_level": 10},
    {"name": "Maggi Noodles 70g (12-pack)", "category": "Instant & Packaged", "supplier": "Nestlé Distributor", "cost_price": 125.00, "selling_price": 158.00, "quantity": 48, "reorder_level": 15},
    {"name": "Maggi Masala 72g (12-pack)", "category": "Instant & Packaged", "supplier": "Nestlé Distributor", "cost_price": 118.00, "selling_price": 148.00, "quantity": 36, "reorder_level": 12},
    {"name": "Turmeric Powder 200g", "category": "Spices & Masala", "supplier": "Annapurna Traders", "cost_price": 35.00, "selling_price": 52.00, "quantity": 55, "reorder_level": 15},
    {"name": "Red Chilli Powder 200g", "category": "Spices & Masala", "supplier": "Krishna Kirana Wholesale", "cost_price": 48.00, "selling_price": 72.00, "quantity": 44, "reorder_level": 12},
    {"name": "MDH Garam Masala 100g", "category": "Spices & Masala", "supplier": "Spices Wholesale Hub", "cost_price": 58.00, "selling_price": 85.00, "quantity": 2, "reorder_level": 8},
    {"name": "Everest Chaat Masala 100g", "category": "Spices & Masala", "supplier": "Spices Wholesale Hub", "cost_price": 42.00, "selling_price": 58.00, "quantity": 18, "reorder_level": 10},
    {"name": "Parle-G Gold 1kg", "category": "Biscuits & Snacks", "supplier": "Parle Distributor", "cost_price": 78.00, "selling_price": 98.00, "quantity": 72, "reorder_level": 20},
    {"name": "Britannia Good Day 500g", "category": "Biscuits & Snacks", "supplier": "Britannia Supply Co.", "cost_price": 52.00, "selling_price": 68.00, "quantity": 41, "reorder_level": 15},
    {"name": "Haldiram Aloo Bhujia 400g", "category": "Biscuits & Snacks", "supplier": "Haldiram Agency", "cost_price": 68.00, "selling_price": 88.00, "quantity": 29, "reorder_level": 12},
    {"name": "Amul Taaza Milk 1L", "category": "Dairy", "supplier": "Amul Distributor", "cost_price": 52.00, "selling_price": 62.00, "quantity": 95, "reorder_level": 30},
    {"name": "Amul Butter 500g", "category": "Dairy", "supplier": "Amul Distributor", "cost_price": 228.00, "selling_price": 275.00, "quantity": 4, "reorder_level": 12},
    {"name": "Amul Masti Curd 500g", "category": "Dairy", "supplier": "Amul Distributor", "cost_price": 28.00, "selling_price": 35.00, "quantity": 38, "reorder_level": 15},
    {"name": "Surf Excel Easy Wash 1kg", "category": "Household & Cleaning", "supplier": "HUL Wholesale", "cost_price": 112.00, "selling_price": 138.00, "quantity": 31, "reorder_level": 10},
    {"name": "Vim Dishwash Gel 500ml", "category": "Household & Cleaning", "supplier": "HUL Wholesale", "cost_price": 48.00, "selling_price": 62.00, "quantity": 26, "reorder_level": 10},
    {"name": "Harpic Toilet Cleaner 500ml", "category": "Household & Cleaning", "supplier": "Reckitt Distributor", "cost_price": 78.00, "selling_price": 95.00, "quantity": 19, "reorder_level": 8},
    {"name": "Colgate Strong Teeth 200g", "category": "Personal Care", "supplier": "Colgate Palmolive India", "cost_price": 88.00, "selling_price": 105.00, "quantity": 42, "reorder_level": 12},
    {"name": "Lifebuoy Soap 125g", "category": "Personal Care", "supplier": "HUL Wholesale", "cost_price": 26.00, "selling_price": 34.00, "quantity": 88, "reorder_level": 25},
    {"name": "Fortune Groundnut Oil 1L", "category": "Oil & Ghee", "supplier": "Adani Wilmar Supply", "cost_price": 138.00, "selling_price": 168.00, "quantity": 33, "reorder_level": 12},
    {"name": "Rajdhani Besan 1kg", "category": "Staples & Rice", "supplier": "Rajdhani Foods", "cost_price": 72.00, "selling_price": 92.00, "quantity": 24, "reorder_level": 10},
    {"name": "MTR Poha 500g", "category": "Instant & Packaged", "supplier": "MTR Foods Distributor", "cost_price": 42.00, "selling_price": 55.00, "quantity": 15, "reorder_level": 8},
    {"name": "Real Mixed Fruit Juice 1L", "category": "Beverages & Tea", "supplier": "Dabur Distributor", "cost_price": 82.00, "selling_price": 105.00, "quantity": 6, "reorder_level": 15},
    {"name": "Kellogg's Chocos 375g", "category": "Biscuits & Snacks", "supplier": "Kellogg Supply India", "cost_price": 145.00, "selling_price": 178.00, "quantity": 14, "reorder_level": 8},
    {"name": "Tata Sampann Cashews 200g", "category": "Dry Fruits & Nuts", "supplier": "Tata Consumer Products", "cost_price": 185.00, "selling_price": 235.00, "quantity": 11, "reorder_level": 6},
    {"name": "Aashirvaad Select Rice 5kg", "category": "Staples & Rice", "supplier": "ITC Distributor", "cost_price": 335.00, "selling_price": 425.00, "quantity": 30, "reorder_level": 12},
    {"name": "Kissan Tomato Ketchup 1kg", "category": "Sauces & Condiments", "supplier": "HUL Wholesale", "cost_price": 95.00, "selling_price": 118.00, "quantity": 27, "reorder_level": 10},
    {"name": "Dhara Mustard Oil 5L", "category": "Oil & Ghee", "supplier": "Mother Dairy Supply", "cost_price": 620.00, "selling_price": 745.00, "quantity": 8, "reorder_level": 5},
    {"name": "Frooti Mango Drink 1L", "category": "Beverages & Tea", "supplier": "Parle Agro Distributor", "cost_price": 38.00, "selling_price": 48.00, "quantity": 1, "reorder_level": 15},
]

EXPENSES = [
    ("Rent", "Monthly shop rent — MG Road kirana", 45000.00, 75),
    ("Rent", "Cold storage unit rent", 8500.00, 74),
    ("Utilities", "Electricity bill — March", 8200.00, 68),
    ("Utilities", "Electricity bill — April", 7850.00, 38),
    ("Utilities", "Electricity bill — May", 9100.00, 8),
    ("Utilities", "Water & sewer charges", 1200.00, 60),
    ("Utilities", "LPG cylinder refill (commercial)", 1850.00, 45),
    ("Salaries", "Counter staff — March payroll", 22000.00, 70),
    ("Salaries", "Delivery helper wages", 12000.00, 63),
    ("Salaries", "April payroll — store team", 22000.00, 33),
    ("Salaries", "May payroll — store team", 22000.00, 3),
    ("Transportation", "Supplier delivery — wholesale market", 4200.00, 50),
    ("Transportation", "Auto-rickshaw stock pickup", 850.00, 25),
    ("Transportation", "Diesel for delivery bike", 2200.00, 18),
    ("Marketing", "Local newspaper ad", 3500.00, 55),
    ("Marketing", "WhatsApp catalogue promotion", 500.00, 40),
    ("Marketing", "Festive banner & flex printing", 2800.00, 82),
    ("Marketing", "UPI cashback offer sponsorship", 1500.00, 22),
    ("Supplies", "Plastic carry bags (50kg)", 2800.00, 42),
    ("Supplies", "Packing tape & labels", 650.00, 15),
    ("Supplies", "Cleaning supplies & mop", 1500.00, 20),
    ("Supplies", "Weighing scale battery", 350.00, 5),
    ("Equipment", "Refrigerator compressor repair", 4500.00, 90),
    ("Equipment", "Barcode scanner", 3200.00, 77),
    ("Equipment", "New weighing scale", 1800.00, 48),
    ("Insurance", "Shop insurance premium", 8500.00, 65),
    ("Insurance", "Fire extinguisher refill", 1200.00, 33),
    ("Taxes", "GST monthly remittance", 18500.00, 72),
    ("Taxes", "GST remittance — April", 19200.00, 32),
    ("Taxes", "Trade licence renewal", 3500.00, 45),
    ("Taxes", "Professional tax", 2500.00, 31),
    ("Miscellaneous", "Pest control service", 1800.00, 10),
    ("Miscellaneous", "Accountant fees", 2500.00, 58),
    ("Miscellaneous", "Customer refund — spoiled milk batch", 310.00, 5),
    ("Miscellaneous", "Tea & snacks for inventory day", 450.00, 18),
    ("Miscellaneous", "Software subscription — billing app", 499.00, 1),
    ("Transportation", "May wholesale market trip", 3800.00, 0),
    ("Marketing", "May pamphlet distribution", 1200.00, 0),
    ("Supplies", "New price tags & shelf labels", 890.00, 0),
    ("Utilities", "Internet & CCTV subscription", 1499.00, 28),
    ("Equipment", "LED tube lights replacement", 2200.00, 12),
    ("Miscellaneous", "Donation — local temple festival", 1100.00, 2),
    ("Transportation", "Emergency late-night stock run", 600.00, 1),
    ("Supplies", "Cardboard boxes for bulk orders", 1100.00, 0),
    ("Taxes", "TDS deposit — staff salary", 4200.00, 15),
]

ACTIVITY_LOGS = [
    ("Login", "User Rajesh Kumar logged in"),
    ("Login", "User Priya Sharma logged in"),
    ("Add Product", "Added India Gate Basmati Rice 5kg (₹450.00)"),
    ("Add Product", "Added Amul Pure Ghee 1L (₹565.00)"),
    ("Add Product", "Added Tata Tea Gold 500g (₹225.00)"),
    ("Record Sale", "Sold 2x India Gate Basmati Rice 5kg (₹900.00)"),
    ("Record Sale", "Sold 1x Amul Taaza Milk 1L (₹62.00)"),
    ("Record Sale", "Sold 3x Parle-G Gold 1kg (₹294.00)"),
    ("Add Expense", "Added ₹45,000.00 for Rent"),
    ("Add Expense", "Added ₹3,500.00 for Marketing"),
    ("Update Product", "Updated Moong Dal 1kg stock levels"),
    ("Record Sale", "Sold 1x Amul Pure Ghee 1L (₹565.00)"),
    ("Record Sale", "Sold 2x Britannia Good Day 500g (₹136.00)"),
    ("Add Expense", "Added ₹8,200.00 for Utilities"),
    ("Delete Expense", "Deleted duplicate expense entry"),
    ("Record Sale", "Sold 1x Fortune Sunflower Oil 1L (₹142.00)"),
    ("Add Product", "Added MDH Garam Masala 100g (₹85.00)"),
    ("Login", "User Amit Patel logged in"),
    ("Record Sale", "Sold 4x Lifebuoy Soap 125g (₹136.00)"),
    ("Add Expense", "Added ₹22,000.00 for Salaries"),
    ("Update Product", "Updated Frooti Mango Drink 1L reorder level"),
    ("Record Sale", "Sold 1x Haldiram Aloo Bhujia 400g (₹88.00)"),
    ("Record Sale", "Sold 2x Maggi Noodles 70g (12-pack) (₹316.00)"),
    ("Add Expense", "Added ₹2,800.00 for Supplies"),
    ("Login", "User Rajesh Kumar logged in"),
]


def has_data():
    """Return True if any seedable data already exists."""
    response = database.db().table("products").select("*", count="exact").limit(1).execute()
    return bool(response.count and response.count > 0)


def clear_all_data():
    """Remove all rows from every table."""
    db = database.db()
    db.table("activity_logs").delete().gte("log_id", 0).execute()
    db.table("sales").delete().gte("sale_id", 0).execute()
    try:
        db.table("bill_items").delete().gte("item_id", 0).execute()
        db.table("bills").delete().gte("bill_id", 0).execute()
    except Exception:
        pass
    db.table("expenses").delete().gte("expense_id", 0).execute()
    db.table("products").delete().gte("product_id", 0).execute()
    db.table("users").delete().gte("id", 0).execute()
    return True, "All data cleared successfully!"


def _days_ago(days, hour=None, minute=0):
    dt = datetime.now().replace(second=0, microsecond=0) - timedelta(days=days)
    if hour is not None:
        dt = dt.replace(hour=hour % 24, minute=minute % 60)
    else:
        dt = dt.replace(hour=random.randint(9, 20), minute=random.randint(0, 59))
    return dt.isoformat()


def _seed_users():
    """Insert demo users; returns {email: id} map."""
    user_ids = {}
    for user in USERS:
        success, result = auth.signup(
            user["name"], user["email"], user["password"], user["role"]
        )
        if success:
            row = (
                database.db()
                .table("users")
                .select("id")
                .eq("email", user["email"])
                .execute()
            )
            user_ids[user["email"]] = row.data[0]["id"]
        else:
            row = (
                database.db()
                .table("users")
                .select("id")
                .eq("email", user["email"])
                .execute()
            )
            if row.data:
                user_ids[user["email"]] = row.data[0]["id"]
    return user_ids


def _seed_products():
    """Insert products; returns list of product dicts with product_id."""
    now = datetime.now().isoformat()
    rows = [{**p, "date_added": now} for p in PRODUCTS]
    response = database.db().table("products").insert(rows).execute()
    return response.data or []


def _seed_sales(products, user_ids):
    """Insert historical + recent sales; sync inventory quantities."""
    random.seed(42)
    owner_id = user_ids.get("owner@biztrack.ai")
    staff_id = user_ids.get("staff@biztrack.ai")

    popular = {
        p["name"] for p in products
        if p["category"] in ("Staples & Rice", "Dairy", "Oil & Ghee", "Biscuits & Snacks")
    }
    stock = {p["product_id"]: p["quantity"] for p in products}
    sales_rows = []

    for _ in range(160):
        product = random.choice(products)
        if product["name"] in popular:
            product = random.choice([p for p in products if p["name"] in popular] or products)

        qty = random.randint(1, 5)
        days = random.randint(0, 89)
        sale_date = _days_ago(days)
        total = round(qty * product["selling_price"], 2)

        sales_rows.append({
            "product_id": product["product_id"],
            "product_name": product["name"],
            "quantity_sold": qty,
            "unit_price": product["selling_price"],
            "total_amount": total,
            "sale_date": sale_date,
        })
        stock[product["product_id"]] = max(0, stock[product["product_id"]] - qty)

    today_targets = products[:8]
    for i, product in enumerate(today_targets):
        qty = random.randint(1, 4)
        total = round(qty * product["selling_price"], 2)
        sales_rows.append({
            "product_id": product["product_id"],
            "product_name": product["name"],
            "quantity_sold": qty,
            "unit_price": product["selling_price"],
            "total_amount": total,
            "sale_date": _days_ago(0, hour=9 + i, minute=12 * i),
        })
        stock[product["product_id"]] = max(0, stock[product["product_id"]] - qty)

    db = database.db()
    chunk_size = 50
    for i in range(0, len(sales_rows), chunk_size):
        db.table("sales").insert(sales_rows[i:i + chunk_size]).execute()

    for product_id, quantity in stock.items():
        db.table("products").update({"quantity": quantity}).eq("product_id", product_id).execute()

    return len(sales_rows), owner_id, staff_id


def _seed_expenses():
    """Insert expense records."""
    rows = [
        {
            "category": cat,
            "description": desc,
            "amount": amount,
            "expense_date": _days_ago(days),
        }
        for cat, desc, amount, days in EXPENSES
    ]
    db = database.db()
    chunk_size = 50
    for i in range(0, len(rows), chunk_size):
        db.table("expenses").insert(rows[i:i + chunk_size]).execute()
    return len(rows)


def _seed_activity_logs(user_ids):
    """Insert activity log entries."""
    owner_id = user_ids.get("owner@biztrack.ai", 1)
    staff_id = user_ids.get("staff@biztrack.ai", 2)
    assignees = [owner_id, staff_id, user_ids.get("manager@biztrack.ai", staff_id)]

    rows = []
    for i, (action, details) in enumerate(ACTIVITY_LOGS):
        rows.append({
            "user_id": assignees[i % len(assignees)],
            "action": action,
            "details": details,
            "timestamp": _days_ago(min(i * 2, 60), hour=9 + (i % 8)),
        })

    database.db().table("activity_logs").insert(rows).execute()
    return len(rows)


def seed_all(force=False):
    """
    Seed the full Indian grocery dataset.
    Returns (success: bool, message: str).
    """
    if has_data():
        if not force:
            return False, "Database already has data. Run: python seed.py --force"
        clear_all_data()

    user_ids = _seed_users()
    products = _seed_products()
    sale_count, _, _ = _seed_sales(products, user_ids)
    expense_count = _seed_expenses()
    log_count = _seed_activity_logs(user_ids)

    updated = database.db().table("products").select("quantity, reorder_level").execute()
    low_stock = sum(
        1 for p in (updated.data or [])
        if p["quantity"] < p["reorder_level"]
    )

    return True, (
        f"Indian grocery seed complete! "
        f"{len(USERS)} users, {len(products)} products ({low_stock} low-stock), "
        f"{sale_count} sales, {expense_count} expenses, {log_count} activity logs."
    )


def main():
    parser = argparse.ArgumentParser(description="Seed Vyapar Indian grocery demo data")
    parser.add_argument(
        "--force", action="store_true",
        help="Clear existing data and reseed from scratch",
    )
    args = parser.parse_args()

    print("Vyapar — seeding Indian grocery data...")
    success, message = seed_all(force=args.force)
    print(message)

    if success:
        print("\nDemo logins:")
        for u in USERS:
            print(f"  {u['role'].title():6}  {u['email']}  /  {u['password']}")
    else:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
