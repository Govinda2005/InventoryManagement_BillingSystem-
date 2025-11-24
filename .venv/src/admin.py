import csv
import datetime
import os
from products import list_products, find_product

BASE_DIR = os.path.dirname(__file__)
DATA_DIR = os.path.join(BASE_DIR, "data")
ADMIN_FILE = os.path.join(DATA_DIR, "admin.csv")
REPORTS_FOLDER = os.path.join(DATA_DIR, "reports")
SALES_LOG = os.path.join(DATA_DIR, "sales_log.csv")
PRODUCTS_FILE = os.path.join(DATA_DIR, "products.csv")

# implementation for admin login function
def loginAdmin():
    username = input("Enter username: ").strip()
    password = input("Enter password: ").strip()
    
    try: 
        with open(ADMIN_FILE, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            #checking usrname and password are valid?
            for row in reader:
                if row['username'] == username and row['password'] == password:
                    print(f"\n \t Welcome back, {username}!") 
                    return True
    except Exception as e:
        print("Invalid admin credentials")
        return False
    return False
#function to display the products
def displayProd_details():
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

#function for search among the products
def searchProd():
    #enter the products to be searched
    pid = input("Enter the Product ID: ").strip()
    #call find_product function
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

#function for updating a products
def updateProd():
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
    # updating the products
    for r in rows:
        if r['product_id'] == pid:
            r['name'], r['price'], r['stock'] = name, price, stock

    with open(PRODUCTS_FILE, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=['product_id', 'name', 'price', 'stock'])
        writer.writeheader()
        writer.writerows(rows)
    print("\nSuccessfully updated product.") 

#function for deleting a products
def deleteProd():
    pid = input("Enter Product ID to delete: ").strip()
    rows = list_products()
    new_rows = [r for r in rows if r['product_id'] != pid]
    
    if len(new_rows) == len(rows):
        print("Product ID not found in list.")
        return
    #deleting the products    
    with open(PRODUCTS_FILE, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=['product_id', 'name', 'price', 'stock'])
        writer.writeheader()
        writer.writerows(new_rows)
        
    print("\nProduct removed from inventory.")

#function for take low stock reports
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
     #printing the low stock products
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

#function for taking sales report
def sales_report():
    print("\n*** Sales Report Options ***") 
    print("1) current day report")
    print("2) Custom day range")
    print("3) Low Stock prod  Report ")
    ch = input("Choose: ")
    today = datetime.date.today()
     #based on the input taking the sales report
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
    #saving the report after modifying
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
