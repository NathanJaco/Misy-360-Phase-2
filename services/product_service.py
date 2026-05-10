import uuid


def get_low_stock_products(products):
    low_stock = []

    for product in products:
        if product["stock"] < 5:
            low_stock.append(product)

    return low_stock


def get_categories(products):
    categories = []

    for product in products:
        if product["category"] not in categories:
            categories.append(product["category"])

    return categories


def filter_products(products, search_product):
    filtered_products = []

    if search_product == "":
        for product in products:
            filtered_products.append(product)
    else:
        for product in products:
            if search_product.lower() in product["name"].lower():
                filtered_products.append(product)

    return filtered_products


def product_exists(products, product_name):
    clean_product_name = product_name.strip().lower()

    for product in products:
        if product["name"].strip().lower() == clean_product_name:
            return True

    return False


def add_product(products, name, category, price, stock):
    new_product = {
        "id": str(uuid.uuid4()),
        "name": name.strip(),
        "category": category,
        "price": price,
        "stock": stock
    }

    products.append(new_product)

    return new_product


def delete_product(products, product_id):
    new_list = []

    for product in products:
        if product["id"] != product_id:
            new_list.append(product)

    return new_list


def update_product(products, product_id, new_price, new_stock):
    for product in products:
        if product["id"] == product_id:
            product["price"] = new_price
            product["stock"] = new_stock
            return product

    return None