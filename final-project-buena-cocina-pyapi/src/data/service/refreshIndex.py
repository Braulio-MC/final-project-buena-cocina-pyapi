import asyncio
from data.service.indexing import refresh_faiss_index_products, refresh_faiss_index_stores

async def periodic_faiss_refresh(interval_seconds: int = 3600):
    while True:
        try:
            print("Refrescando índice FAISS de productos...")
            refresh_faiss_index_products()
            refresh_faiss_index_stores()
            print("Índice FAISS actualizado.")
        except Exception as e:
            print(f"Error al refrescar índice FAISS: {e}")
        await asyncio.sleep(interval_seconds)