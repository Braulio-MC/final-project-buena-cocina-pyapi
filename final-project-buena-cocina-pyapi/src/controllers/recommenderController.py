from fastapi import APIRouter
from data.service.productService import get_similar_product_recommendations


router = APIRouter()

@router.get("/products/{product_id}/similar")
def similar_products(product_id: str):
    return get_similar_product_recommendations(product_id)


