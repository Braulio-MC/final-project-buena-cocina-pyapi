from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import joblib
import pandas as pd
from constants import EMBEDDINGS_JOBLIB, PRODUCTS_IDS_CSV

class Recommender:
    def __init__(self):
        self.embeddings = joblib.load(EMBEDDINGS_JOBLIB)
        self.product_ids = pd.read_csv(PRODUCTS_IDS_CSV)['id'].tolist()

    def recommend(self, product_id: str, top_n: int = 5):
        """
        Recomienda productos similares basados en embeddings.
        """

        if product_id not in self.product_ids:
            raise ValueError(f"El ID del producto '{product_id}' no se encuentra en la base de datos.")

        idx = self.product_ids.index(product_id)
        target_embedding = self.embeddings[idx].reshape(1, -1)
        similarities = cosine_similarity(target_embedding, self.embeddings)[0]

        # Obtener los índices de los productos más similares
        top_indices = np.argsort(similarities)[-top_n-1:-1][::-1]
        return [self.product_ids[i] for i in top_indices]


