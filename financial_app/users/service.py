from fastapi import FastAPI

from financial_app.users.routers import router

user_service = FastAPI()

user_service.include_router(router)
