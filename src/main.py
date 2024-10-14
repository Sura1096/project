from fastapi import FastAPI

from src.api.v1.routers.company import company_router

app = FastAPI()
app.include_router(company_router)
