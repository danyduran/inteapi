from fastapi import FastAPI, Depends, HTTPException
from starlette.responses import RedirectResponse

from sqlalchemy.orm import Session

from database import make_migrations, get_db

from dummy_data import load_dummy_data

from models import Restaurant


make_migrations()
load_dummy_data()
app = FastAPI()


@app.get("/")
def index():
    return RedirectResponse(url="/docs/")


@app.get("/api/restaurants", status_code=200)
def get_all_resturants(db: Session = Depends(get_db)):
    records = db.query(Restaurant).all()
    return records


@app.get("/api/restaurants/{restaurant_id}", status_code=200)
def get_restaurant_by_id(
        restaurant_id: int,
        db: Session = Depends(get_db)):

    restaurant = db.query(Restaurant).filter_by(id=restaurant_id).first()
    if restaurant:
        return restaurant

    raise HTTPException(status_code=404, detail="Restaurant not found")
