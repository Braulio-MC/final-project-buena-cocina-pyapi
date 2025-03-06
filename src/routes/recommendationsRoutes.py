from fastapi import APIRouter, HTTPException
from data.service.recommenderService import RecommenderService


router = APIRouter()
recommender_service = RecommenderService()


@router.get("/productos/{product_id}")
async def get_recommendations(product_id: str, top_n: int = 10):
    """Devuelve productos recomendados para un ID dado."""
    try:
        print(f"Producto recibido: {product_id}")
        recommendations = await recommender_service.get_recommendations(product_id, top_n)
        return {"recommendations": recommendations}
    except ValueError as e:
        print(f"Error de valor: {e}")
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        print(f"Error inesperado: {e}")
        raise HTTPException(status_code=500, detail="Error interno del servidor")



