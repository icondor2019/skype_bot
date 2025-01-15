from fastapi import APIRouter

from app.controllers import (
    health_controller,
    skype_bot_controller
)

api_router = APIRouter()
api_router.include_router(health_controller.api)
api_router.include_router(skype_bot_controller.api)
