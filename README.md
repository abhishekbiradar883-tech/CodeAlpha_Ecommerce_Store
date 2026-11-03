# CodeAlpha E-Commerce Store

## Project Description
A simple e-commerce web application developed as part of the CodeAlpha Full Stack Development Internship. The application allows users to browse products, search for products, add items to a shopping cart, place orders and view their order history.

## Features
- User registration and login
- Secure password hashing
- Product listing with images
- Individual product details pages
- Product search functionality
- Add products to shopping cart
- Remove products from shopping cart
- Automatic total price calculation
- Checkout and order placement
- SQLite database integration
- User-specific order history
- Logout functionality

## Technologies Used
- Python
- Flask
- HTML5
- CSS3
- JavaScript
- SQLite
- Werkzeug

## Project Structure
```text
CodeAlpha_Ecommerce_Store/
│
├── app.py
├── requirements.txt
├── README.md
├── .gitignore
│
├── static/
│   ├── style.css
│   └── script.js
│
├── templates/
│   ├── index.html
│   ├── login.html
│   ├── register.html
│   ├── product.html
│   └── orders.html
│
└── venv/
```

## Installation and Setup

1. Clone the repository:

```bash
git clone https://github.com/abhishekbiradar883-tech/CodeAlpha_Ecommerce_Store.git
```

2. Open the project folder:

```bash
cd CodeAlpha_Ecommerce_Store
```

3. Create a virtual environment:

```bash
python -m venv venv
```

4. Activate the virtual environment on Windows:

```bash
venv\Scripts\activate
```

5. Install the required dependencies:

```bash
pip install -r requirements.txt
```

6. Run the application:

```bash
python app.py
```

7. Open your browser and visit:

http://127.0.0.1:5000/

## Database
The application uses SQLite to store:
- User information
- Product details
- Customer orders

## Developed For
CodeAlpha Full Stack Development Internship

## GitHub Repository
https://github.com/abhishekbiradar883-tech/CodeAlpha_Ecommerce_Store
