from fastapi import FastAPI

from financial_app.users.service import user_service

app = FastAPI()

app.include_router(user_service.router)
