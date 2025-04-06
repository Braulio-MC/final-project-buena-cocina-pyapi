from core.constants import CATEGORY_SYNONYMS, EMBEDDINGS_MODEL
import numpy as np
from sentence_transformers import SentenceTransformer
import faiss
import random
import unicodedata
import re

model = SentenceTransformer(EMBEDDINGS_MODEL)

# Variables globales para los índices y los ids

# Para descripciones
DESCRIPTION_INDEX = None
DESCRIPTION_IDS = None

# Para categorias
CATEGORY_INDEX = None
CATEGORY_LIST = []

# Construir el índice de descripciones
def build_description_faiss_index(products_data: dict):
    descriptions = []
    product_ids = []

    # Crear lista de descripciones y sus correspondientes ids de productos
    for prod_id, prod in products_data.items():
        description = prod.get("description", "")
        if description:  # Asegurarse de que la descripción no esté vacía
            descriptions.append(generate_embedding_simple(description))
            product_ids.append(prod_id)

    # Inicializar FAISS con el número de dimensiones de los embeddings
    index = faiss.IndexHNSWFlat(len(descriptions[0]), 32)
    index.add(np.array(descriptions, dtype=np.float32))

    return index, product_ids

# Función para inicializar el índice de descripciones y los ids
def initialize_description_index(products_data: dict):
    global DESCRIPTION_INDEX, DESCRIPTION_IDS
    DESCRIPTION_INDEX, DESCRIPTION_IDS = build_description_faiss_index(products_data)


def search_by_description_fallback(query: str, products_data: dict):
    query_embedding = generate_embedding_simple(query).reshape(1, -1)

    # Si el índice no ha sido creado, devolver una lista vacía o productos por defecto
    if DESCRIPTION_INDEX is None or DESCRIPTION_IDS is None:
        return []

    # Realizar la búsqueda utilizando el índice FAISS
    distances, idxs = DESCRIPTION_INDEX.search(query_embedding, 5)

    # Devolver los ids de los productos más cercanos
    return [DESCRIPTION_IDS[i] for i in idxs[0]]

# Busqueda por categoria
def build_category_faiss_index():
    if not CATEGORY_SYNONYMS:
        return None, None

    category_names = list(CATEGORY_SYNONYMS.keys())
    category_embeddings = [generate_embedding_simple(category) for category in category_names]

    if not category_embeddings or len(category_embeddings) == 0:
        return None, None

    dim = len(category_embeddings[0])
    index = faiss.IndexHNSWFlat(dim, 32)
    index.add(np.array(category_embeddings, dtype=np.float32))

    return index, category_names

def ensure_category_index_initialized():
    global CATEGORY_INDEX, CATEGORY_LIST
    if CATEGORY_INDEX is None or not CATEGORY_LIST:
        CATEGORY_INDEX, CATEGORY_LIST = build_category_faiss_index()

def detect_categories(query: str) -> list[str]:
    ensure_category_index_initialized()

    detected = set()
    query = query.lower()  # Normaliza todo en minúsculas

    # Búsqueda directa por sinónimos o nombres
    for category, synonyms in CATEGORY_SYNONYMS.items():
        if category in query:
            detected.add(category)
        elif any(syn in query for syn in synonyms):
            detected.add(category)

    # Si ya se detectaron categorías directamente, no usar FAISS (más preciso)
    if detected:
        return list(detected)

    # Si no se detectó nada directo, usar embeddings
    query_embedding = generate_embedding_simple(query).reshape(1, -1)
    distances, indices = CATEGORY_INDEX.search(query_embedding, 5)

    for i, idx in enumerate(indices[0]):
        category = CATEGORY_LIST[idx]
        distance = distances[0][i]

        if distance < 0.15:
            detected.add(category)

    return list(detected)


# Rangos de precio
def extract_price_range(query: str):
    print('rango')

    # 1. Detectar expresiones como "entre 100 y 150" (con o sin pesos)
    match = re.search(r'entre\s+\$?(\d+(?:\.\d{1,2})?)\s+(?:y|a)\s+\$?(\d+(?:\.\d{1,2})?)\s*(?:pesos)?', query)
    if match:
        print(1)
        return float(match.group(1)), float(match.group(2))

    # 2. Detectar expresiones como "de 100 a 200"
    match = re.search(r'de\s+\$?(\d+(?:\.\d{1,2})?)\s+(?:a|y)\s+\$?(\d+(?:\.\d{1,2})?)\s*(?:pesos)?', query)
    if match:
        return float(match.group(1)), float(match.group(2))

    # 3. Detectar expresiones como "más de 100 y menos de 200"
    match = re.search(r'más\s+de\s+\$?(\d+(?:\.\d{1,2})?).*?menos\s+de\s+\$?(\d+(?:\.\d{1,2})?)\s*(?:pesos)?', query)
    if match:
        return float(match.group(1)), float(match.group(2))

    # 4. Detectar expresiones como "$100 a $200" o "100 - 200"
    match = re.search(r'\$?(\d+(?:\.\d{1,2})?)\s*(?:-|a|–|—)\s*\$?(\d+(?:\.\d{1,2})?)\s*(?:pesos)?', query)
    if match:
        return float(match.group(1)), float(match.group(2))

    # No se detectó un rango
    return None, None

