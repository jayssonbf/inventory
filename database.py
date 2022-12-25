"""database.py: Handles all database functionality"""
import sqlite3
import os.path

# File path to database
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(BASE_DIR, "products.db")


def get_product_from_batch(batch):
    """Returns the product with the provided batch number"""
    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()
    curr = cursor.execute(
        f"SELECT * FROM product where batch ='{batch}'",
    )
    products = []
    for row in curr:
        products.append(row)
    return products


def get_product_from_id(id):
    """Returns the product with the given ID"""
    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()
    curr = cursor.execute(
        f"SELECT * FROM product where product_id ='{id}'",
    )
    products = []
    for row in curr:
        products.append(row)
    return products


def get_product_by_type(type):
    """Returns all products with the given type"""
    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()
    curr = cursor.execute(
        f"SELECT * FROM product WHERE product_type ='{type}'",
    )
    products = []
    for row in curr:
        products.append(row)
    return products


def add_product(name, category, batch, description, quantity, status, date):
    """Add product to product table"""
    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()
    cursor.execute(
        f"INSERT INTO product(product_name, product_type, batch, description, qty, status, date)"
        f"VALUES('{name}', '{category}', {batch}, '{description}', {quantity}, '{status}', '{date}')")
    connection.commit()
    connection.close()
