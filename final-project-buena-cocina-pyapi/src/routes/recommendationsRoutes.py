from fastapi import APIRouter
from controllers.recommenderController import router as product_controller

router = APIRouter()
router.include_router(product_controller)