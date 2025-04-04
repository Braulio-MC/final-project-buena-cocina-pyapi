from domain.model.recommenderDomain import RecommenderDomain
from core.constants import table_products

class ProductRecommenderNetwork(RecommenderDomain):

    def to_domain(self) -> RecommenderDomain:
        return RecommenderDomain(
            product_id=self.id,
            recommendations=self.recommendations
        )

    class Meta:
        collection_name = table_products
