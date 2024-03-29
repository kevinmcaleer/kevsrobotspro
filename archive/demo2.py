from pydantic import BaseModel
from fastapi import FastAPI, HTTPException

class Item(BaseModel):
    name: str
    description: str = None
    price: float
    in_stock: bool = True

# This will act as our fake database
items_db = {}

app = FastAPI()

@app.post("/items/")
async def create_item(item: Item):
    if item.name in items_db:
        raise HTTPException(status_code=400, detail="Item already exists")
    items_db[item.name] = item
    return item

@app.get("/items/{item_name}")
async def read_item(item_name: str):
    if item_name not in items_db:
        raise HTTPException(status_code=404, detail="Item not found")
    return items_db[item_name]

@app.put("/items/{item_name}")
async def update_item(item_name: str, item: Item):
    if item_name not in items_db:
        raise HTTPException(status_code=404, detail="Item not found")
    items_db[item_name] = item
    return item

@app.delete("/items/{item_name}")
async def delete_item(item_name: str):
    if item_name not in items_db:
        raise HTTPException(status_code=404, detail="Item not found")
    del items_db[item_name]
    return {"message": "Item deleted successfully"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)