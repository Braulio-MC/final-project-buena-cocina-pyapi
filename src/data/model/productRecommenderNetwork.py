from domain.model.recommenderDomain import RecommenderDomain


class ProductRecommenderNetwork(RecommenderDomain):

    def to_domain(self) -> RecommenderDomain:
        return RecommenderDomain(
            product_id=self.id,
            recommendations=self.recommendations
        )

    class Meta:
        collection_name = "products"
