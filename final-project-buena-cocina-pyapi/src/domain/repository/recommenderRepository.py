from fastapi import Depends
from typing import Annotated
from domain.model.recommenderDomain import RecommenderDomain, RecommendationItem
from data.service.recommenderService import RecommenderService

class RecommenderRespository:
    def __init__(self, service: Annotated[RecommenderService, Depends()]):
        self.service = service

    async def get_recommendations(
            self, product_id: str, top_n: int = 5,
    ) -> RecommenderDomain:
        raw_recommendations = await self.service.get_recommendations(
            product_id, top_n)

        recommendations = [RecommendationItem(**item) for item in raw_recommendations]
        return RecommenderDomain(id=product_id, recommendations=recommendations)
