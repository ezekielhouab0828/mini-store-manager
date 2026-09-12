PRAGMA foreign_keys = ON;

-- ============================
-- TABLE: Category
-- ============================
CREATE TABLE IF NOT EXISTS Category (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    description TEXT
);

-- ============================
-- TABLE: Product
-- ============================
CREATE TABLE IF NOT EXISTS Product (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    description TEXT,
    price REAL NOT NULL CHECK(price >= 0),
    stock INTEGER NOT NULL CHECK(stock >= 0),
    category_id INTEGER NOT NULL,
    FOREIGN KEY (category_id) REFERENCES Category(id)
);

-- ============================
-- TABLE: Customer
-- ============================
CREATE TABLE IF NOT EXISTS Customer (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    city TEXT,
    created_at TEXT NOT NULL
);

-- ============================
-- TABLE: CustomerOrder
-- ============================
CREATE TABLE IF NOT EXISTS CustomerOrder (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    customer_id INTEGER NOT NULL,
    order_date TEXT NOT NULL,
    status TEXT NOT NULL,
    FOREIGN KEY (customer_id) REFERENCES Customer(id)
);

-- ============================
-- TABLE: OrderItem
-- ============================
CREATE TABLE IF NOT EXISTS OrderItem (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    order_id INTEGER NOT NULL,
    product_id INTEGER NOT NULL,
    quantity INTEGER NOT NULL CHECK(quantity > 0),
    unit_price REAL NOT NULL CHECK(unit_price >= 0),
    FOREIGN KEY (order_id) REFERENCES CustomerOrder(id),
    FOREIGN KEY (product_id) REFERENCES Product(id)
);
