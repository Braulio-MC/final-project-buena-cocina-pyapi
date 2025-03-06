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
import nltk
from routes.recommendationsRoutes import router as recommendation_product_router
from routes.botRoutes import api_router as bot_query

load_dotenv()

# Descargar WordNet y su base de datos en español para el bot
nltk.download("wordnet")
nltk.download("omw-1.4")



@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[None]:
    REDIS_CACHE_PREFIX = "fastapi-cache"
    REDIS_SERVER_URL = os.getenv("REDIS_SERVER_URL", "redis://localhost:6379")
    try:
        redis = aioredis.from_url(REDIS_SERVER_URL, encoding="utf-8", decode_responses=True)
        FastAPICache.init(RedisBackend(redis), prefix=REDIS_CACHE_PREFIX)
        print("✅ Redis cache inicializado correctamente")
    except Exception as e:
        print(f"⚠️ No se pudo conectar a Redis: {e}")

    yield  # Continúa ejecutando FastAPI sin bloquear por Redis

fireo.connection(client=db)
app = FastAPI(lifespan=lifespan)

app.include_router(store_review_router, tags=["store_reviews"])
app.include_router(product_review_router, tags=["product_reviews"])
app.include_router(insight_router, tags=["insights"])
app.include_router(recommendation_product_router, tags=["product_recommendation"])
app.include_router(bot_query, tags=['ask'])
