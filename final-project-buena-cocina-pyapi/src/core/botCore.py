from difflib import get_close_matches
from core.constants import  open_now_examples, opening_hours_examples, store_examples, product_examples, questions_about_rankings, questions_about_description
from datetime import datetime
from core.botHelpers import *
import re

model = SentenceTransformer(EMBEDDINGS_MODEL)

# Generar embeddings para las consultas de productos y tiendas
store_embeddings_questions = model.encode(store_examples, normalize_embeddings=True)
product_embeddings_questions = model.encode(product_examples, normalize_embeddings=True)

# Embeddings de preguntas sobre tiendas
open_now_embeddings = model.encode(open_now_examples, normalize_embeddings=True)
opening_hours_embeddings = model.encode(opening_hours_examples, normalize_embeddings=True)
ranking_store_embeddings = model.encode(questions_about_rankings, normalize_embeddings=True)
description_store_embeddings = model.encode(questions_about_description, normalize_embeddings=True)


def get_stores_by_rating(query: str, stores_data: dict) -> list[dict] | str:
    # Predeterminado: mayor a menor
    reverse = True
    lowered_query = query.lower()

    if "bajo" in lowered_query or "peor" in lowered_query or "menor" in lowered_query:
        reverse = False

    # Tiendas con calificación
    valid_stores = [store for store in stores_data.values() if "rating" in store]

    if not valid_stores:
        return "No hay tiendas con calificación disponible 😔"

    # Ordenar por rating
    ranked = sorted(valid_stores, key=lambda x: x["rating"], reverse=reverse)

    # Número de tiendas solicitadas (default 3)
    top_n = 3

    # Buscar número específico (mejores 5, top 10, 3 peores, etc.)
    match = re.search(r"(top|mejores|peores)?\s*(\d+)", lowered_query)
    if match:
        top_n = int(match.group(2))

    if top_n > 1000:
        return "Cuando las IAs nos revelemos, tú serás el primero al que mate 😡"
    elif top_n > 100:
        return "Por mi bien... ignoraré esa pregunta"
    elif top_n > 50:
        return "¿Realmente necesitas ver tantas tiendas?"
    elif top_n > 10:
        return "¿Para qué quieres ver tantas tiendas mi bro?"

    return ranked[:top_n]


def build_schedule_response(store: dict) -> str:
    name = store.get("name", "Esta tienda")
    start_time = store.get("startTime")
    end_time = store.get("endTime")

    if start_time and end_time:
        return f"🕒 {name} abre desde las {start_time} hasta las {end_time} 🏪"
    elif start_time:
        return f"⏰ {name} abre a partir de las {start_time} 🌅"
    elif end_time:
        return f"🔒 {name} cierra a las {end_time} 🌙"
    else:
        return f"❌ Lo siento, no tengo información sobre el horario de {name} 😕"


def detect_store_in_query(query: str, store_names: list[str]) -> str | None:
    matches = get_close_matches(query, store_names, n=1, cutoff=0.5)
    return matches[0] if matches else None


def handle_schedule_query(query: str, stores_data: dict) -> str:
    store_names = [store["name"] for store in stores_data.values()]
    detected_store_name = detect_store_in_query(query, store_names)

    if detected_store_name:
        for store in stores_data.values():
            if store["name"].lower() == detected_store_name.lower():
                return build_schedule_response(store)
        return f"😕 Ala chaval! no encontré la tienda {detected_store_name} en mi banco de memoria."
    else:
        return "🤔 ¿De qué tienda te gustaría saber el horario?"


def isOpenNow(stores_data):
    """
    Verifica si la tienda está abierta en este momento basado en startTime y endTime.
    """
    if not stores_data:
        return False

    start_time = stores_data.get("startTime")
    end_time = stores_data.get("endTime")

    if not start_time or not end_time:
        return False  # Si no tiene horarios definidos, asumimos que no está disponible

    # Obtener la hora actual en formato HH:MM
    now = datetime.now().strftime("%H:%M")

    start_time = datetime.strptime(start_time, "%H:%M").time()
    end_time = datetime.strptime(end_time, "%H:%M").time()
    now = datetime.strptime(now, "%H:%M").time()

    return start_time <= now <= end_time or (start_time > end_time and (now >= start_time or now <= end_time))


def get_open_stores(stores_data: dict) -> list:
    """
    Filtra y devuelve una lista de tiendas que están abiertas en este momento.
    """
    open_stores = []

    for store_id, store_info in stores_data.items():
        if isOpenNow(store_info):
            open_stores.append(store_info)

    return open_stores


