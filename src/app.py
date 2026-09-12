from flask import Flask, render_template
from customers.routes import customers_bp
from products.routes import products_bp
from orders.routes import orders_bp
from categories.routes import categories_bp
from analytics.routes import analytics_bp

from database import (
    get_all_customers,
    get_all_products,
    get_all_orders
)

from collections import defaultdict
from datetime import datetime

app = Flask(__name__)

# ⭐ SECRET KEY OBLIGATOIRE POUR flash(), session, login, etc.
app.secret_key = "ezekiel_super_secret_key_2026"

# ============================================================
# Enregistrement des blueprints
# ============================================================

app.register_blueprint(customers_bp)
app.register_blueprint(products_bp)
app.register_blueprint(orders_bp)
app.register_blueprint(categories_bp)
app.register_blueprint(analytics_bp)

# ============================================================
# Dashboard
# ============================================================

@app.route("/")
@app.route("/dashboard")
def dashboard():
    customers = get_all_customers()
    products = get_all_products()
    orders = get_all_orders()

    # KPIs
    total_customers = len(customers)
    total_products = len(products)
    total_orders = len(orders)
    total_revenue = sum(o["total"] for o in orders)

    # Ventes par produit
    sales_by_product = defaultdict(float)
    qty_by_product = defaultdict(int)

    for o in orders:
        sales_by_product[o["product_name"]] += o["total"]
        qty_by_product[o["product_name"]] += o["quantity"]

    sales_labels = list(sales_by_product.keys())
    sales_values = list(sales_by_product.values())

    # Top 5 produits
    top_products = sorted(
        sales_by_product.items(),
        key=lambda x: x[1],
        reverse=True
    )[:5]

    top_products_labels = [name for name, total in top_products]
    top_products_values = [total for name, total in top_products]

    # Produit le plus vendu (quantité)
    if qty_by_product:
        best_product_name, best_product_qty = max(
            qty_by_product.items(),
            key=lambda x: x[1]
        )
    else:
        best_product_name, best_product_qty = None, 0

    # Stock par produit
    stock_labels = [p["name"] for p in products]
    stock_values = [p["stock"] for p in products]

    # Ventes mensuelles
    sales_by_month = defaultdict(float)
    for o in orders:
        if o["created_at"]:
            try:
                dt = datetime.fromisoformat(o["created_at"])
                key = dt.strftime("%Y-%m")
                sales_by_month[key] += o["total"]
            except:
                pass

    monthly_labels = sorted(sales_by_month.keys())
    monthly_values = [sales_by_month[m] for m in monthly_labels]

    # Commandes par jour
    orders_by_day = defaultdict(int)
    for o in orders:
        if o["created_at"]:
            try:
                dt = datetime.fromisoformat(o["created_at"])
                key = dt.strftime("%Y-%m-%d")
                orders_by_day[key] += 1
            except:
                pass

    daily_labels = sorted(orders_by_day.keys())
    daily_values = [orders_by_day[d] for d in daily_labels]

    # 5 dernières commandes
    def sort_key(o):
        try:
            return datetime.fromisoformat(o["created_at"])
        except:
            return o["id"]

    recent_orders = sorted(orders, key=sort_key, reverse=True)[:5]

    return render_template(
        "dashboard.html",
        total_customers=total_customers,
        total_products=total_products,
        total_orders=total_orders,
        total_revenue=total_revenue,
        sales_labels=sales_labels,
        sales_values=sales_values,
        stock_labels=stock_labels,
        stock_values=stock_values,
        top_products_labels=top_products_labels,
        top_products_values=top_products_values,
        monthly_labels=monthly_labels,
        monthly_values=monthly_values,
        daily_labels=daily_labels,
        daily_values=daily_values,
        recent_orders=recent_orders,
        best_product_name=best_product_name,
        best_product_qty=best_product_qty
    )

# ============================================================
# Lancement
# ============================================================

if __name__ == "__main__":
    app.run(debug=True)
