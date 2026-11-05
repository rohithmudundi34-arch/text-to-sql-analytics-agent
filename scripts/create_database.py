import sqlite3
import random
from datetime import datetime, timedelta
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
DB_PATH = DATA_DIR / "sales.db"

DATA_DIR.mkdir(exist_ok=True)

connection = sqlite3.connect(DB_PATH)
cursor = connection.cursor()

# Drop existing tables
cursor.execute("DROP TABLE IF EXISTS sales")
cursor.execute("DROP TABLE IF EXISTS customers")
cursor.execute("DROP TABLE IF EXISTS products")

# -------------------------
# Customers
# -------------------------

cursor.execute("""
CREATE TABLE customers (
    customer_id INTEGER PRIMARY KEY,
    customer_name TEXT NOT NULL,
    city TEXT NOT NULL,
    state TEXT NOT NULL,
    segment TEXT NOT NULL
)
""")

customers = [
    (1, "Rahul Sharma", "Hyderabad", "Telangana", "Consumer"),
    (2, "Priya Reddy", "Bhimavaram", "Andhra Pradesh", "Consumer"),
    (3, "Arjun Kumar", "Bangalore", "Karnataka", "Corporate"),
    (4, "Sneha Rao", "Chennai", "Tamil Nadu", "Corporate"),
    (5, "Vikram Singh", "Mumbai", "Maharashtra", "Enterprise"),
    (6, "Anjali Patel", "Pune", "Maharashtra", "Consumer"),
    (7, "Kiran Das", "Kolkata", "West Bengal", "Corporate"),
    (8, "Meena Devi", "Delhi", "Delhi", "Enterprise"),
    (9, "Rohit Verma", "Hyderabad", "Telangana", "Corporate"),
    (10, "Divya Nair", "Kochi", "Kerala", "Consumer"),
]

cursor.executemany("""
INSERT INTO customers
(customer_id, customer_name, city, state, segment)
VALUES (?, ?, ?, ?, ?)
""", customers)

# -------------------------
# Products
# -------------------------

cursor.execute("""
CREATE TABLE products (
    product_id INTEGER PRIMARY KEY,
    product_name TEXT NOT NULL,
    category TEXT NOT NULL,
    price REAL NOT NULL
)
""")

products = [
    (1, "Laptop Pro", "Electronics", 75000),
    (2, "Smartphone X", "Electronics", 45000),
    (3, "Wireless Headphones", "Accessories", 5000),
    (4, "Office Chair", "Furniture", 12000),
    (5, "Standing Desk", "Furniture", 25000),
    (6, "Mechanical Keyboard", "Accessories", 7000),
    (7, "Monitor 27", "Electronics", 22000),
    (8, "Tablet Air", "Electronics", 30000),
]

cursor.executemany("""
INSERT INTO products
(product_id, product_name, category, price)
VALUES (?, ?, ?, ?)
""", products)

# -------------------------
# Sales
# -------------------------

cursor.execute("""
CREATE TABLE sales (
    sale_id INTEGER PRIMARY KEY,
    customer_id INTEGER,
    product_id INTEGER,
    quantity INTEGER,
    sale_date TEXT,
    discount REAL,
    FOREIGN KEY(customer_id) REFERENCES customers(customer_id),
    FOREIGN KEY(product_id) REFERENCES products(product_id)
)
""")

random.seed(42)

start_date = datetime(2025, 1, 1)

sales = []

for sale_id in range(1, 501):

    customer_id = random.randint(1, 10)
    product_id = random.randint(1, 8)
    quantity = random.randint(1, 5)

    days = random.randint(0, 364)

    sale_date = start_date + timedelta(days=days)

    discount = round(random.uniform(0, 0.20), 2)

    sales.append(
        (
            sale_id,
            customer_id,
            product_id,
            quantity,
            sale_date.strftime("%Y-%m-%d"),
            discount
        )
    )

cursor.executemany("""
INSERT INTO sales
(
    sale_id,
    customer_id,
    product_id,
    quantity,
    sale_date,
    discount
)
VALUES (?, ?, ?, ?, ?, ?)
""", sales)

connection.commit()

print(f"Database created successfully: {DB_PATH}")

cursor.execute("SELECT COUNT(*) FROM sales")
print("Sales records:", cursor.fetchone()[0])

cursor.execute("SELECT COUNT(*) FROM customers")
print("Customers:", cursor.fetchone()[0])

cursor.execute("SELECT COUNT(*) FROM products")
print("Products:", cursor.fetchone()[0])

connection.close()