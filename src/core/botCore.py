import re
from core.constants import CATEGORY_SYNONYMS, STORE_SYNONYMS, VALID_WORDS
from core.firebaseHelper import db
from core.constants import table_products
from core.synonyms import get_synonyms
from nltk.stem import WordNetLemmatizer
from fuzzywuzzy import process

lemmatizer = WordNetLemmatizer()

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
    product = db.collection(table_products).document(product_id).get().to_dict()

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


def detect_preference(query: str):
    if "barato" in query or "más barato" in query:
        return "price", "asc"
    if "caro" in query or "más caro" in query:
        return "price", "desc"
    if "mejor calificado" in query or "mejor valorado" in query:
        return "rating", "desc"
    return None, None

def detect_query_type(query: str):
    query = query.lower()
    store_keywords = ["restaurante", "tienda", "negocio", "dónde comer", "quien", "cafetería", "donde"]
    product_keywords = ["producto", "comida", "platillo", "hamburguesa", "pizza", "bebida", "postre", "cafe"]

    if any(word in query for word in store_keywords):
        return "store"
    elif any(word in query for word in product_keywords):
        return "product"
    return "unknown"


def correct_word(word: str) -> str:
    """ Corrige la palabra si encuentra una similar en las palabras válidas. """
    suggestion = process.extractOne(word, VALID_WORDS)
    if suggestion and suggestion[1] > 80:  # Si el porcentaje de similitud es alto (ajustable)
        return suggestion[0]
    return word


def expand_query(query: str):
    """ Expande la consulta con sinónimos y luego aplica lematización.
    """
    words = query.lower().split()
    expanded_query = []

    for word in words:
        # Palabras corregidas
        corrected_word = correct_word(word)
        expanded_query.append(corrected_word)

        # Agregamos sinonimos de categoria
        expanded_query.extend(CATEGORY_SYNONYMS.get(word, []))

        # Agregar sinonimos adicionales
        expanded_query.extend(get_synonyms(word))

    lemmatized_query = [lemmatizer.lemmatize(word) for word in expanded_query]

    return " ".join(set(lemmatized_query))
