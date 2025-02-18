import fireo
import os
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from redis import asyncio as aioredis
from core.constants import REDIS_CACHE_PREFIX
from routes.storeReviewRoutes import router as store_review_router
from routes.productReviewRoutes import router as product_review_router
from routes.insightRoutes import router as insight_router
from core.firebaseHelper import db

load_dotenv()

@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[None]:
    redis = aioredis.from_url(os.getenv("REDIS_SERVER_URL"))
    FastAPICache.init(RedisBackend(redis), prefix=REDIS_CACHE_PREFIX)
    yield

fireo.connection(client=db)
app = FastAPI(lifespan=lifespan)

app.include_router(store_review_router, tags=["store_reviews"])
app.include_router(product_review_router, tags=["product_reviews"])
app.include_router(insight_router, tags=["insights"])
