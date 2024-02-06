"""
Sales Calculator
by A01330566

This program calculates the total cost for all sales on a json file
"""

import sys
import json
import time

CATALOGUE_JSON = {}


class CheckElement:
    """
    This class encloses all the information about an item
    from the catalogue.
    """
    def __init__(self, prod_name, cost, qty=0):
        self.prod_name = prod_name
        self.unit_cost = cost
        self.qty = qty
        self.total_to_pay = qty * cost

    def add_elements(self, new_qty):
        """
        This function adds the specified number of items
        to the existent list. Next it calculates the new
        total to pay for all of the desired items
        """
        self.qty += new_qty
        self.total_to_pay += new_qty * self.unit_cost

    def get_unit_cost(self):
        """
        This function returns the unit cost property value
        """
        return self.unit_cost

    def get_product_name(self):
        """
        This function returns the product's name property value
        """
        return self.prod_name

    def get_total_qty(self):
        """
        This function returns the total number of items desired
        """
        return self.qty

    def get_total_to_pay(self):
        """
        This function returns the total to pay for the desired
        number of items
        """
        return self.total_to_pay


def read_json_file(file_path):
    """
    This function reads the json file and handles errors such as:
    - File not existent
    - Json Decode Error
    - Unicode Decode Error
    """
    json_file = {}
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            json_file = json.load(file)
    except FileNotFoundError:
        print("File not found:", file_path)
        sys.exit(1)
    except json.JSONDecodeError:
        print("Invalid format in catalogue json file")
        sys.exit(1)
    except UnicodeDecodeError:
        print("File is not encoded in UTF-8. Verify and retry")
        sys.exit(1)

    return json_file


def get_price(store_item):
    """
    Returns the price of a specific item in the catalogue
    in case it is not found, it returns a price of $0
    """
    for item in CATALOGUE_JSON:
        if item.get("title") == store_item:
            if item.get("price") is not None:
                return item.get("price")
            else:
                print(f"Price Not Found for {store_item} in catalogue")
                return 0

    print(f"Item '{store_item}' not found in catalogue")
    return 0


def get_checkout(check_file):
    """
    This function generates the check from the selected
    products in the Sales json, calculating the total
    number of items per product, total to pay per product,
    and total to pay for all products.
    """
    check_file = read_json_file(check_file)
    dic_check = {}

    for item in check_file:
        product = item.get("Product")
        qty = item.get("Quantity")
        cost = get_price(product)

        if product in dic_check:
            dic_check[product].add_elements(qty)
        else:
            dic_check[product] = CheckElement(product, cost, qty)

    return dic_check


def print_checkout(dic_checkout):
    """
    This function is a complementary function for
    get_checkout(). This function prints in a human
    readable fashion the info generated.
    """
    total = 0
    check_out_output = []
    for item in dic_checkout.values():
        line_out = (f"{item.get_product_name()} = {item.get_total_qty()}" +
                    f" piece(s) x ${item.get_unit_cost()} =  " +
                    f"${round(item.get_total_to_pay(),2)}")
        print(line_out)
        check_out_output.append(line_out + "\n")
        total += item.get_total_to_pay()
    line_out = "="*30
    check_out_output.append(line_out + "\n")
    print(line_out)

    line_out = f"Total: ${round(total,2)}"
    check_out_output.append(line_out + "\n")
    print(line_out)

    return check_out_output


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python computeSales.py Catalogue.json Check.json")
        sys.exit(1)

    start_time = time.time()
    catalogue_path = sys.argv[1]
    check_path = sys.argv[2]

    CATALOGUE_JSON = read_json_file(catalogue_path)
    check_out = get_checkout(check_path)
    checkout_text = print_checkout(check_out)

    with open("SalesResults.txt", 'w', encoding="UTF-8") as results_file:
        results_file.writelines(checkout_text)
        elapsed_time = time.time() - start_time
        print(f"Time elapsed:{elapsed_time} seconds")
        results_file.write(f"Time elapsed:{elapsed_time} seconds")
