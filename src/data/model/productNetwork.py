from pydantic import BaseModel
from typing import Optional, List

class Product(BaseModel):
    id: str
    name: str
    description: str
    image: str
    price: float
    available: bool
    store: str
    category: str
    discount: Optional[float]
    rating: float
    review_count: int
    created_at: str
    updated_at: str
    embedding: Optional[List[float]] = None