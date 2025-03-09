import numpy as np
from sentence_transformers import SentenceTransformer
from core.firebaseHelper import db
from core.constants import SENTENCE_TRANSFORMERS_MODEL_NAME, table_products, table_stores
from nltk.stem import WordNetLemmatizer
import faiss
from functools import lru_cache
from core.botCore import extract_filters, cumple_filtros, dynamic_threshold, detect_preference, expand_query

model = SentenceTransformer(SENTENCE_TRANSFORMERS_MODEL_NAME)
lemmatizer = WordNetLemmatizer()

# Dimensión de los embeddings según el modelo usado
EMBEDDING_DIM = model.get_sentence_embedding_dimension()

@lru_cache(maxsize=1)
def get_faiss_index():
    return store_embeddings_in_faiss_products()


@lru_cache(maxsize=1)
def get_faiss_index_store():
    return store_embeddings_in_faiss_stores()

def store_embeddings_in_faiss_stores() -> tuple:
    index = faiss.IndexFlatL2(EMBEDDING_DIM)
    store_ids = []
    embeddings = []

    # Indexar productos
    stores = db.collection(table_stores).stream()
    for doc in stores:
        store = doc.to_dict()
        product_id = doc.id
        text = store["name"] + " " + store["description"]
        embedding = model.encode(text).astype(np.float32)
        embeddings.append(embedding)
        store_ids.append(product_id)

    if embeddings:
        embeddings_array = np.array(embeddings, dtype=np.float32)
        index.add(embeddings_array)

    return index, store_ids


def store_embeddings_in_faiss_products() -> tuple:
    index = faiss.IndexFlatL2(EMBEDDING_DIM)
    product_ids = []
    embeddings = []

    # Indexar productos
    products = db.collection(table_products).stream()
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
            similarity = 1 / (1 + distances[0][i])  # Convertir distancia en similitud
            results.append((product_id, similarity))

    # Aplicar umbral dinámico
    threshold = dynamic_threshold(query)
    filtered_results = [pid for pid, sim in results if sim >= threshold]


    # Obtener productos desde Firestore por ID
    product_docs = [db.collection(table_products).document(pid).get() for pid in filtered_results]
    products_data = {doc.id: doc.to_dict() for doc in product_docs if doc.exists and doc.to_dict() is not None}

    # Aplicar filtros de precio, categoría y tienda
    final_results = [
        pid for pid in filtered_results
        if cumple_filtros(products_data.get(pid, {}), min_price, max_price, category, store)
    ]

    # Si el filtrado eliminó todos los productos, devolver los más similares sin filtrar
    return final_results if final_results else [pid for pid, _ in results[:top_k]]



def find_stores(query: str, top_k: int = 3):
    index, store_ids = get_faiss_index_store()


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
            store_id = store_ids[indices[0][i]]
            similarity = 1 / (1 + distances[0][i])  # Convertir distancia en similitud
            results.append((store_id, similarity))

    # Aplicar umbral dinámico
    threshold = dynamic_threshold(query)
    filtered_results = [pid for pid, sim in results if sim >= threshold]

    return filtered_results if filtered_results else [item[0] for item in results]