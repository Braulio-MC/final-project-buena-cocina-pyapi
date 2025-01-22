from data.model.productReviewNetwork import ProductReviewNetwork
from datetime import datetime, timezone
from typing import Optional

class ProductReviewService:
    def __init__(self):
        pass

    async def get_all(self) -> list[ProductReviewNetwork | None]:
        product_reviews = ProductReviewNetwork.collection.fetch()
        return list(product_reviews)
    
    async def get_by_product_id_with_range(
        self,
        product_id: str,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None
    ) -> list[ProductReviewNetwork | None]:
        product_reviews = ProductReviewNetwork.collection.filter(product_id=product_id)
        if start_date:
            start_date = start_date.replace(tzinfo=timezone.utc)
            product_reviews = product_reviews.filter('created_at', '>=', start_date)
        if end_date:
            end_date = end_date.replace(tzinfo=timezone.utc)
            product_reviews = product_reviews.filter('created_at', '<=', end_date)
        product_reviews = product_reviews.fetch()
        return list(product_reviews)
    
    async def get_by_user_id_with_range(
        self,
        user_id: str,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None
    ) -> list[ProductReviewNetwork | None]:
        product_reviews = ProductReviewNetwork.collection.filter(user_id=user_id)
        if start_date:
            start_date = start_date.replace(tzinfo=timezone.utc)
            product_reviews = product_reviews.filter('created_at', '>=', start_date)
        if end_date:
            end_date = end_date.replace(tzinfo=timezone.utc)
            product_reviews = product_reviews.filter('created_at', '<=', end_date)
        product_reviews = product_reviews.fetch()
        return list(product_reviews)