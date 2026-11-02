
from flask import Flask, render_template, request, jsonify
import sqlite3
import json

app = Flask(__name__)

def create_database():
    conn = sqlite3.connect("store.db")

    conn.execute("""
        CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            items TEXT,
            total REAL
        )
    """)

    conn.commit()
    conn.close()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/place_order', methods=['POST'])
def place_order():
    data = request.get_json()
    cart = data.get('cart', [])

    if not cart:
        return jsonify({
            "success": False,
            "message": "Your cart is empty!"
        })

    total = sum(item['price'] for item in cart)

    conn = sqlite3.connect("store.db")

    conn.execute(
        "INSERT INTO orders (items, total) VALUES (?, ?)",
        (json.dumps(cart), total)
    )

    conn.commit()
    conn.close()

    return jsonify({
        "success": True,
        "message": "Order placed successfully!"
    })

@app.route('/orders')
def order_history():
    conn = sqlite3.connect("store.db")
    orders = conn.execute(
        "SELECT * FROM orders ORDER BY id DESC"
    ).fetchall()
    conn.close()

    return render_template('orders.html', orders=orders)

if __name__ == '__main__':
    create_database()
    app.run(debug=True)
