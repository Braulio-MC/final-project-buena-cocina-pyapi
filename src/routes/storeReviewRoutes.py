from fastapi import APIRouter, Depends, Query
from datetime import datetime
from typing import Annotated, Optional
from controllers.storeReviewController import StoreReviewController

router = APIRouter()

@router.get('/store-reviews')
async def get_all(controller: Annotated[StoreReviewController, Depends()]):
    """Devuelve todas las reviews analizadas"""
    return await controller.get_all()

@router.get('/store-reviews/store/{store_id}')
async def paging_by_store_id_with_range(
    store_id: str,
    controller: Annotated[StoreReviewController, Depends()],
    limit: Annotated[int, Query()] = 10,
    next_cursor: Annotated[Optional[str], Query()] = None,
    start_date: Annotated[Optional[datetime], Query()] = None,
    end_date: Annotated[Optional[datetime], Query()] = None
):
    """Endpoint para filtrar datos por store_id
    :param: store_id, limit
    :optional parameers: next_cursor, start_date, end_date
    :return un diccionario que contiene el comentario analizado de acuerdo al store_id proporcionado y el cursor para la paginación
    """
    return await controller.paging_by_store_id_with_range(store_id, limit, next_cursor, start_date, end_date)

@router.get('/store-reviews/user/{user_id}')
async def paging_by_user_id_with_range(
    user_id: str, 
    controller: Annotated[StoreReviewController, Depends()],
    limit: Annotated[int, Query()] = 10,
    next_cursor: Annotated[Optional[str], Query()] = None,
    start_date: Annotated[Optional[datetime], Query()] = None,
    end_date: Annotated[Optional[datetime], Query()] = None
):
    """Endpoint para filtrar datos por user_id
    :param: user_id, limit
    :optional parameers: next_cursor start_date, end_date
    :return un diccionario que contiene el comentario analizado de acuerdo al user_id proporcionado y el cursor para la paginación
    """
    return await controller.paging_by_user_id_with_range(user_id, limit, next_cursor, start_date, end_date)
