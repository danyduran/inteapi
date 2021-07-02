import pandas as pd

from database import SessionLocal
from models import Restaurant


def load_dummy_data():
    try:
        session = SessionLocal()
        records_restaurant_in_db = session.query(Restaurant).all()
        if not records_restaurant_in_db:
            restaurant_df = pd.read_csv("./restaurantes.csv")
            restaurant_objs = []
            for index, row in restaurant_df.iterrows():
                restaurant = Restaurant(
                    name=row["name"],
                    rating=row["rating"],
                    site=row["site"],
                    email=row["email"],
                    phone=row["phone"],
                    street=row["street"],
                    city=row["city"],
                    state=row["state"],
                    lat=row["lat"],
                    lng=row["lng"]
                )
                restaurant_objs.append(restaurant)
            session.add_all(restaurant_objs)
            session.commit()
    except Exception:
        session.rollback()
    finally:
        session.close()
