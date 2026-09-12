from flask import Flask, render_template
from products.routes import products_bp
from customers.routes import customers_bp
from orders.routes import orders_bp
from categories.routes import categories_bp
from analytics.routes import analytics_bp

app = Flask(__name__)

# Enregistrement des blueprints
app.register_blueprint(products_bp, url_prefix="/products")
app.register_blueprint(customers_bp, url_prefix="/customers")
app.register_blueprint(orders_bp, url_prefix="/orders")
app.register_blueprint(categories_bp, url_prefix="/categories")
app.register_blueprint(analytics_bp, url_prefix="/analytics")

# Page d'accueil (Dashboard)
@app.route("/")
def dashboard():
    return render_template("dashboard.html")

if __name__ == "__main__":
    app.run(debug=True)
