from fastapi import Depends
from datetime import datetime
from typing import Annotated, Optional
from data.service.storeReviewService import StoreReviewService
from domain.model.storeReviewDomain import StoreReviewDomain

class StoreReviewRepository:
    def __init__(self, service: Annotated[StoreReviewService, Depends()]):
        self.service = service

    async def get_all(self) -> list[StoreReviewDomain | None]:
        response = await self.service.get_all()
        return [review.to_domain() for review in response]
    
    async def get_by_store_id_with_range(
        self,
        store_id: str, 
        start_date: Optional[datetime] = None, 
        end_date: Optional[datetime] = None
    ) -> list[StoreReviewDomain | None]:
        response = await self.service.get_by_store_id_with_range(store_id, start_date, end_date)
        return [review.to_domain() for review in response]
    
    async def get_by_user_id_with_range(
        self,
        user_id: str, 
        start_date: Optional[datetime] = None, 
        end_date: Optional[datetime] = None
    ) -> list[StoreReviewDomain | None]:
        response = await self.service.get_by_user_id_with_range(user_id, start_date, end_date)
        return [review.to_domain() for review in response]