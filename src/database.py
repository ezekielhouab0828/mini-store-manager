import sqlite3

DB_PATH = "store.db"

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

# ============================================================
# CATEGORY
# ============================================================

def get_all_categories():
    conn = get_db()
    return conn.execute("SELECT * FROM Category ORDER BY name").fetchall()

def get_category(category_id):
    conn = get_db()
    return conn.execute("SELECT * FROM Category WHERE id = ?", (category_id,)).fetchone()

def add_category(name, description):
    conn = get_db()
    conn.execute("INSERT INTO Category (name, description) VALUES (?, ?)", (name, description))
    conn.commit()

def update_category(category_id, name, description):
    conn = get_db()
    conn.execute("UPDATE Category SET name = ?, description = ? WHERE id = ?", (name, description, category_id))
    conn.commit()

def delete_category(category_id):
    conn = get_db()
    conn.execute("DELETE FROM Category WHERE id = ?", (category_id,))
    conn.commit()

# ============================================================
# PRODUCT
# ============================================================

def get_all_products():
    conn = get_db()
    return conn.execute("""
        SELECT p.*, c.name AS category_name
        FROM Product p
        JOIN Category c ON p.category_id = c.id
        ORDER BY p.name
    """).fetchall()

def get_product(product_id):
    conn = get_db()
    return conn.execute("SELECT * FROM Product WHERE id = ?", (product_id,)).fetchone()

def add_product(name, description, price, stock, category_id):
    conn = get_db()
    conn.execute("""
        INSERT INTO Product (name, description, price, stock, category_id)
        VALUES (?, ?, ?, ?, ?)
    """, (name, description, price, stock, category_id))
    conn.commit()

def update_product(product_id, name, description, price, stock, category_id):
    conn = get_db()
    conn.execute("""
        UPDATE Product
        SET name = ?, description = ?, price = ?, stock = ?, category_id = ?
        WHERE id = ?
    """, (name, description, price, stock, category_id, product_id))
    conn.commit()

def delete_product(product_id):
    conn = get_db()
    conn.execute("DELETE FROM Product WHERE id = ?", (product_id,))
    conn.commit()

# ============================================================
# CUSTOMER
# ============================================================

def get_all_customers():
    conn = get_db()
    return conn.execute("""
        SELECT c.*,
               COUNT(o.id) AS order_count,
               COALESCE(SUM(oi.quantity * oi.unit_price), 0) AS total_spent
        FROM Customer c
        LEFT JOIN CustomerOrder o ON o.customer_id = c.id
        LEFT JOIN OrderItem oi ON oi.order_id = o.id
        GROUP BY c.id
        ORDER BY c.last_name, c.first_name
    """).fetchall()

def get_customer(customer_id):
    conn = get_db()
    return conn.execute("SELECT * FROM Customer WHERE id = ?", (customer_id,)).fetchone()

def add_customer(first_name, last_name, email, city, created_at):
    conn = get_db()
    conn.execute("""
        INSERT INTO Customer (first_name, last_name, email, city, created_at)
        VALUES (?, ?, ?, ?, ?)
    """, (first_name, last_name, email, city, created_at))
    conn.commit()

def update_customer(customer_id, first_name, last_name, email, city):
    conn = get_db()
    conn.execute("""
        UPDATE Customer
        SET first_name = ?, last_name = ?, email = ?, city = ?
        WHERE id = ?
    """, (first_name, last_name, email, city, customer_id))
    conn.commit()

def delete_customer(customer_id):
    conn = get_db()
    conn.execute("DELETE FROM Customer WHERE id = ?", (customer_id,))
    conn.commit()

# ============================================================
# CUSTOMER ORDER
# ============================================================

def get_all_orders():
    conn = get_db()
    return conn.execute("""
        SELECT o.*,
               c.first_name || ' ' || c.last_name AS customer_name,
               COALESCE(SUM(oi.quantity * oi.unit_price), 0) AS total
        FROM CustomerOrder o
        JOIN Customer c ON o.customer_id = c.id
        LEFT JOIN OrderItem oi ON oi.order_id = o.id
        GROUP BY o.id
        ORDER BY o.order_date DESC
    """).fetchall()

def get_order(order_id):
    conn = get_db()
    return conn.execute("""
        SELECT o.*,
               c.first_name || ' ' || c.last_name AS customer_name,
               c.email, c.city
        FROM CustomerOrder o
        JOIN Customer c ON o.customer_id = c.id
        WHERE o.id = ?
    """, (order_id,)).fetchone()

