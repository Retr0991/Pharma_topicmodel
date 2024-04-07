from fastapi import FastAPI, HTTPException
from pymongo import MongoClient
import os
from dotenv import load_dotenv
load_dotenv()
password = os.getenv("PASS")

app = FastAPI()

def remove_indexing(text):
    # Find the index of the first space
    index = text.find('_')
    # Check if there's an underscore and if the text before it is a number
    if index != -1 and text[:index].isdigit():
        # If so, return the text after the underscore
        return text[index+1:]
    # Otherwise, return the original text
    return text

# Connect to MongoDB
client = MongoClient(f'mongodb+srv://retr0991:{password}@cluster0.rtkjeyb.mongodb.net/')
# client = MongoClient('mongodb://localhost:27017/')
db = client['clinicalsentix']
collection = db['test']

# Endpoint to get all items
@app.get("/items/")
async def read_items():
    items = list(collection.find_one({}, {"_id": 0}))  # Exclude _id field from response
    return items

# Endpoint to get a single item by ID
@app.get("/items/{item_name}")    
async def read_item(item_name: str):
    drugName = item_name
    items = collection.find_one({}, {"_id": 0})
    try:
        # Dict
        item = items[drugName]
        new_data = {"topic" : [], "tweets": []}
        for key, value in item.items():
            name = remove_indexing(value["name"])
            count = value["count"]
            tweet = list(value["tweet"].values())
            if(key != "topic_number_-1"):
                new_data["topic"].append({"name": name, "count": count})
                new_data["tweets"].append({"topic_name": name, "tweets": tweet})
    except KeyError:
        raise HTTPException(status_code=404, detail=f"{drugName} not found")
    return new_data