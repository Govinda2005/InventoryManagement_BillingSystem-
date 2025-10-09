# src/main.py
from src.admin import admin_login, search_product, update_product, delete_product, sales_report
#from src.customer import register_customer, customer_login, customer_menu
def main_menu():
    while True:
        print("\n Hello , Welcome to the Inventory  Management system through console")
        login = input("\n Are you want to \n 1) login as admin \n 2) signup or login as User \n")
        if login == '1':
            if ():
                while True:
                    print("\n 1) Manage Products 2) Reports 3) Exit")
                    ch = input("Choose: ")
                    if ch == '1':
                        print("1) Search 2) Update 3) Delete")
                        sub = input("Choose: ")
                        if sub == '1':
                            search_product()
                        elif sub == '2':
                            update_product()
                        elif sub == '3':
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