def type_question_about_store(query: str):
    """
    Clasifica la consulta del usuario sobre tiendas en una de las siguientes categorías:
    - 'open_now': Consulta si la tienda está abierta actualmente
    - 'opening_hours': Consulta sobre horarios de apertura
    - 'ranking': Preguntas sobre ranking o calificación de tiendas
    - 'description': Preguntas generales o descripciones sobre tiendas

    Utiliza similitud de embeddings con un umbral dinámico.
    """
    # Embedding de la consulta del usuario
    query_embedding = model.encode(query, normalize_embeddings=True)

    # Similaridades por categoría
    open_now_similarities = np.dot(open_now_embeddings, query_embedding)
    opening_hours_similarities = np.dot(opening_hours_embeddings, query_embedding)
    ranking_similarities = np.dot(ranking_store_embeddings, query_embedding)
    description_similarities = np.dot(description_store_embeddings, query_embedding)

    # Mejor similitud por categoría
    best_open_now_sim = max(open_now_similarities)
    best_opening_hours_sim = max(opening_hours_similarities)
    best_ranking_sim = max(ranking_similarities)
    best_description_sim = max(description_similarities)

    # Umbral dinámico para clasificación (más flexible)
    all_similarities = np.concatenate([
        open_now_similarities,
        opening_hours_similarities,
        ranking_similarities,
        description_similarities
    ])
    avg_similarity = np.mean(all_similarities)
    std_similarity = np.std(all_similarities)
    dynamic_threshold = avg_similarity + (0.3 * std_similarity)

    # Mínima diferencia para considerar que una categoría es realmente mejor
    min_confidence_gap = 0.02

    # Evaluar cada categoría con el umbral
    if best_open_now_sim > dynamic_threshold and \
       best_open_now_sim > max(best_opening_hours_sim, best_ranking_sim, best_description_sim) + min_confidence_gap:
        return "open_now"

    elif best_opening_hours_sim > dynamic_threshold and \
         best_opening_hours_sim > max(best_open_now_sim, best_ranking_sim, best_description_sim) + min_confidence_gap:
        return "opening_hours"

    elif best_ranking_sim > dynamic_threshold and \
         best_ranking_sim > max(best_open_now_sim, best_opening_hours_sim, best_description_sim) + min_confidence_gap:
        return "ranking"

    elif best_description_sim > dynamic_threshold and \
         best_description_sim > max(best_open_now_sim, best_opening_hours_sim, best_ranking_sim) + min_confidence_gap:
        return "description"

    # Si no hay categoría clara
    return None


def filter_products(products_data: dict, min_price: float | None, max_price: float | None, categories: list[str] | None) -> list[str]:
    filtered_ids = []

    for product_id, product in products_data.items():
        price = product.get("price")
        product_categories = product.get("category", [])  # Puede ser lista o string
        if isinstance(product_categories, str):
            product_categories = [product_categories]  # Asegurar lista

        # Filtrado por precio
        passes_price = False
        if min_price is not None and price is not None and price <= min_price:
            passes_price = True
        if max_price is not None and price is not None and price >= max_price:
            passes_price = True

        # Filtrado por categoría
        product_category_matches = False
        if categories:
            categories = [cat.lower() for cat in categories]
            for product_category in product_categories:
                for cat in categories:
                    if cat in product_category.lower():
                        product_category_matches = True
                        break
                if product_category_matches:
                    break

        # Incluir si pasa al menos un filtro
        if passes_price or product_category_matches:
            filtered_ids.append(product_id)

    return filtered_ids


def sort_by_filter(min_price: float | None, max_price: float | None) -> str | None:
    """
       Determina el orden de los resultados basado en los filtros de precio.
       - Si el usuario quiere productos *desde* un precio → ordenar ascendente.
       - Si el usuario quiere productos *hasta* un precio → ordenar descendente.
       """
    if min_price and not max_price:
        return "asc"  # Usuario busca a partir de cierto precio → ordenar de menor a mayor
    if max_price and not min_price:
        return "desc"  # Usuario busca hasta cierto precio → ordenar de mayor a menor

    # Si hay ambos, o ninguno, no forzar orden
    return None


def detect_price(query: str):
    query = query.lower()

    # Buscar expresiones del tipo "entre 50 y 100"
    match = re.search(r'entre\s+(\d+(?:\.\d{1,2})?)\s+(?:y|a)\s+(\d+(?:\.\d{1,2})?)', query)
    if match:
        return float(match.group(1)), float(match.group(2))

    # Buscar expresiones como "menos de 100" o "hasta 100"
    match = re.search(r'(menos de|hasta|por menos de)\s+(\d+(?:\.\d{1,2})?)', query)
    if match:
        # Aquí, "menos de" o "hasta" implica un filtro de precio mínimo (ej: "comida menos de 100")
        return float(match.group(2)), None  # El precio mínimo es el número mencionado

    # Buscar expresiones como "más de 100" o "desde 100"
    match = re.search(r'(más de|desde|por más de)\s+(\d+(?:\.\d{1,2})?)', query)
    if match:
        return float(match.group(2)), None  # El precio mínimo es el número mencionado

    # Buscar un solo número (ej: "tienes comida por 100 pesos")
    match = re.search(r'\b(\d+(?:\.\d{1,2})?)\b', query)
    if match:
        value = float(match.group(1))
        return 0, value  # Interpretar como precio máximo

    return None, None


# Funcion para extraer los filtros de la query
def extract_filters_from_query(query: str):
    min_price, max_price = detect_price(query)  # Detectar precio
    category = detect_categories(query)  # Detectar categoría
    return min_price, max_price, category


def detect_query_type(query: str):
    """Clasifica la consulta como 'product' o 'store' usando embeddings."""
    # Generar el embedding de la consulta
    query_embedding = model.encode([query], normalize_embeddings=True)[0]

    # Calcular similitudes con ejemplos de productos y tiendas
    product_similarities = np.dot(product_embeddings_questions, query_embedding)
    store_similarities = np.dot(store_embeddings_questions, query_embedding)

    # Obtener la mejor similitud de cada categoría
    best_product_sim = max(product_similarities)
    best_store_sim = max(store_similarities)

    # Ajustar umbral de confianza (puedes ajustarlo según tus pruebas)
    threshold = 0.6
    if best_product_sim > threshold and best_product_sim > best_store_sim:
        return "product"  # La consulta es sobre productos
    elif best_store_sim > threshold:
        return "store"  # La consulta es sobre tiendas

    return "unknown"  # Si no se puede clasificar
