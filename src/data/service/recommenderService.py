from core.recommender import Recommender
from core.firebaseHelper import db
from core.constants import table_products


class RecommenderService:
    def __init__(self):
        self.recommender = Recommender()

    async def get_recommendations(self, product_id: str, top_n: int = 5):

        """Obtiene productos recomendados con información desde Firestore."""
        product_id = product_id.strip()
        product_ids = self.recommender.recommend(product_id, top_n)

        recommended_products = []
        for pid in product_ids:
            product_ref = db.collection(table_products).document(pid).get()
            if product_ref.exists:
                data = product_ref.to_dict()

                # Validaciones antes de agregar el producto recomendado
                if not data.get("available", False):
                    continue

                # No recomendar productos que no tengan precio o tenhan precio negativo
                if data.get("price", 0) <= 0:
                    continue

                # Agregamos los productos recomendados
                recommended_products.append({
                    "id": pid,
                    "name": data.get("name", ""),
                    "description": data.get("description", ""),
                    "image": data.get("image", ""),
                    "price": data.get("price", 0),
                    "store": data.get("store", {}),
                    "category": data.get("category", []),
                    "rating": data.get("rating", 0),
                })
            else:
                print(f"Producto con ID {pid} no encontrado en Firestore.")
        return recommended_products