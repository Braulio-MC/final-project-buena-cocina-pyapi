import re
from core.constants import CATEGORY_SYNONYMS, VALID_WORDS
from core.firebaseHelper import db
from core.constants import table_stores, EMBEDDINGS_MODEL, CATEGORY_DESCRIPTIONS, open_now_examples, opening_hours_examples, store_examples, product_examples
from core.synonyms import get_synonyms
from nltk.stem import WordNetLemmatizer
from fuzzywuzzy import process
from datetime import datetime
import unicodedata
from sentence_transformers import  SentenceTransformer
import numpy as np


lemmatizer = WordNetLemmatizer()
model = SentenceTransformer(EMBEDDINGS_MODEL)

# Convertir ejemplos a embeddings
store_embeddings_questions = model.encode(store_examples, normalize_embeddings=True)
product_embeddings_questions = model.encode(product_examples, normalize_embeddings=True)


# Embeddings de preguntas sobre horas
open_now_embeddings = model.encode(open_now_examples, normalize_embeddings=True)
opening_hours_embeddings = model.encode(opening_hours_examples, normalize_embeddings=True)


def normalize_text(text):
    """ Elimina tildes y convierte a minúsculas """
    text = text.lower()
    text = re.sub(r"[^\w\s]", "", text)  # Eliminar puntuación
    text = unicodedata.normalize("NFD", text).encode("ascii", "ignore").decode("utf-8")
    return text


def detect_category(query):
    """Detecta la categoría más relevante, considerando sinónimos y embeddings."""

    query_embedding = model.encode(query, normalize_embeddings=True)

    # Crear embeddings de categorías con sus sinónimos
    category_embeddings = {}
    for cat, desc in CATEGORY_DESCRIPTIONS.items():
        expanded_desc = desc + " " + " ".join(CATEGORY_SYNONYMS.get(cat, []))
        category_embeddings[cat] = model.encode(expanded_desc, normalize_embeddings=True)

    # Calcular similitudes
    similarities = {
        category: np.dot(query_embedding, cat_emb)
        for category, cat_emb in category_embeddings.items()
    }

    best_category = max(similarities, key=similarities.get)
    best_similarity = similarities[best_category]

    # Ajustar umbral dinámico
    avg_similarity = np.mean(list(similarities.values()))
    std_similarity = np.std(list(similarities.values()))
    dynamic_threshold = avg_similarity + (0.5 * std_similarity)

    print(f" Similitudes: {similarities}")
    print(f" Mejor categoría: {best_category} (Similitud: {best_similarity})")
    print(f" Umbral dinámico: {dynamic_threshold}")

    return best_category if best_similarity > dynamic_threshold else None


def extract_filters(query: str):
    min_price, max_price, category, store = None, None, None, None
    query = normalize_text(query)

    # Buscar precios
    price_match = re.search(r"(\d+(?:\.\d{1,2})?)\s*(?:-|a|hasta|por menos de)?\s*(\d+(?:\.\d{1,2})?)?", query)
    if price_match:
        min_price = float(price_match.group(1))
        max_price = float(price_match.group(2)) if price_match.group(2) else None

    #  Intentar detectar con embeddings
    category = detect_category(query)
    print(category)

    #  Si embeddings no encontró categoría, usar sinónimos
    if not category:
        for category_name, synonyms in CATEGORY_SYNONYMS.items():
            if any(syn in query.lower() for syn in synonyms):
                category = category_name
                break


    # Buscar nombres de tiendas
    store_docs = db.collection(table_stores).stream()
    store_names = {doc.id: doc.to_dict().get("name", "").lower() for doc in store_docs}
    for store_id, store_name in store_names.items():
        if store_name in query:
            store = store_name
            break

    print(f"✅ Consulta: {query}")
    print(f"Categoría detectada: {category}")
    return min_price, max_price, category, store


