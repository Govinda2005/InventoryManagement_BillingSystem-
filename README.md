# 🏪 Inventory Management & Billing System – Python Console App

## 📘 Overview
This **console-based Python application** manages product inventory, customer orders, and billing.  
It provides separate menus for **Admin** and **Customer** users to manage products, place orders, and generate reports — all stored in CSV files without any external frameworks.

---

## 🎯 Objectives
- Manage products (add, update, delete, search)
- Register and authenticate customers
- Process orders and update stock automatically
- Generate bills in `.txt` and `.csv`
- Produce daily sales and low-stock reports
- Use Python standard libraries only (`csv`, `os`, `datetime`)

---

## 🧩 Features

### 👨‍💼 Admin Features
| Function | Description |
|-----------|--------------|
| **Login System** | Verifies admin credentials from `data/admin.csv` |
| **Product Management** | Add, view, search, update, and delete products |
| **Low Stock Report** | Lists and saves items with stock below threshold |
| **Sales Report** | Displays total sales for a date or range, exports to CSV |

### 👤 Customer Features
| Function | Description |
|-----------|--------------|
| **Registration & Login** | New customer registration and authentication |
| **View Products** | Browse available items |
| **Cart Management** | Add, update, or remove items in the shopping cart |
| **Checkout & Billing** | Generate detailed bill saved in `.txt` and `.csv` |
| **Stock Auto-Update** | Decreases inventory stock after checkout |

---

## 🗂️ Project Structure

```text
InventoryManagement_BillingSystem/
│
├── src/
│   ├── main.py             # Entry point (menu-based interface)
│   ├── admin.py            # Admin login & report management
│   ├── customer.py         # Customer registration & checkout flow
│   ├── billing.py          # Bill generation (.txt / .csv)
│   ├── products.py         # Product CRUD operations
│   ├── storage.py          # CSV read/write helpers
│   └── __init__.py
│
├── data/
│   ├── admin.csv           # Admin credentials
│   ├── customers.csv       # Customer info
│   ├── products.csv        # Product inventory
│   └── sales_log.csv       # Sales history
│
├── bills/                  # Auto-generated bill files
├── reports/                # Auto-generated reports
├── docs/screenshots/       # Terminal screenshots
├── README.md               # Documentation (this file)
└── presentation.pptx       # Project presentation (optional)
```

---

## ⚙️ Setup Instructions

### 🧩 1. Prerequisites
- **Python Version:** 3.8 or above  
- **No external libraries** required — uses only:
  - `csv` – for file handling  
  - `datetime` – for timestamps  
  - `os` – for file operations

---

### ▶️ 2. How to Run the Application
1. Open the terminal in your project folder.  
2. Navigate to the `src` directory:
   ```bash
   cd InventoryManagement_BillingSystem/src
   ```
3. Run the main Python file:
   ```bash
   python main.py
   ```

---

### 🔐 3. Default Admin Login
Before running the application, make sure your file `data/admin.csv` contains at least one admin account:

```csv
username,password
admin,admin123
```

---

## 💻 How the System Works

### 🧮 Admin Flow
1. Login using admin credentials.  
2. Perform product operations: add, update, delete, or search.  
3. Generate sales and low-stock reports.  
4. Reports are automatically saved under the `reports/` folder.

### 🛍️ Customer Flow
1. Register a new account or login as an existing customer.  
2. Browse available products from inventory.  
3. Add, update, or remove items in your cart.  
4. Checkout to:  
   - Generate bills (saved as `.txt` and `.csv` files)  
   - Update stock automatically in `products.csv`  
   - Log sales into `sales_log.csv`

---

## 📊 Example Data Files

### `products.csv`
```csv
product_id,name,price,stock
P001,Notebook,30.00,50
P002,Pen,5.00,200
P003,Stapler,120.00,10
P004,Envelope Pack,25.50,5
```

### `sales_log.csv`
```csv
order_id,customer_id,date,total
ORD1001,C001,2025-10-20,250.00
```

---

## 🧾 Sample Bill Output (Console)
```
===== BILL SUMMARY =====
Order ID: ORD1729580098
Customer ID: C001
Date: 2025-10-20
------------------------------------------------------------
Product          Qty     Price     Subtotal
------------------------------------------------------------
Pen              10      5.0       50.0
Notebook         2       30.0      60.0
------------------------------------------------------------
Total                                110.0
============================================================
✅ Bill saved. Total: ₹110.0
```

---

## 📁 Auto-Generated Reports

After successful checkouts, the system automatically creates reports:

**Low Stock Report:**  
`reports/low_stock_report_YYYYMMDD_HHMMSS.csv`  

**Daily Sales Report:**  
`reports/report_YYYYMMDD_HHMMSS.csv`  

Each report includes:
- Product details  
- Date and time of generation  
- Total sales summary  

---

## 📸 Screenshots
You can store terminal screenshots inside the `docs/screenshots/` folder for documentation or your GitHub README:
- Admin Login Successful  
- Product List Display  
- Checkout Bill Generation  
- Low-Stock Report CSV  

---

## 🚀 Tech Stack
| Component | Technology Used |
|------------|------------------|
| **Language** | Python 3 |
| **Interface** | Console (CLI) |
| **Storage** | CSV files |
| **Libraries** | csv, datetime, os |
| **Platform** | Works offline on Windows / Linux / macOS |

---

## 📈 Future Enhancements
- Add discount and GST calculation.  
- Replace CSV with SQLite database for better scalability.  
- Create GUI using Tkinter or Flask.  
- Add password encryption for better security.  
- Role-based access (Admin / Staff / Customer).  

---

## 🧑‍💻 Author
**Govinda**  
🎓 *Inventory Management & Billing System (Python Console Project)*  
🔗 GitHub: [https://github.com/your-username](https://github.com/your-username)


---

## 🧠 System Flow Diagram

Below is the high-level flow of the console application showing **Admin** and **Customer** modules and their operations:

![System Flow Diagram](docs/screenshots/system_flow.png)
