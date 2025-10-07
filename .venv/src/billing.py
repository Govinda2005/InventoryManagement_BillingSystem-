# src/billing.py
import csv, datetime, os

def save_bill_txt(order_id, items, total, folder='bills'):
    os.makedirs(folder, exist_ok=True)
    fname = f"{folder}/bill_{order_id}_{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}.txt"
    with open(fname, 'w', encoding='utf-8') as f:
        f.write(f"Order ID: {order_id}\nDate: {datetime.datetime.now()}\n\n")
        f.write("Item\tQty\tPrice\tSubtotal\n")
        for it in items:
            f.write(f"{it['name']}\t{it['qty']}\t{it['price']}\t{it['qty']*float(it['price'])}\n")
        f.write(f"\nTotal: {total}\n")
    return fname

def save_bill_csv(order_id, items, total, folder='bills'):
    os.makedirs(folder, exist_ok=True)
    fname = f"{folder}/bill_{order_id}_{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}.csv"
    with open(fname, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['order_id','item_name','qty','price','subtotal'])
        for it in items:
            writer.writerow([order_id, it['name'], it['qty'], it['price'], it['qty']*float(it['price'])])
        writer.writerow([])
        writer.writerow(['', '', '', 'TOTAL', total])
    return fname
