from pydantic import BaseModel
from typing import List, Dict, Any

class RecommenderDomain(BaseModel):
    product_id: str
    recommendations: List[Dict[str, Any]]