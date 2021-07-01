from typing import Optional
from pydantic import BaseModel


class Restaurant(BaseModel):
    id: Optional[int] = None
    rating: int
    name: str
    site: str
    email: str
    phone: str
    street: str
    state: str
    city: str
    lat: str
    lng: str
