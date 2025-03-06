from fastapi import APIRouter
from data.service.embeddingService import find_similar_products
from domain.repository.productRepository import get_products_by_ids

router = APIRouter()

@router.get("/query")
async def get_recommendations(query: str):
    product_ids = find_similar_products(query)
    return get_products_by_ids(product_ids)