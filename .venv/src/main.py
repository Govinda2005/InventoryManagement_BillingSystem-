import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import admin
import customer

def main_menu():
    # asking whether he wants to login as admin or user
    while True:
        print("\n \n Hey Welcome to the  Inventory  Management system through console")
        user_Logged= input("\n if you are a  \n 1) Admin  \n 2)  User \n")
        # if user is an admin or customer
        if user_Logged == '1':
            # if user is a admin
            if admin.loginAdmin():
                while True:
                    print("\n 1) Manage Products  2) Reports 3) Exit ")
                    ch = input("Choose option: ")
                    if ch == '1':
                        print("\n 1) View Products  \n 2) Search Products \n 3) Update Products  \n 4) Delete Products")
                        sub = input("Choose: ")
                        if sub == '1':
                            admin.displayProd()
                        elif sub == '2':
                            admin.searchProd()
                        elif sub == '3':
                            admin.updateProd()
                        elif sub == '4':
                            admin.deleteProd()
                    elif ch == '2':
                        admin.sales_report()
                    else:
                        break
    #for user login activities
        elif user_Logged == '2':
            #if user is a cutomer
            print("1) Register a new user 2) Login as user")
            #asking user input
            usr_inp = input("your option : ")
            # if user is new user
            if usr_inp == '1':
                customer.register_customer()
                #already existing user
            if usr_inp == '2':
                cid = customer.customer_login()
                if cid:
                    customer.customer_menu(cid)

if __name__ == '__main__':
    main_menu()
