# CodeAlpha E-Commerce Store

## 1. Project Overview

The **CodeAlpha E-Commerce Store** is a full-stack web application developed using Python Django, HTML, CSS, JavaScript, and SQLite.

The application allows users to browse products, view product details, add products to a shopping cart, register, log in, and place orders.

## 2. Technologies Used

- **Frontend:** HTML, CSS, JavaScript
- **Backend:** Python Django
- **Database:** SQLite
- **Development Environment:** Visual Studio Code
- **Version Control:** Git and GitHub

## 3. Main Features

1. **User Registration:** New users can create an account.
2. **User Login:** Registered users can securely log in.
3. **Product Listing:** Users can browse available products.
4. **Product Details:** Users can view product descriptions, images, and prices.
5. **Shopping Cart:** Users can add and remove products and view the total price.
6. **Order Processing:** Logged-in users can place orders.
7. **Order History:** Users can view their previous orders.
8. **Product Management:** Administrators can manage products through Django Admin.
9. **Product Search:** Users can search for products.

## 4. Project Structure

```text
CodeAlpha_Ecommerce_Store/
│
├── ecommerce_config/
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
│
├── store/
│   ├── migrations/
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   └── admin.py
│
├── templates/
│   ├── index.html
│   ├── login.html
│   ├── register.html
│   ├── product.html
│   └── orders.html
│
├── static/
│   ├── style.css
│   └── script.js
│
├── manage.py
├── requirements.txt
├── README.md
└── db.sqlite3
```

## 5. Installation and Setup

### Step 1: Clone the Repository

```bash
git clone https://github.com/abhishekbiradar883-tech/CodeAlpha_Ecommerce_Store.git
```

### Step 2: Open the Project Folder

```bash
cd CodeAlpha_Ecommerce_Store
```

### Step 3: Create a Virtual Environment

```bash
python -m venv venv
```

### Step 4: Activate the Virtual Environment

For Windows PowerShell:

```bash
venv\Scripts\Activate
```

### Step 5: Install Django

```bash
pip install Django==6.1.2
```

### Step 6: Apply Database Migrations

```bash
python manage.py migrate
```

### Step 7: Create an Admin Account

```bash
python manage.py createsuperuser
```

### Step 8: Run the Development Server

```bash
python manage.py runserver
```

Open the following URL in your browser:

http://127.0.0.1:8000/

## 6. Django Admin Panel

Administrators can manage products and view customer orders using the Django Admin Panel.

URL:

http://127.0.0.1:8000/admin/

Log in using the superuser credentials created during setup.

## 7. Database

The application uses SQLite to store:

- Product information
- User account information
- Customer order information

## 8. Future Enhancements

- Online payment gateway integration
- Product reviews and ratings
- Order tracking
- Wishlist functionality
- Improved security and deployment

## 9. Internship Project

**Internship Organization:** CodeAlpha

**Task:** Task 1 – Simple E-Commerce Store

**Project Type:** Full Stack Web Development

**Developer:** Abhishek Biradar

## 10. Conclusion

This project demonstrates the development of a full-stack e-commerce application using Django. It provides essential online shopping functionalities, including user authentication, product management, shopping cart operations, and order processing.
