from enum import Enum
from typing import Union

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()


class Item(BaseModel):
    name: str
    price: float
    is_offer: Union[bool, None] = None


class Car(str, Enum):
    toyota = "toyota"
    honda = "honda"


class BackupStatus(BaseModel):
    status: str
    last_backup: str | None = None
    size: str | None = None
    error_message: str | None = None


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.post("/status/create")
def create_status(status: BackupStatus):
    print(f"Posted status is: {type(status)}")
    status_dict = status.dict()
    print(f"Posted status is: {type(status_dict)}")
    if status.last_backup is not None:
        status_dict.update({"New": False})
    return status_dict


fake_items_db = [{"item_name": "Foo"}, {"item_name": "Bar"}, {"item_name": "Baz"}]


@app.get("/items/")
def read_items(skip: int = 0, limit: int = 10):
    return fake_items_db[skip : skip + limit]


@app.get("/items/{item_id}")
def read_item(item_id: str, q: str | None = None, short: bool = False):
    item = {"item_id": item_id}
    if q:
        item.update({"q": q})
    if not short:
        item.update(
            {"description": "This is an amazing item that has a long description"}
        )
    return item


# def read_item(item_id: int, q: Union[str, None] = None):
# return {"item_id": item_id, "q": q}


@app.put("/items/{item_id}")
def update_item(item_id: int, item: Item):
    return {"item_name": item.name, "item_id": item_id}


@app.get("/cars/{car}")
async def read_cars(car: Car):
    if car is car.toyota:
        return {"car": car, "message": "Toyota message"}
    elif car is car.honda:
        return {"car": car, "message": "Honda message"}
    # If the car is not recognized, raise an HTTPException
    raise HTTPException(status_code=404, detail="Car not found")
