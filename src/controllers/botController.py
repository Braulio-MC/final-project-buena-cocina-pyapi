from fastapi import APIRouter
from data.service.embeddingService import find_similar_products, find_stores
from domain.repository.productRepository import get_products_by_ids
from domain.repository.storeRepository import get_stores_by_ids
from core.botCore import detect_query_type, detect_preference

router = APIRouter()

@router.get("/query")
async def get_recommendations(query: str):
    if detect_query_type(query) == 'store':
        store_response = find_stores(query)
        if isinstance(store_response, list):
            results = get_stores_by_ids(store_response)
            sort_field, sort_order = detect_preference(query)
            if sort_field:
                results.sort(key=lambda x: x[sort_field], reverse=(sort_order == "desc"))
            return results
        elif isinstance(store_response, str):
            return {"message": store_response}
        elif isinstance(store_response, dict):
            return store_response
        else:
            return {"error": "No se encontraron resultados para tu consulta."}
    else:
        product_response = find_similar_products(query)

        if isinstance(product_response, list):
            results = get_products_by_ids(product_response)
            sort_field, sort_order = detect_preference(query)
            if sort_field:
                results.sort(key=lambda x: x[sort_field], reverse=(sort_order == "desc"))

            return results  # Ahora siempre retorna resultados
        else:
            return {"error": "No se encontraron resultados para tu consulta."}