def get_order_items(order_id):
    conn = get_db()
    return conn.execute("""
        SELECT oi.*, p.name AS product_name
        FROM OrderItem oi
        JOIN Product p ON oi.product_id = p.id
        WHERE oi.order_id = ?
    """, (order_id,)).fetchall()

# ============================================================
# CREATE ORDER (TRANSACTION)
# ============================================================

def create_order(customer_id, items):
    """
    items = list of dicts:
    [
        {"product_id": 1, "quantity": 2},
        {"product_id": 5, "quantity": 1}
    ]
    """

    conn = get_db()
    try:
        cursor = conn.cursor()
        cursor.execute("BEGIN")

        # Create order
        cursor.execute("""
            INSERT INTO CustomerOrder (customer_id, order_date, status)
            VALUES (?, DATE('now'), 'Payée')
        """, (customer_id,))
        order_id = cursor.lastrowid

        # Process items
        for item in items:
            product = cursor.execute("SELECT price, stock FROM Product WHERE id = ?", (item["product_id"],)).fetchone()

            if product["stock"] < item["quantity"]:
                raise Exception("Stock insuffisant")

            # Insert order item
            cursor.execute("""
                INSERT INTO OrderItem (order_id, product_id, quantity, unit_price)
                VALUES (?, ?, ?, ?)
            """, (order_id, item["product_id"], item["quantity"], product["price"]))

            # Update stock
            cursor.execute("""
                UPDATE Product
                SET stock = stock - ?
                WHERE id = ?
            """, (item["quantity"], item["product_id"]))

        conn.commit()
        return order_id

    except Exception as e:
        conn.rollback()
        raise e

# ============================================================
# ANALYTICS
# ============================================================

def get_revenue_by_category():
    conn = get_db()
    return conn.execute("""
        SELECT c.name,
               COALESCE(SUM(oi.quantity), 0) AS units_sold,
               COALESCE(SUM(oi.quantity * oi.unit_price), 0) AS revenue
        FROM Category c
        LEFT JOIN Product p ON p.category_id = c.id
        LEFT JOIN OrderItem oi ON oi.product_id = p.id
        GROUP BY c.id
        ORDER BY revenue DESC
    """).fetchall()

def get_top_customers():
    conn = get_db()
    return conn.execute("""
        SELECT c.first_name || ' ' || c.last_name AS customer_name,
               COUNT(o.id) AS order_count,
               COALESCE(SUM(oi.quantity * oi.unit_price), 0) AS total_spent
        FROM Customer c
        LEFT JOIN CustomerOrder o ON o.customer_id = c.id
        LEFT JOIN OrderItem oi ON oi.order_id = o.id
        GROUP BY c.id
        ORDER BY total_spent DESC
        LIMIT 5
    """).fetchall()

def get_products_never_ordered():
    conn = get_db()
    return conn.execute("""
        SELECT p.*
        FROM Product p
        LEFT JOIN OrderItem oi ON oi.product_id = p.id
        WHERE oi.product_id IS NULL
        ORDER BY p.name
    """).fetchall()

def get_avg_order_value():
    conn = get_db()
    return conn.execute("""
        SELECT AVG(total) AS avg_value
        FROM (
            SELECT SUM(oi.quantity * oi.unit_price) AS total
            FROM CustomerOrder o
            LEFT JOIN OrderItem oi ON oi.order_id = o.id
            GROUP BY o.id
        )
    """).fetchone()["avg_value"]

def get_orders_above_average():
    conn = get_db()
    return conn.execute("""
        WITH order_totals AS (
            SELECT o.id,
                   SUM(oi.quantity * oi.unit_price) AS total
            FROM CustomerOrder o
            LEFT JOIN OrderItem oi ON oi.order_id = o.id
            GROUP BY o.id
        ),
        avg_value AS (
            SELECT AVG(total) AS avg FROM order_totals
        )
        SELECT ot.*
        FROM order_totals ot, avg_value av
        WHERE ot.total > av.avg
        ORDER BY ot.total DESC
    """).fetchall()

def get_low_stock_products():
    conn = get_db()
    return conn.execute("""
        SELECT *
        FROM Product
        WHERE stock < 5
        ORDER BY stock ASC
    """).fetchall()

def get_sales_by_month():
    conn = get_db()
    return conn.execute("""
        SELECT strftime('%Y-%m', o.order_date) AS month,
               SUM(oi.quantity * oi.unit_price) AS revenue
        FROM CustomerOrder o
        LEFT JOIN OrderItem oi ON oi.order_id = o.id
        GROUP BY month
        ORDER BY month
    """).fetchall()
