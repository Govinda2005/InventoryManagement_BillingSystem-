# src/customer.py
import csv
import datetime
import os
from products import list_products, update_stock, find_product
from billing import write_BillAsText, write_BillAsCSV

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
CUSTOMER_FILE = os.path.join(BASE_DIR, 'data', 'customers.csv')
SALES_LOG = os.path.join(BASE_DIR, 'data', 'sales_log.csv')

# register as customer
def register_customer():
    cid = input("Enter Customer ID: ").strip()
    name = input("Enter Name: ").strip()
    password = input("Enter Password: ").strip()

    with open(CUSTOMER_FILE, 'a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        if os.stat(CUSTOMER_FILE).st_size == 0:
            writer.writerow(['customer_id','name','password'])
        writer.writerow([cid, name, password])
    print("\successfully registered")

#log in as customer
def customer_login():
    #enter customer name
    cid = input("Enter Customer ID: ").strip()
    password = input("Enter Password: ").strip()
    with open(CUSTOMER_FILE, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row['customer_id'] == cid and row['password'] == password:
                print("\n Logged in customer. Welcome,", row['name'])
                return cid
    print("\n Invalid credentials. plz enter correct details")
    return None


# view cart function
def display_cart(cart):
    """Display cart items in tabular format."""
    if not cart:
        print("\n Your cart is empty.")
        return
    print("\n  Your Cart:")
    print("-" * 30)
    print(f"{'Product ID':<12}{'Name':<20}{'Qty':<10}{'Price':<10}{'Subtotal':<10}")
    print("-" * 32)
    for item in cart:
        subtotal = float(item['price']) * item['qty']
        print(f"{item['product_id']:<12}{item['name']:<20}{item['qty']:<10}{item['price']:<10}{subtotal:<10}")
    print("-" * 32)
    total = sum(float(it['price']) * it['qty'] for it in cart)
    print(f"{'Total':<12}{'':<20}{'':<10}{'':<10}{total:<10}")
    print("-" * 32)


# viewing the menu 
def customer_menu(cid):
    cart = []
    while True:
        print("\n1) View Products\n2) Add to Cart\n3) Update Cart\n4) Remove Item\n5) View Cart\n6) Checkout\n7) Exit")
        ch = input("Choose: ")

        if ch == '1':
            for p in list_products():
                print(p)

        elif ch == '2':
            pid = input("Enter product ID to add: ")
            qty = int(input("Enter quantity: "))
            product = find_product(pid)
            if not product:
                print(" no product found.")
            elif int(product['stock']) < qty:
                print(" low stock product.")
            else:
                # If item already exists in cart, update qty
                for it in cart:
                    if it['product_id'] == pid:
                        it['qty'] += qty
                        break
                else:
                    cart.append({'product_id': pid, 'name': product['name'], 'price': product['price'], 'qty': qty})
                print("Added to cart.")

        elif ch == '3':
            pid = input("Enter product ID to update quantity: ")
            for item in cart:
                if item['product_id'] == pid:
                    item['qty'] = int(input("Enter new quantity: "))
                    print(" Updated.")
                    break
            else:
                print("Item not found in cart.")

        elif ch == '4':
            pid = input("Enter product ID to remove: ")
            new_cart = [it for it in cart if it['product_id'] != pid]
            if len(new_cart) < len(cart):
                cart = new_cart
                print("Removed successfully.")
            else:
                print("Item not found in cart.")

        elif ch == '5':
            display_cart(cart)

        elif ch == '6':
            if not cart:
                print("\nYou cannot checkout because your cart is empty.")
            else:
                display_cart(cart)
                checkout(cid, cart)
                cart.clear()  # clear cart after successful checkout
            break

        elif ch == '7':
            break


# billing logic
def checkout(cid, cart):
    #if cart is empty
    if not cart:
        print(" Cart is empty.")
        return

    total = sum(float(it['price']) * it['qty'] for it in cart)
    order_id = f"ORD{int(datetime.datetime.now().timestamp())}"
    print(f"\n🧾 Generating Bill for {order_id} ...")

    # Display bill in console
    print("\n===== BILL SUMMARY =====")
    print(f"Order ID: {order_id}")
    print(f"Customer ID: {cid}")
    print(f"Date: {datetime.date.today()}")
    print("-" * 40)
    print(f"{'Product':<20}{'Qty':<10}{'Price':<10}{'Subtotal':<10}")
    print("-" * 40)
    for it in cart:
        subtotal = float(it['price']) * it['qty']
        print(f"{it['name']:<20}{it['qty']:<10}{it['price']:<10}{subtotal:<10}")
    print("-" * 40)
    print(f"{'Total':<20}{'':<10}{'':<10}{total:<10}")
    print("=" * 40)

    # Save bill files in the folder 
    write_BillAsText(order_id, cart, total, user_id=cid)
    write_BillAsCSV(order_id, cart, total, user_id=cid)
    # Log sale 
    os.makedirs('data', exist_ok=True)
    file_exists = os.path.exists(SALES_LOG)
    with open(SALES_LOG, 'a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(['order_id', 'customer_id', 'date', 'total'])
        writer.writerow([order_id, cid, datetime.date.today().strftime("%Y-%m-%d"), total])

    # Update stock and render on console
    for it in cart:
        product = find_product(it['product_id'])
        new_stock = int(product['stock']) - it['qty']
        update_stock(it['product_id'], new_stock)

    print(f"Bill saved. Total: ₹{total}")
