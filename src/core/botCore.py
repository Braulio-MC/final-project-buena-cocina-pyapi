import re
from core.constants import CATEGORY_SYNONYMS, STORE_SYNONYMS
from core.firebaseHelper import db

def extract_filters(query: str):
    min_price, max_price, category, store = None, None, None, None

    # Buscar precios
    price_match = re.search(r"(\d+(?:\.\d{1,2})?)\s*(?:-|a|hasta|y|por menos de)?\s*(\d+(?:\.\d{1,2})?)?", query)

    if price_match:
        min_price = float(price_match.group(1))
        if price_match.group(2):
            max_price = float(price_match.group(2))

    # Buscar categorías y tiendas
    for category_name, synonyms in CATEGORY_SYNONYMS.items():
        if any(syn in query for syn in synonyms):
            category = category_name

    for store_name, synonyms in STORE_SYNONYMS.items():
        if any(syn in query for syn in synonyms):
            store = store_name

    return min_price, max_price, category, store

def cumple_filtros(product_id, min_price, max_price, category, store):
    # Obtener el producto desde Firebase usando el ID
    product = db.collection("productos").document(product_id).get().to_dict()

    # Validar si existe el producto
    if not product:
        return False

    # Filtrar por precio
    price = float(product.get("price", 0))
    if min_price and price < min_price:
        return False
    if max_price and price > max_price:
        return False

    # Filtrar por categoría
    if category and category not in product.get("category", []):
        return False

    # Filtrar por tienda
    if store and product.get("store", "").lower() != store.lower():
        return False

    return True


# Esto va ayudar a ser mas flexible con preguntas largas y preciso con preguntas mas directas
def dynamic_threshold(query: str):
    words = len(query.split())
    return max(0.2, min(0.5, 0.5 - 0.05 * words))