from domain.repository import storeRepository
from core.recommender import get_similar_stores

def get_similar_store_recommendations(store_id: str):
    original = storeRepository.get_store_by_id(store_id)
    if not original:
        return {"error": "Tienda no encontrada"}

    similar_ids = get_similar_stores(store_id)
    similar_products = storeRepository.get_stores_by_ids(similar_ids)
    return similar_products