# Mejor y pulir la consulta
def find_closest_word(query: str, index, valid_words):
    query_embedding = model.encode([query])
    D, I = index.search(np.array(query_embedding, dtype=np.float32), k=1)
    closest_word = valid_words[I[0][0]]
    return closest_word, D[0][0]


def correct_word(word: str) -> str:
    ensure_category_index_initialized()
    closest_word, distance = find_closest_word(word, CATEGORY_INDEX, CATEGORY_LIST)
    return closest_word if distance < 0.3 else word


# Normalizar query
def normalize_query(query: str) -> str:
    # Pasar a minúsculas
    query = query.lower()

    # Eliminar acentos/tildes
    query = unicodedata.normalize('NFD', query)
    query = query.encode('ascii', 'ignore').decode('utf-8')

    # Eliminar puntuación
    query = re.sub(r'[^\w\s]', '', query)

    # Quitar espacios extras
    query = re.sub(r'\s+', ' ', query).strip()

    return query


# Generar embedding de preguntas
def generate_embedding_simple(text: str):
    """
        Esto genera el embedding de mi pregunta
    """
    embedding = model.encode(text)
    return np.array(embedding, dtype=np.float32)


# Mensajes del bot
def get_no_results_message():

    """
        Generamos un mensaje aleatorio en caso de no encontar los productos solicitados
    """

    messages = [
        "¡Ups! No encontré productos que coincidan con lo que estás buscando. ¿Quieres intentar con otra categoría o precio?",
        "Parece que no tengo nada que mostrarte con esos filtros 😔. ¡Prueba cambiando tu búsqueda y lo intentamos de nuevo!",
        "Nada por aquí... nada por allá... 🧙‍♂️ Pero puedes probar con otras palabras o quitar algunos filtros.",
        "No encontré coincidencias esta vez. Pero no te preocupes, ¡hay muchos sabores por descubrir! 🍽️",
        "Hmm... no hay resultados por ahora. ¡Pero el menú es grande! Intenta con algo diferente 😄",
        "La verdad no te entendí, amigo… pero deberías leer El Capital de Marx 🔨🌾"
    ]

    return random.choice(messages)


def no_open_stores_message():
    messages = [
        "🕒 Parece que las tiendas están tomando una siesta… ¡vuelve más tarde!",
        "🌙 Las tiendas están cerradas por ahora… ¡como un buen croissant, hay que esperar el momento justo!",
        "🚪 No encontramos tiendas abiertas en este momento. ¡Pero no te preocupes, pronto volverán a abrir sus puertas!",
        "🍵 Todo en pausa… ¡es hora del té! Las tiendas abrirán en breve.",
        "😴 Las tiendas están durmiendo. Mientras tanto, ¿por qué no piensas en tu próximo antojo?"
    ]
    return random.choice(messages)


def get_confused_message():
    messages = [
        "¡Ups! Creo que mi paladar virtual no reconoció eso 🤔. ¿Puedes decirlo de otra forma?",
        "Hmm... eso no está en mi menú mental 🍴. ¿Quizás quisiste decir otra cosa?",
        "¡Ay caramba! Mi recetario se quedó en blanco con eso 😵‍💫. ¿Me lo repites con otras palabras?",
        "Esa especialidad no la tengo en la carta... por ahora 😅. ¿Quieres intentar con otra categoría?",
        "¡Error de cocinero! No entendí bien tu antojo 👨‍🍳. ¿Puedes aclararlo un poquito más?",
        "Mi radar gastronómico está confundido 😵. ¿Podrías reformular tu pregunta?",
        "Hmm... ¿me hablaste en otro idioma culinario? 🍜 Intenta preguntarme de otra forma 😉"
    ]
    return random.choice(messages)

def nosense_response():
    messages = [
        "Mmm... no entendí muy bien eso 🤔 ¿comida de qué tipo estás buscando?",
        "¡Eso suena interesante, pero no lo tengo en el menú! 😅",
        "¿Armas de fuego? Creo que te equivocaste de restaurante 🔫🚫🍔",
        "Estoy entrenado para encontrar comida, no para entrar en acción 😂",
        "No entendí la pregunta. ¿Podrías decirlo de otra forma más sabrosa? 😋",
    ]
    return random.choice(messages)