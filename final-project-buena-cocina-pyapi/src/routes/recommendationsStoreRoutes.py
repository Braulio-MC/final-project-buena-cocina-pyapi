from fastapi import APIRouter
from controllers.recommenderStoreController import router as store_controller

router = APIRouter()
router.include_router(store_controller)