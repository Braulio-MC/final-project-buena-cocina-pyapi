from data.service.productBotService import get_all_products
from core.firebaseHelper import db


def fetch_products():
    return get_all_products()


def get_products_by_ids(product_ids: list):
    products = []
    for product_id in product_ids:
        doc = db.collection("productos").document(product_id).get()
        if doc.exists:
            product = doc.to_dict()
            product["id"] = doc.id  # Agregar el ID al diccionario si es necesario
            products.append(product)
    return products