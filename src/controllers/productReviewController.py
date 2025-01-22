from fastapi import Depends
from typing import Optional, Annotated
from datetime import datetime
from core.preProcessing import cleaning_review
from core.sentimentAnalyzer import feeling_review
from domain.repository.productReviewRepository import ProductReviewRepository

class ProductReviewController:
    def __init__(self, repository: Annotated[ProductReviewRepository, Depends()]):
        self.repository = repository

    async def get_all(self):
        """Devuelve todas las reviews analizadas"""
        reviews = await self.repository.get_all()
        cleaned_reviews = [cleaning_review(review) for review in reviews]
        analyzed_reviews = [feeling_review(review) for review in cleaned_reviews]
        return analyzed_reviews
    
    async def get_by_product_id_with_range(
        self,
        product_id: str,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None
    ):
        """Endpoint para filtrar datos por product_id
        :param: product_id
        :optional parameers: start_date, end_date
        :return un diccionario que contiene el comentario analizado de acuerdo al product_id proporcionado
        """
        reviews = await self.repository.get_by_product_id_with_range(product_id, start_date, end_date)
        cleaned_reviews = [cleaning_review(review) for review in reviews]
        analyzed_reviews = [feeling_review(review) for review in cleaned_reviews]
        return {"query_id": product_id, "reviews": analyzed_reviews}
    
    async def get_by_user_id_with_range(
        self, 
        user_id: str,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None
    ):
        """Endpoint para filtrar datos por user_id
        :param: user_id
        :optional parameers: start_date, end_date
        :return un diccionario que contiene el comentario analizado de acuerdo al user_id proporcionado
        """
        reviews = await self.repository.get_by_user_id_with_range(user_id, start_date, end_date)
        cleaned_reviews = [cleaning_review(review) for review in reviews]
        analyzed_reviews = [feeling_review(review) for review in cleaned_reviews]
        return {"query_id": user_id, "reviews": analyzed_reviews}