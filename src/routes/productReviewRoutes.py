from fastapi import APIRouter, Depends, Query
from datetime import datetime
from typing import Annotated, Optional
from controllers.productReviewController import ProductReviewController

router = APIRouter()

@router.get('/product-reviews')
async def get_all(controller: Annotated[ProductReviewController, Depends()]):
    """Devuelve todas las reviews analizadas"""
    return await controller.get_all()

@router.get('/product-reviews/product/{product_id}')
async def get_by_product_id_with_range(
    product_id: str,
    controller: Annotated[ProductReviewController, Depends()],
    start_date: Annotated[Optional[datetime], Query()] = None,
    end_date: Annotated[Optional[datetime], Query()] = None
):
    """Endpoint para filtrar datos por product_id
    :param: product_id
    :optional parameers: start_date, end_date
    :return un diccionario que contiene el comentario analizado de acuerdo al product_id proporcionado
    """
    return await controller.get_by_product_id_with_range(product_id, start_date, end_date)

@router.get('/product-reviews/user/{user_id}')
async def get_by_user_id_with_range(
    user_id: str, 
    controller: Annotated[ProductReviewController, Depends()],
    start_date: Annotated[Optional[datetime], Query()] = None,
    end_date: Annotated[Optional[datetime], Query()] = None
):
    """Endpoint para filtrar datos por user_id
    :param: user_id
    :optional parameers: start_date, end_date
    :return un diccionario que contiene el comentario analizado de acuerdo al user_id proporcionado
    """
    return await controller.get_by_user_id_with_range(user_id, start_date, end_date)
