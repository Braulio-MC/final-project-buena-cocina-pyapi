from fastapi import APIRouter, Depends, Query
from typing import Annotated
from controllers.recommenderController import RecommenderController

router = APIRouter()

@router.get('recommendations/{product_id}')
async def get_recommendations(
    product_id: str,
    controller: Annotated[RecommenderController, Depends()],
    top_n: Annotated[int, Query(ge=1, le=20)] = 5
):
    """
       Obtiene productos recomendados basados en embeddings.
       :param product_id: ID del producto de referencia
       :param top_n: Número de recomendaciones (máx. 20)
    """

    return await controller.get_recommendations(product_id, top_n)
