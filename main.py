from bson import ObjectId
from fastapi import FastAPI, HTTPException
from mongo_config import MongoConfig
from models import Car
from pymongo.errors import DuplicateKeyError

app = FastAPI()
mongo_config = MongoConfig()
db = mongo_config.get_database()
cars_collection = db.cars

@app.post("/cars")
def create_car(car: Car):
    try:
        car_dict = car.model_dump()
        result = cars_collection.insert_one(car_dict)
        return {"message": "Car created successfully", "id": str(result.inserted_id)}
    except DuplicateKeyError:
        raise HTTPException(status_code=400, detail="Car with this description already exists")

@app.get("/cars")
def get_cars():
    cars = list(cars_collection.find({}, {"_id": 0, "id": {"$toString": "$_id"}, "description": 1}))
    return {"cars": cars}

@app.get("/cars/{car_id}")
def get_car_by_id(car_id: str):
    car = cars_collection.find_one({"_id": ObjectId(car_id)}, {"_id": 0, "id": {"$toString": "$_id"}, "description": 1})
    if car is None:
        raise HTTPException(status_code=404, detail="Car not found")
    return car

@app.delete("/cars/{car_id}")
def delete_car_by_id(car_id: str):
    result = cars_collection.delete_one({"_id": ObjectId(car_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Car not found")
    return {"message": "Car deleted successfully"}