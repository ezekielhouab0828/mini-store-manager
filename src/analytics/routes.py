from flask import Blueprint, render_template
from database import (
    get_revenue_by_category,
    get_top_customers,
    get_products_never_ordered,
    get_avg_order_value,
    get_orders_above_average,
    get_low_stock_products,
    get_sales_by_month
)

analytics_bp = Blueprint("analytics", __name__)

@analytics_bp.route("/")
def analytics_dashboard():
    stats = {
        "revenue_by_category": get_revenue_by_category(),
        "top_customers": get_top_customers(),
        "products_never_ordered": get_products_never_ordered(),
        "avg_order_value": get_avg_order_value(),
        "orders_above_avg": get_orders_above_average(),
        "low_stock_products": get_low_stock_products(),
        "sales_by_month": get_sales_by_month()
    }
    return render_template("analytics/dashboard.html", **stats)
