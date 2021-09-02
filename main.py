from fastapi import FastAPI, Depends, HTTPException, status
from starlette.responses import RedirectResponse

from sqlalchemy.orm import Session

from database import make_migrations, get_db

from dummy_data import load_dummy_data

from models import Restaurant
from schemas import Restaurant as RestaurantSchema


make_migrations()
load_dummy_data()
app = FastAPI()


@app.get("/")
def index():
    return RedirectResponse(url="/docs/")


@app.get("/api/restaurants", status_code=200)
def get_all_resturants(db: Session = Depends(get_db)):
    """Get all records of restaurant in db.

    Args:

    Returns:
      All saved records of restaurant in db.
    """
    return db.query(Restaurant).all()


@app.get("/api/restaurants/{restaurant_id}", status_code=status.HTTP_200_OK)
def get_restaurant_by_id(
        restaurant_id: int,
        db: Session = Depends(get_db)):
    """Get one record of restaurant in db, getting by id.

    Args:
      restaurant_id: specific id of restaurant record.

    Returns:
      One specific saved record of restaurant in db, filtered by id.
    """
    restaurant = db.query(Restaurant).filter_by(id=restaurant_id).first()
    if restaurant:
        return restaurant

    raise HTTPException(status_code=404, detail="Restaurant not found")


@app.post("/api/restaurants", status_code=status.HTTP_201_CREATED)
def create_new_restaurant(
        restaurant: RestaurantSchema,
        db: Session = Depends(get_db)):
    """Create one record of restaurant.

    Args:
      restaurant: json that contains the next params(name,
        rating, site, email, phone, state, city, lat, lng).

    Returns:
      A new saved record of restaurant in db.
    """
    new_restaurant = Restaurant(
        rating=restaurant.rating,
        name=restaurant.name,
        email=restaurant.email,
        site=restaurant.site,
        phone=restaurant.phone,
        street=restaurant.street,
        city=restaurant.city,
        state=restaurant.street,
        lat=restaurant.lat,
        lng=restaurant.lng
    )
    try:
        db.add(new_restaurant)
        db.commit()
        db.refresh(new_restaurant)
    except Exception:
        db.rollback()
        raise HTTPException(
            status_code=409,
            detail="Have had an error"
        )
    return new_restaurant


def update_record_restaurant(restaurant_id, restaurant, db):
    restaurant_record = db.query(Restaurant).filter_by(
        id=restaurant_id
    ).first()
    if restaurant_record:
        try:
            new_values = restaurant.dict()
            del new_values["id"]
            for key, value in new_values.items():
                setattr(restaurant_record, key, value)
            db.commit()
            db.refresh(restaurant_record)
            return restaurant_record
        except Exception:
            db.rollback()
            raise HTTPException(
                status_code=409,
                detail="Have had an error while updating the record"
            )
    raise HTTPException(status_code=404, detail="Restaurant not found")


@app.put("/api/restaurants/{restaurant_id}")
def update_complete_restaurant(
        restaurant_id: int,
        restaurant: RestaurantSchema,
        db: Session = Depends(get_db)):
    """Updated one specific record of restaurant.

    Args:
      restaurant_id: id from restaurant
      restaurant: json that contains the next params(name,
        rating, site, email, phone, state, city, lat, lng).

    Returns:
      A updated record of restaurant in db.
    """
    return update_record_restaurant(restaurant_id, restaurant, db)


@app.patch("/api/restaurants/{restaurant_id}")
def update_partial_restaurant(
        restaurant_id: int,
        restaurant: RestaurantSchema,
        db: Session = Depends(get_db)):
    """Updated one specific record of restaurant.

    Args:
      restaurant_id: id from restaurant
      restaurant: json that contains the next params(name,
        rating, site, email, phone, state, city, lat, lng).

    Returns:
      A updated record of restaurant in db.
    """
    return update_record_restaurant(restaurant_id, restaurant, db)


@app.delete("/api/restaurants/{restaurant_id}", status_code=204)
def delete_a_restaurant(
        restaurant_id: int,
        db: Session = Depends(get_db)):
    """Deleted one specific record of restaurant, filtered by id .

    Args:
      restaurant_id: id from restaurant

    Returns:
       msg: saying that record was deleted sucessfully.
    """
    restaurant_record = db.query(Restaurant).filter_by(
        id=restaurant_id
    )
    if restaurant_record.first():
        restaurant_record.delete()
        db.commit()
        return {"detail": "Resource has been deleted sucessfully"}
    raise HTTPException(status_code=404, detail="Restaurant not found")
