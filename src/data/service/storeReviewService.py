from data.model.storeReviewNetwork import StoreReviewNetwork
from datetime import datetime, timezone
from typing import Optional

class StoreReviewService:
    def __init__(self):
        pass

    async def get_all(self) -> list[StoreReviewNetwork | None]:
        store_reviews = StoreReviewNetwork.collection.fetch()
        return list(store_reviews)

    async def get_by_store_id_with_range(
        self,
        store_id: str,
        start_date: Optional[datetime] = None, 
        end_date: Optional[datetime] = None
    ) -> list[StoreReviewNetwork | None]:
        store_reviews = StoreReviewNetwork.collection.filter(store_id=store_id)
        if start_date:
            start_date = start_date.replace(tzinfo=timezone.utc)
            store_reviews = store_reviews.filter('created_at', '>=', start_date)
        if end_date:
            end_date = end_date.replace(tzinfo=timezone.utc)
            store_reviews = store_reviews.filter('created_at', '<=', end_date)
        store_reviews = store_reviews.fetch()
        return list(store_reviews)
    
    async def get_by_user_id_with_range(
        self, 
        user_id: str, 
        start_date: Optional[datetime] = None, 
        end_date: Optional[datetime] = None
    ) -> list[StoreReviewNetwork | None]:
        store_reviews = StoreReviewNetwork.collection.filter(user_id=user_id)
        if start_date:
            start_date = start_date.replace(tzinfo=timezone.utc)
            store_reviews = store_reviews.filter('created_at', '>=', start_date)
        if end_date:
            end_date = end_date.replace(tzinfo=timezone.utc)
            store_reviews = store_reviews.filter('created_at', '<=', end_date)
        store_reviews = store_reviews.fetch()
        return list(store_reviews)
