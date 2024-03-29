
from pydantic import BaseModel
from fastapi import FastAPI, HTTPException

class Item(BaseModel):
    name: str
    description: str = None
    price: float
    tax: float = 0.1

class User(BaseModel):
    name: str
    age: int
    is_active: bool = True

# Creating an instance of the User model
user = User(name="John Doe", age=30)

print(user)


app = FastAPI()

@app.post("/items/")
async def create_item(item: Item):
    return {"name": item.name, "price": item.price}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)