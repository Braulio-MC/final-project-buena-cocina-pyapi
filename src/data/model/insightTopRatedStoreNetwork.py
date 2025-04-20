from pydantic import BaseModel
from google.cloud.bigquery.table import Row
from domain.model.insightTopRatedStoreDomain import InsightTopRatedStoreDomain

class InsightTopRatedStoreNetwork(BaseModel):
    id: str
    name: str
    image: str
    avg_rating: float
    total_reviews: int

    @staticmethod
    def from_bq_row(row: Row) -> 'InsightTopRatedStoreNetwork':
        return InsightTopRatedStoreNetwork(
            id=row['store_id'],
            name=row['store_name'],
            image=row['store_image'],
            avg_rating=row['store_avg_rating'],
            total_reviews=row['store_total_reviews']
        )
    
    def to_domain(self) -> InsightTopRatedStoreDomain:
        return InsightTopRatedStoreDomain(
            id=self.id,
            name=self.name,
            image=self.image,
            avg_rating=self.avg_rating,
            total_reviews=self.total_reviews
        )