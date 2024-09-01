from fastapi import FastAPI
import uvicorn

# Create an instance of FastAPI
app = FastAPI()

# Define a simple route
@app.get("/")
def read_root():
    return {"message": "Hello, World!"}

# Define another route with a path parameter
@app.get("/items/{item_id}")
def read_item(item_id: int, q: str = None):
    return {"item_id": item_id, "query": q}