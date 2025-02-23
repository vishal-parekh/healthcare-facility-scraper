from pydantic import BaseModel

class Product(BaseModel):
    service_name: str
    service_description: str
    service_price: str