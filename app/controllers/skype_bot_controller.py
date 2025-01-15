from fastapi import APIRouter, HTTPException, Header, Body
from app.services.skype_bot_service import lambda_handler

api = APIRouter()

@api.post(path="/v1/skype/webhook")
def get_available_products(event = Body(...)):
    print(event)
    response = lambda_handler(event, context=None)
    if response is None:
        raise HTTPException(status_code=404, detail='Error executing skype bot')
    return response
