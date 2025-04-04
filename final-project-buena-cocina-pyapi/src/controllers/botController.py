from fastapi import APIRouter

from core.botHelpers import get_no_results_message
from data.service.embeddingService import find_products, find_stores
from core.botCore import detect_query_type

router = APIRouter()


@router.get("/query")
async def get_recommendations(query: str):
    # Detectar el tipo de consulta
    query_type = detect_query_type(query)

    # La consulta es sobre tiendas
    if query_type == 'store':
        store_response = find_stores(query)
        if isinstance(store_response, list):
            return {"type": "store", "data": store_response}
        elif isinstance(store_response, str):
            return {"type": "message", "message": store_response}
        else:
            return {"type": "message", "message": "No se encontraron resultados para tu consulta de tienda."}
    else:
        # La conulta es sobre productos
        product_response = find_products(query)
        if isinstance(product_response, list):
            return {"type": "product", "data": product_response}
        else:
            return {"type": "message", "message": get_no_results_message()}
