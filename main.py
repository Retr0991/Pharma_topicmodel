from fastapi import FastAPI, HTTPException
from pymongo import MongoClient

app = FastAPI()

# Connect to MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client['test']
collection = db['test']

# Endpoint to get all items
@app.get("/items/")
async def read_items():
    items = list(collection.find())
    return items

# Endpoint to get a single item by ID
@app.get("/items/{item_id}")    
async def read_item(item_id: str):
    item = collection.find_one({"_id": item_id})
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return item

# Endpoint to update an item
@app.put("/items/{item_id}")
async def update_item(item_id: str, new_item: dict):
    updated_item = collection.find_one_and_update(
        {"_id": item_id}, {"$set": new_item}, return_document=True
    )
    if updated_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return updated_item
