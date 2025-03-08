from fastapi import APIRouter
from data.service.embeddingService import find_similar_products, find_stores
from domain.repository.productRepository import get_products_by_ids
from domain.repository.storeRepository import get_stores_by_ids
from core.botCore import detect_query_type

router = APIRouter()

@router.get("/query")
async def get_recommendations(query: str):
    if detect_query_type(query) == 'store':
        store_ids = find_stores(query)
        return get_stores_by_ids(store_ids)
    else:
        product_ids = find_similar_products(query)
        return get_products_by_ids(product_ids)
