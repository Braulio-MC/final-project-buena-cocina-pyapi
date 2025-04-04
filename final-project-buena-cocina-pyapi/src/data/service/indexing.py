from core.constants import table_products, table_stores, EMBEDDINGS_MODEL
from core.firebaseHelper import db
import numpy as np
from sentence_transformers import SentenceTransformer
import faiss

# Inicialización del modelo y configuración de FAISS
model = SentenceTransformer(EMBEDDINGS_MODEL)
EMBEDDING_DIM = model.get_sentence_embedding_dimension()

# Variables globales del índice
PRODUCT_INDEX = None
PRODUCT_IDS = []
PRODUCTS_DATA = {}

STORE_INDEX = None
STORE_IDS = []
STORES_DATA = {}

def refresh_faiss_index_products():
    global PRODUCT_INDEX, PRODUCT_IDS, PRODUCTS_DATA

    # Crear un nuevo índice FAISS
    index = faiss.IndexFlatL2(EMBEDDING_DIM)
    product_ids = []
    embeddings = []
    products_data = {}

    # Obtener los productos desde Firebase
    try:
        products = db.collection(table_products).stream()
        for doc in products:
            product = doc.to_dict()
            product_id = doc.id
            products_data[product_id] = product

            # Crear el texto para el embedding
            text = f"{product['name']} {product['description']} {' '.join(product.get('category', []))} {product['store']['name']}"
            embedding = model.encode(text).astype(np.float32)

            embeddings.append(embedding)
            product_ids.append(product_id)

        if embeddings:
            # Convertir los embeddings a un array numpy y agregar al índice FAISS
            embeddings_array = np.array(embeddings, dtype=np.float32)
            index.add(embeddings_array)

        # Actualizar las variables globales
        PRODUCT_INDEX = index
        PRODUCT_IDS = product_ids
        PRODUCTS_DATA = products_data

        print(f"FAISS index actualizado con {len(product_ids)} productos.")
    except Exception as e:
        print(f"Error al refrescar el índice de productos: {e}")


def refresh_faiss_index_stores() -> tuple:
    global STORE_INDEX, STORE_IDS, STORES_DATA

    # Crear un nuevo índice FAISS
    index = faiss.IndexFlatL2(EMBEDDING_DIM)
    store_ids = []
    embeddings = []
    stores_data = {}

    # Obtener las tiendas desde Firebase
    try:
        stores = db.collection(table_stores).stream()
        for doc in stores:
            store = doc.to_dict()
            store_id = doc.id
            stores_data[store_id] = store

            # Crear el texto para el embedding
            text = f"{store['id']} {store['name']} {store['email']} {store['description']} {store['startTime']}-{store['endTime']} {store['rating']}"
            embedding = model.encode(text).astype(np.float32)

            embeddings.append(embedding)
            store_ids.append(store_id)

        if embeddings:
            # Convertir los embeddings a un array numpy y agregar al índice FAISS
            embeddings_array = np.array(embeddings, dtype=np.float32)
            index.add(embeddings_array)

        # Actualizar las variables globales
        STORE_INDEX = index
        STORE_IDS = store_ids
        STORES_DATA = stores_data

        print(f"FAISS index actualizado con {len(store_ids)} tiendas.")
    except Exception as e:
        print(f"Error al refrescar el índice de tiendas: {e}")

    return index, store_ids, stores_data
