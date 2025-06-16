from fastapi import FastAPI
from app.api import platforms, products, scraping, regression

app = FastAPI()

app.include_router(platforms.router)
app.include_router(products.router)
app.include_router(scraping.router)
app.include_router(regression.router)
