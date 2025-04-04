from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from core.constants import  SENTENCE_TRANSFORMERS_MODEL_NAME, EMBEDDINGS_MODEL
from core.dataPreprocessing import create_features_df
from sentence_transformers import SentenceTransformer
from core.firebaseHelper import db

model = SentenceTransformer(EMBEDDINGS_MODEL)

class Recommender:
    def __init__(self):
        """Carga embeddings e IDs de productos desde Firestore, generándolos si no existen."""
        embeddings_ref = db.collection("embeddings").stream()
        self.embeddings = []
        self.product_ids = []

        for doc in embeddings_ref:
            data = doc.to_dict()
            self.product_ids.append(doc.id)
            self.embeddings.append(data["embedding"])

        # Si no hay embeddings en Firestore, generarlos
        if not self.embeddings:
            print("Embeddings no encontrados en Firestore. Generando embeddings...")
            self.generate_and_save_embeddings()
        else:
            print("Embeddings cargados desde Firestore correctamente.")

    def generate_and_save_embeddings(self):
        """Genera los embeddings de los productos y los guarda en Firestore."""

        df = create_features_df()

        # Verificar si el DataFrame tiene datos
        if df.empty:
            print("No hay datos disponibles para generar embeddings.")
            return  # Terminar la función si no hay datos

        if 'text_features' not in df.columns:
            raise ValueError("La columna 'text_features' no se encuentra en el DataFrame.")

        # Verificar si hay textos en 'text_features'
        if df['text_features'].dropna().empty:
            print("No hay textos válidos en la columna 'text_features'.")
            return  # Terminar la función si no hay textos válidos

        # Generar embeddings
        embeddings = model.encode(df['text_features'].tolist(), show_progress_bar=True)

        # Guardar embeddings y product_ids en Firestore
        batch = db.batch()
        batch_size = 0  # Controlar el tamaño del batch
        max_batch_size = 500  # Límite de Firestore

        for product_id, embedding in zip(df['id'], embeddings):
            # Comprimir a float16 para ahorrar espacio
            compressed_embedding = np.array(embedding, dtype=np.float16).tolist()

            doc_ref = db.collection("embeddings").document(product_id)
            batch.set(doc_ref, {"embedding": compressed_embedding})
            batch_size += 1

            # Confirmar batch si llega al límite
            if batch_size >= max_batch_size:
                batch.commit()
                batch = db.batch()
                batch_size = 0

        # Confirmar el batch final si quedó algo pendiente
        if batch_size > 0:
            batch.commit()

        print("Embeddings generados y guardados en Firestore correctamente.")

    def recommend(self, product_id: str, top_n: int = 5):
        """
        Recomienda productos similares a un producto dado.

         Parámetros:
        - product_id (str): ID del producto a buscar.
        - top_n (int): Número de recomendaciones.

         Retorno:
        - Lista con los `top_n` productos más similares.
        """
        print(f"Recomendando productos para el ID: {product_id}")
        product_id = product_id.strip()  # Eliminar espacios en blanco y saltos de línea

        if product_id not in self.product_ids:
            raise ValueError(f"El ID del producto '{product_id}' no se encuentra en la base de datos.")

        #  **Obtener el índice del producto consultado**
        idx = self.product_ids.index(product_id)
        target_embedding = np.array(self.embeddings[idx]).reshape(1, -1) # Embedding del producto consultado

        # **Calcular la similitud de coseno con todos los productos**
        similarities = cosine_similarity(target_embedding, self.embeddings)[0]

        # **Obtener los índices de los productos más similares**
        top_indices = np.argsort(similarities)[-top_n - 1:-1][::-1]

        # **Devolver los IDs de los productos similares**
        return [self.product_ids[i] for i in top_indices]