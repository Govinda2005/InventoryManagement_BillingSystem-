import csv
import datetime
import os
from src.products import list_products, find_product, update_stock, add_product
from src.billing import save_bill_csv, save_bill_txt

ADMIN_FILE = '../data/admin.csv'
SALES_LOG = '../data/sales_log.csv'
PRODUCTS_FILE = '../data/products.csv'
REPORTS_FOLDER = '../reports' 

def admin_login():
    username = input("Enter username: ").strip()
    password = input("Enter password: ").strip()
    with open(ADMIN_FILE, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row['username'] == username and row['password'] == password:
                print("Hello govind, you logged in successfully")
                return True
    print("Invalid admin username and password.")
    return False


# ---------------- Helper Function: Display Products ---------------- #
def view_products():
    products = list_products()
    if not products:
        print(" No valid product found in the store.")
        return

    print("Product List:")
    print("----------------------------------------------------------------------------")
    print(f"{'Product ID':<20}{'Name':<50}{'Price':<10}{'Stock':<15}")
    print("-----------------------------------------------------------------------------")
    for p in products:
        print(f"{p['product_id']:<20}{p['name']:<50}{p['price']:<10}{p['stock']:<15}")
    print("----------------------------------------------")
    total = len(products)
    print(f"Products total is: {total}")
    print("-----------------------------------------------")


# ---------------- Product Management ---------------- #
def search_product():
    pid = input("Enter the Product ID: ").strip()
    product = find_product(pid)
    if product:
        print("\n Product Found:")
        print("----------------------------------------")
        print(f"{'Product ID':<20}: {product['product_id']}")
        print(f"{'Name':<50}: {product['name']}")
        print(f"{'Price':<10}: {product['price']}")
        print(f"{'Stock':<15}: {product['stock']}")
        print("-----------------------------------------")
    else:
        print("\n No Product found.")


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
        writer = csv.DictWriter(f, fieldnames=['product_id', 'name', 'price', 'stock'])
        writer.writeheader()
        writer.writerows(rows)
    print("\n Product updated successfully.")


def delete_product():
    pid = input("Enter Product ID to delete: ").strip()
    rows = list_products()
    new_rows = [r for r in rows if r['product_id'] != pid]
    if len(new_rows) == len(rows):
        print(" Product not found.")
        return
    with open(PRODUCTS_FILE, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=['product_id', 'name', 'price', 'stock'])
        writer.writeheader()
        writer.writerows(new_rows)
    print("\n Product deleted successfully.")


# ---------------- Low Stock Report ---------------- #
def low_stock_report(threshold=3):
    products = list_products()
    if not products:
        print("\n No products found in store.")
        return

    low_stock_items = []
    for p in products:
        stock_val = p.get('stock', '').strip()
        try:
            stock_num = int(float(stock_val)) if stock_val != '' else 0
        except (ValueError, TypeError):
            print(f"⚠️ Skipping product with invalid stock value: {p}")
            continue

        if stock_num < threshold:
            # ensure output uses consistent types/strings
            low_stock_items.append({
                'product_id': p.get('product_id', ''),
                'name': p.get('name', ''),
                'price': p.get('price', ''),
                'stock': str(stock_num)
            })

    if not low_stock_items:
        print(f"\n✅ No low-stock products found (threshold: {threshold}).")
        return

    # Print low-stock table
    print(f"\n📉 Low Stock Report (stock < {threshold}):")
    print("-" * 70)
    print(f"{'Product ID':<15}{'Name':<30}{'Price':<12}{'Stock':<8}")
    print("-" * 70)
    for item in low_stock_items:
        print(f"{item['product_id']:<15}{item['name']:<30}{item['price']:<12}{item['stock']:<8}")
    print("-" * 70)
    print(f"Total low-stock items: {len(low_stock_items)}")

    # Save report to CSV
    os.makedirs(REPORTS_FOLDER, exist_ok=True)
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    report_file = os.path.join(REPORTS_FOLDER, f"low_stock_report_{timestamp}.csv")

    with open(report_file, 'w', newline='', encoding='utf-8') as rf:
        fieldnames = ['product_id', 'name', 'price', 'stock']
        writer = csv.DictWriter(rf, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(low_stock_items)
        # add summary row
        writer.writerow({})
        writer.writerow({'product_id': 'TOTAL LOW STOCK', 'stock': len(low_stock_items)})

    print(f"\n📁 Low-stock report saved successfully at: {report_file}")


# ---------------- Sales Reports ---------------- #
def sales_report():
    print("\n1) Report for Current Day")
    print("2) Report for Custom Date Range")
    print("3) Low Stock Report")  # <-- new option added
    ch = input("Choose: ")
    today = datetime.date.today()

    if ch == '3':
        # call the low-stock report and return (keeps previous logic intact)
        low_stock_report()
        return

    if ch == '1':
        start_date = end_date = today
    elif ch == '2':
        start_date = datetime.datetime.strptime(input("Enter start date (YYYY-MM-DD): "), "%Y-%m-%d").date()
        end_date = datetime.datetime.strptime(input("Enter end date (YYYY-MM-DD): "), "%Y-%m-%d").date()
    else:
        print("Invalid choice.")
        return

    total_sales = 0
    report_data = []

    print(f"\n📊 Sales Report ({start_date} to {end_date}):\n")

    if not os.path.exists(SALES_LOG):
        print("❌ No sales data found.")
        return

    with open(SALES_LOG, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            date_str = row.get('date', '').strip()
            sale_date = None

            # ✅ Try both possible formats (for compatibility)
            for fmt in ("%Y-%m-%d", "%m/%d/%Y"):
                try:
                    sale_date = datetime.datetime.strptime(date_str, fmt).date()
                    break
                except ValueError:
                    continue

            if not sale_date:
                print(f"⚠️ Skipping row with invalid date: {row}")
                continue

            if start_date <= sale_date <= end_date:
                report_data.append(row)
                print(row)
                try:
                    total_sales += float(row['total'])
                except ValueError:
                    print(f"⚠️ Skipping invalid total in row: {row}")

    print(f"\n💰 Total Sales: {total_sales}")

    # ---------------- Save Report to CSV ---------------- #
    if report_data:
        os.makedirs(REPORTS_FOLDER, exist_ok=True)
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        report_file = os.path.join(REPORTS_FOLDER, f"report_{timestamp}.csv")

        with open(report_file, 'w', newline='', encoding='utf-8') as rf:
            fieldnames = report_data[0].keys()
            writer = csv.DictWriter(rf, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(report_data)

            # Add summary row
            writer.writerow({})
            writer.writerow({'order_id': 'TOTAL SALES', 'total': total_sales})

        print(f"\n📁 Report saved successfully at: {report_file}")
    else:
        print("\n⚠️ No sales found for the selected date range.")
