
import csv
import datetime
import os
import random

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
BILLS_DIR = os.path.join(BASE_DIR, 'bills')
# generating the random bill id
def makeBill_Id():
    """Makes a unique bill ID by mixing timestamp and some random chars."""
   
    ts = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    rand_part = ''.join(random.choices('ABCDEF0123456789', k=4)) 
    return f"INV-{ts}-{rand_part}" 

# writing the bill contents
def write_BillAsText(order_num, items_list, final_total, output_dir='../bills', user_id=None):
    """Saves the bill as a messy but functional .txt invoice."""
    
    # setting the date
    os.makedirs(output_dir, exist_ok=True)
    now = datetime.datetime.now()
    

    date_part = now.strftime("%Y%m%d") 
    time_part = now.strftime("%H%M")
    #getting the bill id from make bill id method
    bill_id = makeBill_Id()
    

    user_key = user_id if user_id else "Guest"
    file_name = f"{output_dir}/bill_{user_key}_{date_part}_{time_part}.txt"
#opening the file
    with open(file_name, 'w', encoding='utf-8') as f:
        # writing the bill contents
        f.write("###########################################\n")
        f.write("      INVENTORY & CASH REGISTER RECEIPT    \n") 
        f.write("###########################################\n")
        
        # billids,  orders
        f.write(f"Bill ID       : {bill_id}\n")
        f.write(f"Customer      : {user_key}\n")
        f.write(f"Order Ref     : {order_num}\n")
        f.write(f"Date/Time     : {now.strftime('%Y-%m-%d %I:%M %p')}\n")
        f.write("-------------------------------------------\n")

        # printing the table
        f.write("Item \t\t Qty \t Price \t\t Subtotal\n") 
        f.write("-------------------------------------------\n")

        for item in items_list:
        
            sub_total = item['qty'] * float(item['price'])
            f.write(f"{item['name'][:15]}\t {item['qty']} \t {item['price']} \t {sub_total:.2f}\n")

        f.write("===========================================\n")
       
        f.write(f"TOTAL AMOUNT DUE:\t\t\t {final_total:.2f}\n") 
        f.write("===========================================\n")
        f.write(" \t\t Thank You, Come Again! \t\t\n") 
    print(f"\nBill created and saved to disk: {file_name}")

    return file_name

#saving the bill as csv 
def write_BillAsCSV(order_num, items_list, final_total, output_dir='../bills', user_id=None): # Renamed function
    """Saves bill details to a CSV file for back office records."""
    os.makedirs(output_dir, exist_ok=True)
    now = datetime.datetime.now()
    
    date_part = now.strftime("%Y%m%d")
    time_part = now.strftime("%H%M")
    bill_id = makeBill_Id()

    user_key = user_id if user_id else "Guest"
    file_name = f"{output_dir}/log_{user_key}_{date_part}_{time_part}.csv" 
#opening the file
    with open(file_name, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
    
        writer.writerow(["BILL_ID", bill_id]) 
        writer.writerow(["Customer_ID", user_key])
        writer.writerow(["Order Number:", order_num])
        writer.writerow(["Timestamp", now.strftime("%Y-%m-%d %H:%M:%S")])
        writer.writerow([])
        

        writer.writerow(['Item Name', 'Qty', 'Unit Price', 'Line Total']) 
        for item in items_list:
            line_total = item['qty'] * float(item['price'])
            writer.writerow([item['name'], item['qty'], item['price'], line_total])
            
        writer.writerow([])
        writer.writerow(['', '', 'FINAL TOTAL', final_total])

    print(f"\nCSV sales log saved successfully: {file_name}")

    return file_name
