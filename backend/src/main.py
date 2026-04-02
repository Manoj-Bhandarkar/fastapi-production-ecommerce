from fastapi import FastAPI
from src.account.routers import router as account_router
from src.product.routers.category import router as category_router
app = FastAPI(title="FastAPI E-Commerce Backend")

@app.get("/")
def root():
    return {"message": "Welcome to the E-Commerce API"}

app.include_router(account_router, prefix="/api/account", tags=["Account"])
app.include_router(category_router, prefix="/api/products/category", tags=["categories"])