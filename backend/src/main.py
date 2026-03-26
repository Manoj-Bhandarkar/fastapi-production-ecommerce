from fastapi import FastAPI

app = FastAPI(title="FastAPI E-Commerce Backend")

@app.get("/")
def root():
    return {"message": "Welcome to the E-Commerce API"}
