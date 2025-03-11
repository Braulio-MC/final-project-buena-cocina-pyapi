import numpy as np
from sentence_transformers import SentenceTransformer
from core.firebaseHelper import db
from core.constants import table_products, table_stores, EMBEDDINGS_MODEL
from nltk.stem import WordNetLemmatizer
import faiss
from functools import lru_cache
from core.botCore import extract_filters, cumple_filtros, dynamic_threshold,  expand_query, detect_store_availability_query, isOpenNow

model = SentenceTransformer(EMBEDDINGS_MODEL)
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
    stores_data = {}

    # Indexar productos
    stores = db.collection(table_stores).stream()
    for doc in stores:
        store = doc.to_dict()
        store_id = doc.id
        stores_data[store_id] = store

        # Generar embeddings sobre tiendas
        text = f" {store['id']} {store['name']} {store['email']} {store['description']} {store['startTime']}-{store['endTime']} {store['rating']}"
        embedding = model.encode(text).astype(np.float32)
        embeddings.append(embedding)
        store_ids.append(store_id)

    if embeddings:
        embeddings_array = np.array(embeddings, dtype=np.float32)
        index.add(embeddings_array)

    return index, store_ids, stores_data


def store_embeddings_in_faiss_products() -> tuple:
    index = faiss.IndexFlatL2(EMBEDDING_DIM)
    product_ids = []
    embeddings = []
    products_data = {}

    # Indexar productos
    products = db.collection(table_products).stream()
    for doc in products:
        product = doc.to_dict()
        product_id = doc.id
        products_data[product_id] = product  # Guardamos todos los productos

        # Generar embedding
        text = f'{product["id"]} {product["name"]} {product["description"]} {" ".join(product["category"])} {product["store"]["name"]} '
        embedding = model.encode(text).astype(np.float32)
        embeddings.append(embedding)
        product_ids.append(product_id)

    if embeddings:
        embeddings_array = np.array(embeddings, dtype=np.float32)
        index.add(embeddings_array)

    return index, product_ids, products_data


# Genera embeddings en base a la pregunta para comprarlos con los embeddings de los productos
def generate_embedding(text: str):
    expanded_text = expand_query(text)
    embedding = model.encode(expanded_text)
    return np.array(embedding, dtype=np.float32)


# Encuentra productos similares
def find_similar_products(query: str, top_k: int = 10):
    index, product_ids, products_data = store_embeddings_in_faiss_products()  # Ahora obtenemos `products_data`
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

    # Aplicar umbral dinámico antes de filtrar por categoría, tienda y precio
    threshold = dynamic_threshold(query)
    filtered_results = [pid for pid, sim in results if sim >= threshold]

    # Filtrar solo los productos que están en `filtered_results`
    print(min_price)
    print(max_price)
    print(category)
    print(store)
    final_results = [
        pid for pid in filtered_results
        if cumple_filtros(products_data.get(pid, {}), min_price, max_price, category, store)
    ]

    # Si el filtrado eliminó todos los productos, devolver los más similares sin filtrar
    return final_results if final_results else [pid for pid, _ in results[:top_k]]


def find_stores(query: str, top_k: int = 10):
    index, product_ids, stores_data = store_embeddings_in_faiss_stores()  # Ahora obtenemos `stores_data`

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
            store_id = product_ids[indices[0][i]]
            similarity = 1 / (1 + distances[0][i])  # Convertir distancia en similitud
            results.append((store_id, similarity))

    # Aplicar umbral dinámico antes de filtrar por categoría, tienda y precio
    threshold = dynamic_threshold(query)
    filtered_results = [pid for pid, sim in results if sim >= threshold]

    # Detectar tipo de consulta
    query_type = detect_store_availability_query(query)
    print(query_type)
    if query_type == "open_now":
        # Filtrar tiendas abiertas en este momento
        open_stores = [sid for sid in filtered_results if isOpenNow(stores_data.get(sid, {}))]

        # Nueva verificación: ¿Todas las tiendas filtradas están abiertas?
        if len(open_stores) == len(filtered_results) and len(open_stores) > 0:
            return "Todas las tiendas están abiertas en este momento."

        return open_stores if open_stores else "No hay tiendas abiertas en este momento."

    elif query_type == "opening_hours":
        # Obtener horarios de apertura/cierre
        horarios = {
            sid: {
                "name": stores_data[sid].get("name", "Tienda desconocida"),
                "startTime": stores_data[sid].get("startTime", "No disponible"),
                "endTime": stores_data[sid].get("endTime", "No disponible"),
            }
            for sid in filtered_results
        }
        return next(iter(horarios.values()), {"message": "No se encontraron horarios disponibles."})

    return filtered_results if filtered_results else [item[0] for item in results]