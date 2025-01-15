from fastapi import FastAPI
from mangum import Mangum
from app.configuration.settings import settings
from app.controllers import api_router
from contextlib import asynccontextmanager


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Starting app...")
    yield
    print("Closing app...")

app = FastAPI(root_path='/skype/bot',
              title='bot skype service',
              version='1.0.0',
              description='skype bot service',
              docs_url=settings.OPEN_API_PATH,
              openapi_url=settings.OPEN_API_JSON,
              lifespan=lifespan
              )

handler = Mangum(app)

def setup_application():
    app.include_router(api_router)

setup_application()