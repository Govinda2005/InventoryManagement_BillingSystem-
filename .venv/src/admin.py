# src/admin.py
import csv
import datetime
import os
from src.products import list_products, find_product, update_stock, add_product
from src.billing import save_bill_csv, save_bill_txt

ADMIN_FILE = '../data/admin.csv'
SALES_LOG = '../data/sales_log.csv'
PRODUCTS_FILE = '../data/products.csv'

def admin_login():
    username = input("Enter admin username: ").strip()
    password = input("Enter admin password: ").strip()
    with open(ADMIN_FILE, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row['username'] == username and row['password'] == password:
                print("\n✅ Login successful. Welcome Admin!")
                return True
    print("\n❌ Invalid admin credentials.")
    return False


# ---------------- Product Management ---------------- #
def search_product():
    pid = input("Enter Product ID to search: ").strip()
    product = find_product(pid)
    if product:
        print("\nProduct Found:")
        print(product)
    else:
        print("\n❌ Product not found.")


def update_product():
    pid = input("Enter Product ID to update: ").strip()
    product = find_product(pid)
    if not product:
        print("Product not found.")
        return
    print(f"Current product details: {product}")
    name = input("Enter new name (leave blank to keep same): ") or product['name']
    price = input("Enter new price (leave blank to keep same): ") or product['price']
    stock = input("Enter new stock (leave blank to keep same): ") or product['stock']

    rows = list_products()
    for r in rows:
        if r['product_id'] == pid:
            r['name'], r['price'], r['stock'] = name, price, stock
    with open(PRODUCTS_FILE, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=['product_id','name','price','stock'])
        writer.writeheader()
        writer.writerows(rows)
    print("\n✅ Product updated successfully.")


def delete_product():
    pid = input("Enter Product ID to delete: ").strip()
    rows = list_products()
    new_rows = [r for r in rows if r['product_id'] != pid]
    if len(new_rows) == len(rows):
        print("❌ Product not found.")
        return
    with open(PRODUCTS_FILE, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=['product_id','name','price','stock'])
        writer.writeheader()
        writer.writerows(new_rows)
    print("\n✅ Product deleted successfully.")


# ---------------- Sales Reports ---------------- #
def sales_report():
    print("\n1) Report for Current Day")
    print("2) Report for Custom Date Range")
    ch = input("Choose: ")
    today = datetime.date.today()

    start_date, end_date = None, None
    if ch == '1':
        start_date = end_date = today
    elif ch == '2':
        start_date = datetime.datetime.strptime(input("Enter start date (YYYY-MM-DD): "), "%Y-%m-%d").date()
        end_date = datetime.datetime.strptime(input("Enter end date (YYYY-MM-DD): "), "%Y-%m-%d").date()
    else:
        print("Invalid choice.")
        return

    total_sales = 0
    print(f"\n📊 Sales Report ({start_date} to {end_date}):\n")
    with open(SALES_LOG, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            sale_date = datetime.datetime.strptime(row['date'], "%Y-%m-%d").date()
            if start_date <= sale_date <= end_date:
                print(row)
                total_sales += float(row['total'])
    print(f"\n💰 Total Sales: {total_sales}")
