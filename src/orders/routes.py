from flask import Blueprint, render_template, request, redirect
from database import (
    get_all_orders,
    get_order,
    get_order_items,
    get_all_customers,
    get_all_products,
    create_order
)

orders_bp = Blueprint("orders", __name__)

@orders_bp.route("/")
def list_orders():
    orders = get_all_orders()
    return render_template("orders/list.html", orders=orders)

@orders_bp.route("/<int:order_id>")
def order_detail(order_id):
    order = get_order(order_id)
    items = get_order_items(order_id)
    return render_template("orders/detail.html", order=order, items=items)

@orders_bp.route("/add", methods=["GET", "POST"])
def add_order_route():
    if request.method == "GET":
        customers = get_all_customers()
        products = get_all_products()
        return render_template("orders/add.html", customers=customers, products=products)

    customer_id = int(request.form["customer_id"])

    # Build items list
    items = []
    products = get_all_products()
    for p in products:
        qty = request.form.get(f"qty_{p['id']}")
        if qty and int(qty) > 0:
            items.append({"product_id": p["id"], "quantity": int(qty)})

    create_order(customer_id, items)
    return redirect("/orders")
