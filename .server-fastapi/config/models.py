from pydantic import BaseModel

class Item(BaseModel):
    name: str
    description: str
    price: float
    quantity: int

class ItemResponse(Item):
    id: int
