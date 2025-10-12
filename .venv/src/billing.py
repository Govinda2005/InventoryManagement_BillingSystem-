# src/billing.py
import csv
import datetime
import os
import random

def generate_bill_id():
    """Generate a unique bill/invoice ID like INV202510121045AB12."""
    timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    rand_suffix = ''.join(random.choices('ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789', k=4))
    return f"INV{timestamp}{rand_suffix}"


def save_bill_txt(order_id, items, total, folder='bills', user_id=None):
    """Save bill in .txt format with proper invoice structure."""
    os.makedirs(folder, exist_ok=True)
    now = datetime.datetime.now()
    date_str = now.strftime("%d_%m_%Y")
    time_str = now.strftime("%H_%M")
    bill_id = generate_bill_id()

    # ✅ Filename: DD_MM_YYYY_userid_HH_MM.txt
    user_part = user_id if user_id else "unknown"
    fname = f"{folder}/bill_{date_str}_{user_part}_{time_str}.txt"

    with open(fname, 'w', encoding='utf-8') as f:
        f.write("=============================================\n")
        f.write("         INVENTORY MANAGEMENT SYSTEM         \n")
        f.write("=============================================\n")
        f.write(f"Bill ID     : {bill_id}\n")
        f.write(f"Customer ID : {user_part}\n")
        f.write(f"Order ID    : {order_id}\n")
        f.write(f"Date        : {now.strftime('%d-%m-%Y %H:%M:%S')}\n")
        f.write("---------------------------------------------\n")
        f.write(f"{'Item':<20}{'Qty':<10}{'Price':<10}{'Subtotal':<10}\n")
        f.write("---------------------------------------------\n")

        for it in items:
            subtotal = it['qty'] * float(it['price'])
            f.write(f"{it['name']:<20}{it['qty']:<10}{it['price']:<10}{subtotal:<10.2f}\n")

        f.write("---------------------------------------------\n")
        f.write(f"{'TOTAL':<20}{'':<10}{'':<10}{total:<10.2f}\n")
        f.write("=============================================\n")
        f.write("        THANK YOU FOR YOUR PURCHASE!         \n")
        f.write("=============================================\n")

    # ✅ Auto-display bill content in console
    print("\n🧾 Bill Generated Successfully!")
    print(f"📁 Saved as: {fname}")
    print("\n----------- BILL PREVIEW -----------")
    with open(fname, 'r', encoding='utf-8') as f:
        print(f.read())
    print("------------------------------------")

    return fname


def save_bill_csv(order_id, items, total, folder='bills', user_id=None):
    """Save bill in .csv format for record keeping."""
    os.makedirs(folder, exist_ok=True)
    now = datetime.datetime.now()
    date_str = now.strftime("%d_%m_%Y")
    time_str = now.strftime("%H_%M")
    bill_id = generate_bill_id()

    # ✅ Filename: DD_MM_YYYY_userid_HH_MM.csv
    user_part = user_id if user_id else "unknown"
    fname = f"{folder}/bill_{date_str}_{user_part}_{time_str}.csv"

    with open(fname, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(["Bill ID", bill_id])
        writer.writerow(["Customer ID", user_part])
        writer.writerow(["Order ID", order_id])
        writer.writerow(["Date", now.strftime("%d-%m-%Y %H:%M:%S")])
        writer.writerow([])
        writer.writerow(['Item Name', 'Quantity', 'Price', 'Subtotal'])
        for it in items:
            subtotal = it['qty'] * float(it['price'])
            writer.writerow([it['name'], it['qty'], it['price'], subtotal])
        writer.writerow([])
        writer.writerow(['', '', 'TOTAL', total])
        writer.writerow([])
        writer.writerow(['Thank you for your purchase!'])

    # ✅ Auto-display CSV confirmation
    print(f"\n✅ CSV version saved as: {fname}")

    return fname
