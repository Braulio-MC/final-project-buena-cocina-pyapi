from pydantic import BaseModel
from typing import List, Optional


class DiscountItem(BaseModel):
    id: str
    percentage: float
    startDate: str
    endDate: str


class StoreItem(BaseModel):
    id: str
    name: str


class RecommendationItem(BaseModel):
    id: str
    name: str
    description: str
    image: str
    price: float
    available: bool
    store: StoreItem
    category: List[str]
    discount: Optional[DiscountItem] = None  # Puede ser None si no hay descuento
    rating: float
    totalRating: int
    totalReviews: int
    paginationKey: Optional[str] = None
    createdAt: str
    updatedAt: str



class RecommenderDomain(BaseModel):
    id: str
    recommendations: List[RecommendationItem]
