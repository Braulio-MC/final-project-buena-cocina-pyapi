import os
import joblib
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from core.constants import EMBEDDINGS_JOBLIB, PRODUCTS_IDS_CSV, SENTENCE_TRANSFORMERS_MODEL_NAME
from core.dataPreprocessing import create_features_df
from sentence_transformers import SentenceTransformer

class Recommender:
    def __init__(self):
        """Carga embeddings e IDs de productos, generándolos si no existen."""
        if not os.path.exists(EMBEDDINGS_JOBLIB) or not os.path.exists(PRODUCTS_IDS_CSV):
            print("⚠ Archivos no encontrados. Generando embeddings...")
            self.generate_and_save_embeddings()



        # **Cargar embeddings y productos**
        self.embeddings = joblib.load(EMBEDDINGS_JOBLIB)
        self.product_ids = pd.read_csv(PRODUCTS_IDS_CSV, dtype=str)['id'].str.strip().tolist()

    def generate_and_save_embeddings(self):
        """Genera los embeddings de los productos si no existen."""
        model = SentenceTransformer(SENTENCE_TRANSFORMERS_MODEL_NAME )  # Modelo para generar embeddings
        df = create_features_df()  # Obtener los datos preprocesados

        embeddings = model.encode(df['text_features'].tolist(), show_progress_bar=True)

        # 🔹 **Guardar los archivos**
        os.makedirs(os.path.dirname(EMBEDDINGS_JOBLIB), exist_ok=True)
        joblib.dump(embeddings, EMBEDDINGS_JOBLIB)
        df[["id"]].to_csv(PRODUCTS_IDS_CSV, index=False)

        print("Embeddings generados y guardados correctamente.")

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
        target_embedding = self.embeddings[idx].reshape(1, -1)  # Embedding del producto consultado

        # **Calcular la similitud de coseno con todos los productos**
        similarities = cosine_similarity(target_embedding, self.embeddings)[0]

        # **Obtener los índices de los productos más similares**
        top_indices = np.argsort(similarities)[-top_n - 1:-1][::-1]

        # **Devolver los IDs de los productos similares**
        return [self.product_ids[i] for i in top_indices]