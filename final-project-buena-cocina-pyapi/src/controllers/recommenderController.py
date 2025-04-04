from fastapi import Depends
from typing import Annotated
from domain.repository.recommenderRepository import RecommenderRespository

class RecommenderController:
    def __init__(self, repository: Annotated[RecommenderRespository, Depends()]):
        self.repository = repository

    async def get_recommendations(
            self,
            product_id: str,
            top_n: int = 5
    ):
        # Limpiar el ID eliminando espacios y caracteres especiales
        product_id = product_id.strip()

        return await self.repository.get_recommendations(
            product_id, top_n)

