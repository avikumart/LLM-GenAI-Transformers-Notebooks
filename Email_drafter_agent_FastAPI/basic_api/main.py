from fastapi import FastAPI, HTTPException, Query, Path
from pydantic import BaseModel, Field
from typing import Optional, List

# initialize FastAPI app
app = FastAPI(title="Basic CRUD API", description="A simple CRUD API example", version="1.0")

# in memory database
items_db = {}

# pydantic data validation model for the input data
class Item(BaseModel):
    id: int = Field(...,title="ID of the item")
    name: str = Field(..., title="Name of the item", max_length=50)
    description: Optional[str] = Field(None, title="Description of the item")
    price: float = Field(..., title="Price of the item", gt=0)
    quantity: int = Field(..., title="Quantity of the item", ge=0)

# get first server check api 
@app.get("/")
def read_root():
    return {"message":"Welcome to the Basic CRUD API"}

# Create the post api endpoint to add item in the database
@app.post("/items/", response_model=Item, status_code=201)
def create_item(item_id: int, item: Item):
    if item_id in items_db:
        raise HTTPException(status_code=400, detail="Item already exists")
    items_db[item_id] = item
    return item

# read all the items of the database
@app.get("/items", response_model=List[Item])
def get_items():
    if not items_db:
        raise HTTPException(status_code=404, detail="No items found")
    return list(items_db.values())

# get certain item from the db
@app.get("/items/{item_id}", response_model=Item)
def get_item(item_id: int):
    if item_id not in items_db:
        raise HTTPException(status_code=404, detail="item not found")
    return items_db[item_id]

# update the item inn the database 
@app.put("/items/{item_id}", response_model=Item)
def update_item(item_id: int, item:Item):
    if item_id not in items_db:
        raise HTTPException(status_code=404, detail="item not found")
    items_db[item_id] = item
    return item

# delete the item from the database
@app.delete("/items/{item_id}", response_model=dict)
def delete_item(item_id: int):
    if item_id not in items_db:
        raise HTTPException(status_code=404, detail="item not found")
    del items_db[item_id]
    return {"message": "Item deleted successfully"} 