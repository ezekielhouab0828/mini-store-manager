from flask import Blueprint, render_template, request, redirect
from database import (
    get_all_customers,
    get_customer,
    add_customer,
    update_customer,
    delete_customer,
    get_all_orders
)

customers_bp = Blueprint("customers", __name__)

@customers_bp.route("/")
def list_customers():
    customers = get_all_customers()
    return render_template("customers/list.html", customers=customers)

@customers_bp.route("/<int:customer_id>")
def customer_detail(customer_id):
    customer = get_customer(customer_id)
    orders = get_all_orders()
    orders = [o for o in orders if o["customer_id"] == customer_id]
    return render_template("customers/detail.html", customer=customer, orders=orders)

@customers_bp.route("/add", methods=["GET", "POST"])
def add_customer_route():
    if request.method == "GET":
        return render_template("customers/add.html")

    first_name = request.form["first_name"]
    last_name = request.form["last_name"]
    email = request.form["email"]
    city = request.form["city"]
    created_at = request.form["created_at"]

    add_customer(first_name, last_name, email, city, created_at)
    return redirect("/customers")

@customers_bp.route("/edit/<int:customer_id>", methods=["GET", "POST"])
def edit_customer_route(customer_id):
    customer = get_customer(customer_id)

    if request.method == "GET":
        return render_template("customers/edit.html", customer=customer)

    first_name = request.form["first_name"]
    last_name = request.form["last_name"]
    email = request.form["email"]
    city = request.form["city"]

    update_customer(customer_id, first_name, last_name, email, city)
    return redirect(f"/customers/{customer_id}")

@customers_bp.route("/delete/<int:customer_id>")
def delete_customer_route(customer_id):
    delete_customer(customer_id)
    return redirect("/customers")
