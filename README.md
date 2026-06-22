Overview

StockFlow is a simple Inventory Management System built with Django and Django REST Framework (DRF). The project demonstrates REST API development, JWT authentication, role-based permissions, filtering, searching, ordering, pagination, and a basic web interface for authentication and navigation.

This project was developed as part of an internship to demonstrate backend development using Django REST Framework.

Features:

JWT Authentication
Role-Based Access Control
Product Management
Category Management
Supplier Management
Customer Management
Sales Management
Dashboard API
Filtering
Searching
Ordering
Pagination
Nested Serializers
Optimized database queries using select_related()
Simple Login/Logout Web Interface

Technologies Used:
Python
Django
Django REST Framework
SQLite
Simple JWT
django-filter

#API Features

Authentication:
JWT Login
JWT Refresh Token
Protected API Endpoints

Products:
Create Product
View Products
Update Product
Delete Product
Search Products
Filter Products
Order Products
Pagination
Categories
CRUD Operations

Suppliers:
CRUD Operations
Customers
CRUD Operations

Sales:
Record Sales
Track Sales History

Dashboard:

Provides summary information such as:

Total Products
Total Categories
Total Suppliers
Total Customers
Total Sales
Role-Based Permissions
Admin

The Django Superuser has full access to the system.

Admin Features:

Full access to all APIs
Create, Update, Delete Products
Manage Categories
Manage Suppliers
Manage Customers
Manage Sales
Manage Users
Access Django Admin Panel
View Dashboard

Manager:

Login Credentials:
Username: manager
Password: pass@123

Manager Features:

Login to the system
View Dashboard
Create Products
Update Products
Delete Products
Manage Categories
Manage Suppliers
Manage Customers
View Sales
Create Sales


Sales Staff:

Login Credentials
Username: sales
Password: pass@123

Sales Features:

Login to the system
View Dashboard
View Products
View Categories
View Suppliers
View Customers
Create Customers
Create Sales
Update Customer Information

Sales Staff cannot:

Delete Products
Delete Categories
Delete Suppliers
Manage Users
Access Django Admin Panel
Authentication

The project uses JWT Authentication.

Obtain an access token:

POST /api/token/

Refresh token:

POST /api/token/refresh/

Include the access token in the request header:

Authorization: Bearer <access_token>
Filtering

Example:

GET /api/products/?category=2
GET /api/products/?supplier=1
GET /api/products/?is_active=true
Searching

Example:

GET /api/products/?search=laptop

Searchable fields:

Product Name
SKU
Barcode
Ordering

Example:

GET /api/products/?ordering=selling_price
GET /api/products/?ordering=-selling_price
GET /api/products/?ordering=quantity
Pagination

Pagination is enabled using Django REST Framework's PageNumberPagination.

Example:

GET /api/products/?page=1
GET /api/products/?page=2

#Running the Project:

Clone the Repository:
git clone <repository-url>

Create Virtual Environment:
python -m venv venv

Activate Virtual Environment:
Windows
venv\Scripts\activate
Linux / macOS
source venv/bin/activate


Install Dependencies:
pip install -r requirements.txt
Apply Migrations
python manage.py migrate
Run the Development Server
python manage.py runserver


Project Structure:
StockFlow/
│
├── inventory/
├── templates/
├── static/
├── manage.py
├── requirements.txt
└── README.md


Future Improvements:
Product Image Uploads
Inventory Alerts
Sales Reports
Purchase Orders
Export Reports (PDF/Excel)
Responsive Frontend
Advanced Analytics Dashboard