def cumple_filtros(product, min_price, max_price, category, store):
    """ Verifica si el producto cumple con los filtros de precio, categoría y tienda. """

    # Verificar precio
    if min_price is not None and product.get("price", float("inf")) < min_price:
        return False
    if max_price is not None and product.get("price", float("-inf")) > max_price:
        return False

    # Verificar categoría usando sinónimos
    if category and "category" in product:
        product_categories = product["category"]
        if isinstance(product_categories, str):
            product_categories = [product_categories]  # Convertir a lista si es string

        # Obtener la lista de categorías equivalentes (incluyendo la original)
        categorias_validas = CATEGORY_SYNONYMS.get(category.lower(), []) + [category.lower()]

        # Verificar si alguna categoría del producto coincide con la lista
        if not any(c.lower() in categorias_validas for c in product_categories):
            return False

    # Verificar tienda
    if store and product.get("store", {}).get("name", "").lower() != store.lower():
        return False

    return True


# Esto va ayudar a ser mas flexible con preguntas largas y preciso con preguntas mas directas
def dynamic_threshold(query: str):
    words = len(query.split())
    if words <= 2:
        return 0.05  # Reducido de 0.1 a 0.05
    elif words <= 5:
        return 0.08  # Reducido de 0.2 a 0.08
    else:
        return 0.1  # Reducido de 0.3 a 0.1


def detect_preference(query: str):
    if "barato" in query or "más barato" or "por menos" or "barata" or "economica" in query:
        return "price", "asc"
    if "caro" in query or "más caro" in query:
        return "price", "desc"
    if "mejor calificado" in query or "mejor valorado" in query:
        return "rating", "desc"
    return None, None


def detect_query_type(query: str):
    """Clasifica la consulta como 'store', 'product' o 'unknown' usando embeddings."""
    query_embedding = model.encode(query, normalize_embeddings=True)

    # Calcular similitud con ejemplos de tiendas y productos
    store_similarities = np.dot(store_embeddings_questions, query_embedding)
    product_similarities = np.dot(product_embeddings_questions, query_embedding)

    # Obtener la mejor similitud de cada categoría
    best_store_sim = max(store_similarities)
    best_product_sim = max(product_similarities)

    # Ajustar umbral de confianza
    threshold = 0.6
    if best_store_sim > threshold and best_store_sim > best_product_sim:
        return "store"
    elif best_product_sim > threshold:
        return "product"

    return "unknown"


def correct_word(word: str) -> str:
    """ Corrige la palabra si encuentra una similar en las palabras válidas. """
    suggestion = process.extractOne(word, VALID_WORDS)
    if suggestion and suggestion[1] > 70:  # Si el porcentaje de similitud es alto (ajustable)
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

def isOpenNow(store_data):
    """
    Verifica si la tienda está abierta en este momento basado en startTime y endTime.
    """
    if not store_data:
        return False

    start_time = store_data.get("startTime")
    end_time = store_data.get("endTime")

    if not start_time or not end_time:
        return False  # Si no tiene horarios definidos, asumimos que no está disponible

    # Obtener la hora actual en formato HH:MM
    now = datetime.now().strftime("%H:%M")

    return start_time <= now <= end_time


def detect_store_availability_query(query: str):
    """Clasifica la consulta en 'open_now', 'opening_hours' o None usando embeddings."""
    query_embedding = model.encode(query, normalize_embeddings=True)

    # Calculamos la similitud con cada categoría
    open_now_similarities = np.dot(open_now_embeddings, query_embedding)
    opening_hours_similarities = np.dot(opening_hours_embeddings, query_embedding)

    # Encontramos la mejor similitud para cada categoría
    best_open_now_sim = max(open_now_similarities)
    best_opening_hours_sim = max(opening_hours_similarities)

    # Ajustamos umbrales de confianza
    threshold = 0.65
    if best_open_now_sim > threshold and best_open_now_sim > best_opening_hours_sim:
        return "open_now"
    elif best_opening_hours_sim > threshold:
        return "opening_hours"

    return None