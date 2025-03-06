import numpy as np
from sentence_transformers import SentenceTransformer
from core.firebaseHelper import db
from core.synonyms import get_synonyms
from core.constants import SENTENCE_TRANSFORMERS_MODEL_NAME, CATEGORY_SYNONYMS
from nltk.stem import WordNetLemmatizer
import faiss
from functools import lru_cache
from core.botCore import extract_filters, cumple_filtros, dynamic_threshold

model = SentenceTransformer(SENTENCE_TRANSFORMERS_MODEL_NAME)
lemmatizer = WordNetLemmatizer()

# Dimensión de los embeddings según el modelo usado
EMBEDDING_DIM = model.get_sentence_embedding_dimension()

@lru_cache(maxsize=1)
def get_faiss_index():
    return store_embeddings_in_faiss()


def store_embeddings_in_faiss() -> tuple:
    index = faiss.IndexFlatL2(EMBEDDING_DIM)
    product_ids = []
    products = db.collection("productos").stream()
    embeddings = []

    for doc in products:
        product = doc.to_dict()
        product_id = doc.id
        text = product["name"] + " " + product["description"] + " " + " ".join(product["category"])
        embedding = model.encode(text).astype(np.float32)
        embeddings.append(embedding)
        product_ids.append(product_id)

    if embeddings:
        embeddings_array = np.array(embeddings, dtype=np.float32)
        index.add(embeddings_array)

    return index, product_ids


def expand_query(query: str):
    """ Expande la consulta con sinónimos y luego aplica lematización.
    """
    words = query.lower().split()
    expanded_query = []

    for word in words:
        expanded_query.append(word)

        # Agregamos sinonimos de categoria
        expanded_query.extend(CATEGORY_SYNONYMS.get(word, []))

        # Agregar sinonimos adicionales
        expanded_query.extend(get_synonyms(word))

    lemmatized_query = [lemmatizer.lemmatize(word) for word in expanded_query]

    return " ".join(set(lemmatized_query))


# Genera embeddings en base a la pregunta para comprarlos con los embeddings de los productos
def generate_embedding(text: str):
    expanded_text = expand_query(text)
    embedding = model.encode(expanded_text)
    return np.array(embedding, dtype=np.float32)


# Encuentra productos similares
def find_similar_products(query: str, top_k: int = 3):
    index, product_ids = get_faiss_index()
    min_price, max_price, category, store = extract_filters(query)

    if index is None or index.ntotal == 0:
        print("El índice FAISS está vacío.")
        return []

    # Generar embedding para la consulta
    query_embedding = np.array([generate_embedding(query)], dtype=np.float32)

    # Buscar en FAISS (devuelve distancias y posiciones en el índice)
    distances, indices = index.search(query_embedding, top_k)

    results = []
    for i in range(top_k):
        if indices[0][i] != -1:  # Verificar si FAISS devolvió un índice válido
            product_id = product_ids[indices[0][i]]
            results.append((product_id, distances[0][i]))  # Guardar ID y distancia

    threshold = dynamic_threshold(query)
    results = [(product_id, dist) for product_id, dist in results if dist >= threshold]

    # Filtrar los resultados según los filtros extraídos
    filtered_results = [
        (pid, dist) for pid, dist in results
        if cumple_filtros(pid, min_price, max_price, category, store)
    ]

    # Aquí está el cambio para manejar el caso cuando no hay resultados filtrados
    if filtered_results:
        return [item[0] for item in filtered_results]
    else:
        return [item[0] for item in results]



