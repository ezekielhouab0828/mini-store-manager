from flask import Blueprint, render_template, request, redirect
from database import (
    get_all_products,
    get_product,
    add_product,
    update_product,
    delete_product,
    get_all_categories
)

products_bp = Blueprint("products", __name__)

@products_bp.route("/")
def list_products():
    products = get_all_products()
    return render_template("products/list.html", products=products)

@products_bp.route("/add", methods=["GET", "POST"])
def add_product_route():
    if request.method == "GET":
        categories = get_all_categories()
        return render_template("products/add.html", categories=categories)

    name = request.form["name"]
    description = request.form["description"]
    price = float(request.form["price"])
    stock = int(request.form["stock"])
    category_id = int(request.form["category_id"])

    add_product(name, description, price, stock, category_id)
    return redirect("/products")

@products_bp.route("/<int:product_id>")
def product_detail(product_id):
    product = get_product(product_id)
    return render_template("products/detail.html", product=product)

@products_bp.route("/edit/<int:product_id>", methods=["GET", "POST"])
def edit_product_route(product_id):
    product = get_product(product_id)

    if request.method == "GET":
        categories = get_all_categories()
        return render_template("products/edit.html", product=product, categories=categories)

    name = request.form["name"]
    description = request.form["description"]
    price = float(request.form["price"])
    stock = int(request.form["stock"])
    category_id = int(request.form["category_id"])

    update_product(product_id, name, description, price, stock, category_id)
    return redirect(f"/products/{product_id}")

@products_bp.route("/delete/<int:product_id>")
def delete_product_route(product_id):
    delete_product(product_id)
    return redirect("/products")
