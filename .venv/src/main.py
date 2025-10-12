# src/main.py
from src.admin import admin_login,view_products, search_product, update_product, delete_product, sales_report
from src.customer import register_customer, customer_login, customer_menu

def main_menu():
    while True:
        print("\n Hello , Welcome to the Inventory  Management system through console")
        login = input("\n Are you want to \n 1) login as admin \n 2) signup or login as User \n")
        if login == '1':
            if admin_login():
                while True:
                    print("\n 1) Manage Products 2) Reports 3) Exit")
                    ch = input("Choose option: ")
                    if ch == '1':
                        print("\n 1) View Products \n 2) Search Products \n 3) Update Products \n 4) Delete Products")
                        sub = input("Choose: ")
                        if sub == '1':
                            view_products()
                        elif sub == '2':
                            search_product()
                        elif sub == '3':
                            update_product()
                        elif sub == '4':
                            delete_product()
                    elif ch == '2':
                        sales_report()
                    else:
                        break

        elif login == '2':
            print("1) Register 2) Login")
            sub = input("Choose: ")
            if sub == '1':
                register_customer()
            elif sub == '2':
                cid = customer_login()
                if cid:
                    customer_menu(cid)

if __name__ == '__main__':
    main_menu()
