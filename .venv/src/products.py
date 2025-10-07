# src/products.py
from src.storage import read_csv, write_csv

PRODUCTS_FILE = 'data/products.csv'
FIELDS = ['product_id','name','price','stock']

def list_products():
    return read_csv(PRODUCTS_FILE)

def find_product(pid):
    for p in list_products():
        if p['product_id'] == pid:
            return p
    return None

def add_product(product):
    rows = list_products()
    rows.append(product)
    write_csv(PRODUCTS_FILE, FIELDS, rows)

def update_stock(pid, new_stock):
    rows = list_products()
    for r in rows:
        if r['product_id'] == pid:
            r['stock'] = str(new_stock)
    write_csv(PRODUCTS_FILE, FIELDS, rows)
