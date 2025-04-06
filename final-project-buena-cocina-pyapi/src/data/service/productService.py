from domain.repository import productRespository
from  core.recommender import get_similar_stores

def get_similar_product_recommendations(product_id: str):
    original = productRespository.get_product_by_id(product_id)
    if not original:
        return {"error": "Producto no encontrado"}

    similar_ids = get_similar_stores(product_id)
    similar_products = productRespository.get_products_by_ids(similar_ids)
    return similar_products


