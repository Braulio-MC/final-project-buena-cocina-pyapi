from core.recommender import Recommender
from firebase_admin import firestore

db = firestore.client()

class RecommenderService:
    def __init__(self):
        self.recommender = Recommender()

    async def get_recommendations(self, product_id: str, top_n: int = 5):
        product_ids = self.recommender.recommend(product_id, top_n)

        # Obtener detalles de los productos recomendados desde firebase
        recommended_products = []
        for pid in product_ids:
            product_ref = db.collection('products').document(pid).get()
            if product_ref.exists:
                recommended_products.append(product_ref.to_dict())

        return recommended_products