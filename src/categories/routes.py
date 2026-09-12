from flask import Blueprint, render_template, request, redirect
from database import (
    get_all_categories,
    get_category,
    add_category,
    update_category,
    delete_category
)

categories_bp = Blueprint("categories", __name__)

@categories_bp.route("/")
def list_categories():
    categories = get_all_categories()
    return render_template("categories/list.html", categories=categories)

@categories_bp.route("/<int:category_id>")
def category_detail(category_id):
    category = get_category(category_id)
    return render_template("categories/detail.html", category=category)

@categories_bp.route("/add", methods=["GET", "POST"])
def add_category_route():
    if request.method == "GET":
        return render_template("categories/add.html")

    name = request.form["name"]
    description = request.form["description"]
    add_category(name, description)
    return redirect("/categories")

@categories_bp.route("/edit/<int:category_id>", methods=["GET", "POST"])
def edit_category_route(category_id):
    category = get_category(category_id)

    if request.method == "GET":
        return render_template("categories/edit.html", category=category)

    name = request.form["name"]
    description = request.form["description"]
    update_category(category_id, name, description)
    return redirect(f"/categories/{category_id}")

@categories_bp.route("/delete/<int:category_id>")
def delete_category_route(category_id):
    delete_category(category_id)
    return redirect("/categories")
