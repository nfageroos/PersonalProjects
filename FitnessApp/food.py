import os
import pandas as pd
from models import init_db, SessionLocal, Food
from typing import Optional

CSV_PATH = os.path.join(os.path.dirname(__file__), "sr_legacy_foods.csv")


def load_foods():
    init_db()

    with SessionLocal() as session:
        if session.query(Food).first():
            print("Foods already loaded, skipping.")
            return

        print("Reading sr_legacy_foods.csv...")
        food_list = pd.read_csv(CSV_PATH).to_dict(orient="records")

        print(f"Adding {len(food_list)} foods to the database...")
        for row in food_list:
            food = Food(
                fdc_id=int(row["fdc_id"]),
                description=row["description"],
                calories=row.get("calories_kcal"),
                protein_g=row.get("protein_g"),
                fat_g=row.get("fat_g"),
                carbs_g=row.get("carbs_g"),
                fiber_g=row.get("fiber_g"),
            )
            session.add(food)

        session.commit()
        print(f"Done! {len(food_list)} foods loaded.")


def search_foods(query: str, limit: int = 20) -> list[dict]:
    #Return foods whose name contains the search
    with SessionLocal() as session:
        results = (
            session.query(Food)
            .filter(Food.description.ilike(f"%{query}%"))
            .limit(limit)
            .all()
        )
        return [food.to_dict() for food in results]


def get_food(fdc_id: int) -> Optional[dict]:
    #return food by ID
    with SessionLocal() as session:
        food = session.get(Food, fdc_id)
        return food.to_dict() if food else None
