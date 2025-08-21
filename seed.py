import json, os, re
from sqlalchemy.orm import Session
from .database import SessionLocal, engine, Base
from .models import Recipe
from .utils import parse_number_or_none

def clean_numeric(v):
    num = parse_number_or_none(v)
    return None if num is None else int(num) if float(num).is_integer() else float(num)

def load_json(path: str):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def normalize_record(rec: dict) -> dict:
    # Ensure required keys exist even if null
    def to_null_if_nan(x):
        n = parse_number_or_none(x)
        return None if n is None else n

    return {
        "cuisine": rec.get("cuisine"),
        "title": rec.get("title"),
        "rating": to_null_if_nan(rec.get("rating")),
        "prep_time": int(to_null_if_nan(rec.get("prep_time"))) if to_null_if_nan(rec.get("prep_time")) is not None else None,
        "cook_time": int(to_null_if_nan(rec.get("cook_time"))) if to_null_if_nan(rec.get("cook_time")) is not None else None,
        "total_time": int(to_null_if_nan(rec.get("total_time"))) if to_null_if_nan(rec.get("total_time")) is not None else None,
        "description": rec.get("description"),
        "nutrients": rec.get("nutrients") or {},
        "serves": rec.get("serves"),
    }

def seed(db: Session, json_path: str):
    data = load_json(json_path)
    if isinstance(data, dict):
        data = [data]
    records = [normalize_record(d) for d in data]
    db.bulk_insert_mappings(Recipe, records)
    db.commit()

if __name__ == "__main__":
    Base.metadata.create_all(bind=engine)
    json_path = os.environ.get("RECIPES_JSON", "/app/data/recipes.json")
    with SessionLocal() as db:
        seed(db, json_path)
    print("Seed complete.")
