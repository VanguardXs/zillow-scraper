from fastapi import FastAPI
from api.routes import router
from database.db import init_db

app = FastAPI(
    title="Zillow Real Estate API",
    description="Real Estate Data from Zillow",
    version="1.0.0"
)

@app.on_event("startup")
def startup():
    init_db()

app.include_router(router)

@app.get("/")
def root():
    return {"message": "Zillow Scraper API is running 🚀"}