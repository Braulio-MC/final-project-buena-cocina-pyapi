from pydantic import BaseModel

class InsightTopRatedStoreDomain(BaseModel):
    id: str
    name: str
    image: str
    avg_rating: float
    total_reviews: int