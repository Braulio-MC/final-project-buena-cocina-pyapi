from fastapi import APIRouter

from data.service.storeService import get_similar_store_recommendations

router = APIRouter()

@router.get("/stores/{store_id}/similar")
def similar_stores(stores_id):
    return get_similar_store_recommendations(stores_id)