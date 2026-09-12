from flask import Blueprint, render_template, request, redirect, url_for, flash
from database import (
    get_all_orders,
    get_order,
    get_order_items,
    get_all_customers,
    get_all_products,
    create_order
)
import sqlite3

orders_bp = Blueprint("orders", __name__)

# ------------------------------------------------------------
# LISTE DES COMMANDES
# ------------------------------------------------------------
@orders_bp.route("/")
def list_orders():
    orders = get_all_orders()
    return render_template("orders/list.html", orders=orders)


# ------------------------------------------------------------
# DÉTAIL D’UNE COMMANDE
# ------------------------------------------------------------
@orders_bp.route("/<int:order_id>")
def order_detail(order_id):
    order = get_order(order_id)
    items = get_order_items(order_id)

    # Calcul du total
    total = sum(i["quantity"] * i["unit_price"] for i in items)

    products = get_all_products()

    return render_template(
        "orders/edit.html",
        order=order,
        items=items,
        products=products,
        total=total
    )


# ------------------------------------------------------------
# CRÉATION D’UNE COMMANDE
# ------------------------------------------------------------
@orders_bp.route("/add", methods=["GET", "POST"])
def add_order_route():
    if request.method == "GET":
        customers = get_all_customers()
        return render_template("orders/create.html", customers=customers)

    # POST → création de commande
    customer_id = int(request.form["customer_id"])
    items = []  # pas d’items à la création

    order_id = create_order(customer_id, items)
    flash("Commande créée avec succès.", "success")
    return redirect(url_for("orders.order_detail", order_id=order_id))


# ------------------------------------------------------------
# MISE À JOUR DU STATUT
# ------------------------------------------------------------
@orders_bp.route("/<int:order_id>/update_status", methods=["POST"])
def update_status(order_id):
    new_status = request.form["status"]

    conn = sqlite3.connect("database/store.db")
    conn.execute("UPDATE CustomerOrder SET status = ? WHERE id = ?", (new_status, order_id))
    conn.commit()
    conn.close()

    flash("Statut mis à jour.", "success")
    return redirect(url_for("orders.order_detail", order_id=order_id))


# ------------------------------------------------------------
# AJOUT D’UN PRODUIT DANS UNE COMMANDE
# ------------------------------------------------------------
@orders_bp.route("/<int:order_id>/add_item", methods=["POST"])
def add_item(order_id):
    product_id = int(request.form["product_id"])
    quantity = int(request.form["quantity"])

    conn = sqlite3.connect("database/store.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    # Vérifier stock
    product = cursor.execute("SELECT stock, price FROM Product WHERE id = ?", (product_id,)).fetchone()
    if product["stock"] < quantity:
        flash("Stock insuffisant.", "danger")
        return redirect(url_for("orders.order_detail", order_id=order_id))

    # Ajouter item
    cursor.execute("""
        INSERT INTO OrderItem (order_id, product_id, quantity, unit_price)
        VALUES (?, ?, ?, ?)
    """, (order_id, product_id, quantity, product["price"]))

    # Mettre à jour stock
    cursor.execute("""
        UPDATE Product SET stock = stock - ? WHERE id = ?
    """, (quantity, product_id))

    conn.commit()
    conn.close()

    flash("Produit ajouté à la commande.", "success")
    return redirect(url_for("orders.order_detail", order_id=order_id))


# ------------------------------------------------------------
# SUPPRESSION D’UN PRODUIT D’UNE COMMANDE
# ------------------------------------------------------------
@orders_bp.route("/remove_item/<int:item_id>")
def remove_item(item_id):
    conn = sqlite3.connect("database/store.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    # Récupérer l’item
    item = cursor.execute("SELECT * FROM OrderItem WHERE id = ?", (item_id,)).fetchone()
    if not item:
        flash("Produit introuvable.", "danger")
        return redirect(url_for("orders.list_orders"))

    order_id = item["order_id"]

    # Rendre le stock
    cursor.execute("""
        UPDATE Product SET stock = stock + ?
        WHERE id = ?
    """, (item["quantity"], item["product_id"]))

    # Supprimer l’item
    cursor.execute("DELETE FROM OrderItem WHERE id = ?", (item_id,))
    conn.commit()
    conn.close()

    flash("Produit retiré de la commande.", "success")
    return redirect(url_for("orders.order_detail", order_id=order_id))
