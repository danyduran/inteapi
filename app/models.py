from sqlalchemy import Column, Float, Integer, String, SmallInteger
from sqlalchemy.orm import validates

from database import BaseModel


class Restaurant(BaseModel):
    __tablename__ = "restaurants"

    id = Column(Integer, primary_key=True)
    rating = Column(SmallInteger, default=0)
    name = Column(String, nullable=False)
    site = Column(String, nullable=True)
    email = Column(String, nullable=False)
    phone = Column(String)
    street = Column(String)
    state = Column(String)
    city = Column(String)
    lat = Column(Float)
    lng = Column(Float)

    @validates("email")
    def validate_email(self, key, address):
        assert "@" in address
        return address
