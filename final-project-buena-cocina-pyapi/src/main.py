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
from routes.recommendationsRoutes import router as recommendation_product_router
from routes.botRoutes import api_router as bot_query
from data.service.indexing import refresh_faiss_index_products, refresh_faiss_index_stores
from  data.service.refreshIndex import periodic_faiss_refresh
import asyncio

load_dotenv()


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[None]:
    REDIS_SERVER_URL = os.getenv("REDIS_SERVER_URL", "redis://localhost:6379")
    try:
        redis = aioredis.from_url(REDIS_SERVER_URL, encoding="utf-8", decode_responses=True)
        FastAPICache.init(RedisBackend(redis), prefix=REDIS_CACHE_PREFIX)
        print("Redis cache inicializado correctamente")
    except Exception as e:
        print(f"No se pudo conectar a Redis: {e}")

        # Construir el índice FAISS al iniciar
    try:
        refresh_faiss_index_products()
        refresh_faiss_index_stores()
        print("Índice FAISS de productos generado correctamente al iniciar.")
    except Exception as e:
        print(f"Error al generar índice FAISS de productos: {e}")

    # Tarea de refresco periódico
    asyncio.create_task(periodic_faiss_refresh(interval_seconds=3600))  # cada hora

    yield  # Continúa ejecutando FastAPI sin bloquear por Redis


fireo.connection(client=db)
app = FastAPI(lifespan=lifespan)

app.include_router(store_review_router, tags=["store_reviews"])
app.include_router(product_review_router, tags=["product_reviews"])
app.include_router(insight_router, tags=["insights"])
app.include_router(recommendation_product_router, tags=["product_recommendation"])
app.include_router(bot_query, tags=['ask'])