from app.db import get_products_collection
import json

def check_product():
    products_collection = get_products_collection()
    product = products_collection.find_one({"asin": "B0F99YG4WG"})
    if product:
        if "_id" in product:
            del product["_id"]
        print(json.dumps(product, indent=2))
    else:
        print("Product not found")

if __name__ == "__main__":
    check_product()
