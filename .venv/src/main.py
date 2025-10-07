# src/main.py
from products import list_products, add_product, find_product
def main_menu():
    while True:
        print("\n1) Manage products  2) New order  3) Reports  4) Exit")
        c = input("Choose: ").strip()
        if c == '1':
            pass
        elif c == '2':
            pass
        elif c == '3':
            pass
        else:
            break
if __name__ == '__main__':
    main_menu()
