
from flask import Flask, render_template, request, jsonify, redirect, url_for, session, flash
import sqlite3
import json
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = "change-this-to-a-long-random-secret"


# Database connection
def get_db_connection():
    conn = sqlite3.connect("store.db")
    conn.row_factory = sqlite3.Row
    return conn


# Create database tables and sample products
def create_database():
    conn = get_db_connection()

    # Users table
    conn.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    """)

    # Products table
    conn.execute("""
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            description TEXT,
            price REAL NOT NULL,
            image TEXT
        )
    """)

    # Orders table
    conn.execute("""
        CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            items TEXT,
            total REAL
        )
    """)

    # Add user_id to existing orders table if missing
    columns = [
        column["name"]
        for column in conn.execute(
            "PRAGMA table_info(orders)"
        ).fetchall()
    ]

    if "user_id" not in columns:
        conn.execute(
            "ALTER TABLE orders ADD COLUMN user_id INTEGER"
        )

    # Sample products
    products = [
        (
            1,
            "Smart Watch",
            "Smart watch with modern features",
            1999,
            "https://images.unsplash.com/photo-1523275335684-37898b6baf30?w=400"
        ),
        (
            2,
            "Headphones",
            "High-quality wireless headphones",
            999,
            "https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=400"
        ),
        (
            3,
            "Smart Phone",
            "Modern smartphone",
            12999,
            "https://images.unsplash.com/photo-1511707171634-5f897ff02aa9?w=400"
        )
    ]

    conn.executemany("""
        INSERT OR IGNORE INTO products
        (id, name, description, price, image)
        VALUES (?, ?, ?, ?, ?)
    """, products)

    conn.commit()
    conn.close()


# Home page
@app.route('/')
def home():
    return render_template('index.html')


# User Registration
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '')

        if not username or not email or not password:
            flash("Please fill all fields.")
            return redirect(url_for('register'))

        hashed_password = generate_password_hash(password)

        conn = get_db_connection()

        try:
            conn.execute(
                """
                INSERT INTO users (username, email, password)
                VALUES (?, ?, ?)
                """,
                (username, email, hashed_password)
            )

            conn.commit()
            flash("Registration successful! Please log in.")
            return redirect(url_for('login'))

        except sqlite3.IntegrityError:
            flash("Username or email already exists.")
            return redirect(url_for('register'))

        finally:
            conn.close()

    return render_template('register.html')


# User Login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '')

        conn = get_db_connection()

        user = conn.execute(
            "SELECT * FROM users WHERE email = ?",
            (email,)
        ).fetchone()

        conn.close()

        if user and check_password_hash(user['password'], password):
            session['user_id'] = user['id']
            session['username'] = user['username']

            flash("Login successful!")
            return redirect(url_for('home'))

        flash("Invalid email or password.")
        return redirect(url_for('login'))

    return render_template('login.html')


# User Logout
@app.route('/logout')
def logout():
    session.clear()
    flash("You have logged out.")
    return redirect(url_for('login'))


# Product Details
@app.route('/product/<int:product_id>')
def product_details(product_id):
    conn = get_db_connection()

    product = conn.execute(
        "SELECT * FROM products WHERE id = ?",
        (product_id,)
    ).fetchone()

    conn.close()

    if product is None:
        return "Product not found!", 404

    return render_template('product.html', product=product)


# Place Order
@app.route('/place_order', methods=['POST'])
def place_order():

    # Require login before checkout
    if 'user_id' not in session:
        return jsonify({
            "success": False,
            "message": "Please log in before placing an order."
        }), 401

    data = request.get_json(silent=True) or {}
    cart = data.get('cart', [])

    if not isinstance(cart, list) or not cart:
        return jsonify({
            "success": False,
            "message": "Your cart is empty!"
        }), 400

    conn = get_db_connection()

    try:
        order_items = []
        total = 0

        # Get actual product prices from database
        for item in cart:
            if not isinstance(item, dict):
                return jsonify({
                    "success": False,
                    "message": "Invalid cart item."
                }), 400

            name = item.get('name')

            if not name:
                return jsonify({
                    "success": False,
                    "message": "Invalid product."
                }), 400

            product = conn.execute(
                "SELECT name, price FROM products WHERE name = ?",
                (name,)
            ).fetchone()

            if product is None:
                return jsonify({
                    "success": False,
                    "message": "Product not found."
                }), 400

            order_items.append({
                "name": product['name'],
                "price": product['price']
            })

            total += product['price']

        conn.execute(
            """
            INSERT INTO orders (items, total, user_id)
            VALUES (?, ?, ?)
            """,
            (
                json.dumps(order_items),
                total,
                session['user_id']
            )
        )

        conn.commit()

        return jsonify({
            "success": True,
            "message": "Order placed successfully!"
        })

    finally:
        conn.close()


# Customer Order History
@app.route('/orders')
def order_history():

    if 'user_id' not in session:
        flash("Please log in to view your orders.")
        return redirect(url_for('login'))

    conn = get_db_connection()

    orders = conn.execute(
        """
        SELECT * FROM orders
        WHERE user_id = ?
        ORDER BY id DESC
        """,
        (session['user_id'],)
    ).fetchall()

    conn.close()

    return render_template('orders.html', orders=orders)


# Run application
if __name__ == '__main__':
    create_database()
    app.run(debug=True)
