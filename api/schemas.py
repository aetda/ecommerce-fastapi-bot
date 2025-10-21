from pydantic import BaseModel


class ProductCreate(BaseModel):
    name: str
    price: float
    description: str
    category: str


class ProductResponse(ProductCreate):
    id: int

    model_config = {
        "from_attributes": True
    }

