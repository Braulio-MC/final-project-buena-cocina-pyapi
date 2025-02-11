import fireo
from fastapi import FastAPI
from routes.storeReviewRoutes import router as store_review_router
from routes.productReviewRoutes import router as product_review_router
from routes.recommendationsRoutes import router as recommendation_product_router
from core.firebaseHelper import db

fireo.connection(client=db)
app = FastAPI()

app.include_router(store_review_router, tags=["store_reviews"])
app.include_router(product_review_router, tags=["product_reviews"])
app.include_router(recommendation_product_router, tags=["product_recommendation"])

if __name__ == '__main__':
    pass
