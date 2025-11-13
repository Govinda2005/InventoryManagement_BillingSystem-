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
    
    try: 
        with open(ADMIN_FILE, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row['username'] == username and row['password'] == password:
                    print(f"\nWelcome back, {username}!") 
                    return True
    except FileNotFoundError:
        print("Admin file not found. Check your paths.")
        return False
    print("invalid admin username or password.")
    return False

def view_products():
    products = list_products()
    if not products:
        print("No valid product found in the store.")
        return

    print("\n--- Current Inventory ---")
    
    print("ID\t\tNAME\t\t\t\t\tPRICE\t\tSTOCK") 
    print("-------------------------------------------------------------------------------------------------")
    
    for p in products:
        print(f"{p['product_id']}\t\t{p['name']}\t\t\t\t{p['price']}\t\t{p['stock']}")
        
    print("-------------------------")
    total = len(products)
    print(f"Total items in inventory: {total}")
    print("-------------------------")


def search_product():
    pid = input("Enter the Product ID: ").strip()
    product = find_product(pid)
    if product:
        print("\nFound the product:")
        print("----------------------------------------")
        print(f"Product ID: {product['product_id']}")
        print(f"Name: {product['name']}")
        print(f"Price: {product['price']}")
        print(f"Stock: {product['stock']}")
        print("-----------------------------------------")
    else:
        print("\nProduct not found, try again.")


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
    print("\nSuccessfully updated product.") 


def delete_product():
    pid = input("Enter Product ID to delete: ").strip()
    rows = list_products()
    new_rows = [r for r in rows if r['product_id'] != pid]
    
    if len(new_rows) == len(rows):
        print("Product ID not found in list.")
        return
        
    with open(PRODUCTS_FILE, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=['product_id', 'name', 'price', 'stock'])
        writer.writeheader()
        writer.writerows(new_rows)
        
    print("\nProduct removed from inventory.")

def low_stock_report(threshold=3):
    products = list_products()
    if not products:
        print("\nInventory is empty.")
        return

    low_stock_items = []
    for p in products:
        stock_val = p.get('stock', '').strip()
        try:
            stock_num = int(float(stock_val)) if stock_val != '' else 0
        except (ValueError, TypeError): 
            print(f"Something is wrong with the stock value for product: {p['product_id']}")
            continue

        if stock_num < threshold:
            low_stock_items.append(p) 

    if not low_stock_items:
        print(f"\nEverything is stocked up! (Threshold was {threshold}).")
        return

    print(f"\n--- Products Running Low (Stock < {threshold}) ---")
    print("ID\t\tNAME\t\tSTOCK")
    print("-------------------------------------")
    for item in low_stock_items:
        print(f"{item['product_id']}\t\t{item['name']}\t\t{item['stock']}")
        
    print(f"\nTotal items to order: {len(low_stock_items)}")

    os.makedirs(REPORTS_FOLDER, exist_ok=True)
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    report_file = os.path.join(REPORTS_FOLDER, f"low_stock_report_{timestamp}.csv")

    with open(report_file, 'w', newline='', encoding='utf-8') as rf:
        fieldnames = ['product_id', 'name', 'price', 'stock'] 
        writer = csv.DictWriter(rf, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(low_stock_items)
        
    print(f"\nSaved report to: {report_file}")


def sales_report():
    print("\n*** Sales Report Options ***") 
    print("1) Today's Report")
    print("2) Custom Dates")
    print("3) Low Stock Report (For inventory)")
    ch = input("Choose: ")
    today = datetime.date.today()

    if ch == '3':
        low_stock_report()
        return

    if ch == '1':
        start_date = end_date = today
    elif ch == '2':
        try:
            start_date = datetime.datetime.strptime(input("Start date (YYYY-MM-DD): "), "%Y-%m-%d").date()
            end_date = datetime.datetime.strptime(input("End date (YYYY-MM-DD): "), "%Y-%m-%d").date()
        except ValueError:
            print("Date input was wrong. Use YYYY-MM-DD.")
            return
    else:
        print("Not a valid choice.")
        return

    total_sales = 0.0
    report_data = []

    print(f"\nReport for {start_date} to {end_date}:\n")

    if not os.path.exists(SALES_LOG):
        print("No sales log file found.")
        return

    with open(SALES_LOG, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            date_str = row.get('date', '').strip()

            try:
                sale_date = datetime.datetime.strptime(date_str, "%Y-%m-%d").date()
            except ValueError:
                print(f"Couldn't read date in row: {row}")
                continue

            if start_date <= sale_date <= end_date:
                report_data.append(row)
                print(row)
                try:
                    total_sales += float(row.get('total', 0.0)) 
                except ValueError:
                    print(f"Total sales data is bad in row: {row}")

    print(f"\nTOTAL SALES: {total_sales}")

    if report_data:
        os.makedirs(REPORTS_FOLDER, exist_ok=True)
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        report_file = os.path.join(REPORTS_FOLDER, f"sales_report_{timestamp}.csv")

        with open(report_file, 'w', newline='', encoding='utf-8') as rf:
            fieldnames = report_data[0].keys()
            writer = csv.DictWriter(rf, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(report_data)

        print(f"\nReport saved: {report_file}")
    else:
        print("\nNo sales in this date range.")
