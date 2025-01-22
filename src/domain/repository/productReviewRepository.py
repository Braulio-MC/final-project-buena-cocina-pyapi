from fastapi import Depends
from datetime import datetime
from typing import Annotated, Optional
from data.service.productReviewService import ProductReviewService
from domain.model.productReviewDomain import ProductReviewDomain

class ProductReviewRepository:
    def __init__(self, service: Annotated[ProductReviewService, Depends()]):
        self.service = service

    async def get_all(self) -> list[ProductReviewDomain | None]:
        response = await self.service.get_all()
        return [review.to_domain() for review in response]
    
    async def get_by_product_id_with_range(
        self,
        product_id: str, 
        start_date: Optional[datetime] = None, 
        end_date: Optional[datetime] = None
    ) -> list[ProductReviewDomain | None]:
        response = await self.service.get_by_product_id_with_range(product_id, start_date, end_date)
        return [review.to_domain() for review in response]
    
    async def get_by_user_id_with_range(
        self,
        user_id: str,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None
    ) -> list[ProductReviewDomain | None]:
        response = await self.service.get_by_user_id_with_range(user_id, start_date, end_date)
        return [review.to_domain() for review in response]