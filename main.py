from fastapi import FastAPI, Depends, Query, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
from sqlalchemy import func, text, select, desc, and_
from typing import Optional

from .database import Base, engine, get_db
from .models import Recipe
from .schemas import RecipeOut, PaginatedRecipes
from .utils import parse_op_value

app = FastAPI(title="Recipes API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve static frontend
app.mount("/", StaticFiles(directory="app/static", html=True), name="static")

@app.on_event("startup")
def on_startup():
    Base.metadata.create_all(bind=engine)

def calories_int_expr():
    # Extract digits from JSONB nutrients->>'calories', e.g., "389 kcal" -> 389
    return text("(regexp_replace((recipes.nutrients->>'calories'), '\\D', '', 'g'))::int")

@app.get("/api/recipes", response_model=PaginatedRecipes)
def get_recipes(
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db),
):
    q = db.query(Recipe).order_by(desc(Recipe.rating.nullslast()))
    total = q.count()
    items = q.offset((page - 1) * limit).limit(limit).all()
    return {"page": page, "limit": limit, "total": total, "data": items}

@app.get("/api/recipes/search")
def search_recipes(
    calories: Optional[str] = None,
    title: Optional[str] = None,
    cuisine: Optional[str] = None,
    total_time: Optional[str] = None,
    rating: Optional[str] = None,
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db),
):
    query = db.query(Recipe)

    # Title partial match
    if title:
        query = query.filter(Recipe.title.ilike(f"%{title}%"))
    if cuisine:
        query = query.filter(Recipe.cuisine.ilike(f"%{cuisine}%"))

    # Numeric filters with operators
    if total_time:
        op, val = parse_op_value(total_time)
        if val is None:
            raise HTTPException(status_code=400, detail="Invalid total_time filter")
        col = Recipe.total_time
        if op == ">=": query = query.filter(col >= val)
        elif op == "<=": query = query.filter(col <= val)
        elif op == ">": query = query.filter(col > val)
        elif op == "<": query = query.filter(col < val)
        else: query = query.filter(col == val)

    if rating:
        op, val = parse_op_value(rating)
        if val is None:
            raise HTTPException(status_code=400, detail="Invalid rating filter")
        col = Recipe.rating
        if op == ">=": query = query.filter(col >= val)
        elif op == "<=": query = query.filter(col <= val)
        elif op == ">": query = query.filter(col > val)
        elif op == "<": query = query.filter(col < val)
        else: query = query.filter(col == val)

    if calories:
        op, val = parse_op_value(calories)
        if val is None:
            raise HTTPException(status_code=400, detail="Invalid calories filter")
        cal_expr = calories_int_expr()
        if op == ">=": query = query.filter(cal_expr >= val)
        elif op == "<=": query = query.filter(cal_expr <= val)
        elif op == ">": query = query.filter(cal_expr > val)
        elif op == "<": query = query.filter(cal_expr < val)
        else: query = query.filter(cal_expr == val)

    total = query.count()
    items = query.order_by(desc(Recipe.rating.nullslast())).offset((page - 1)*limit).limit(limit).all()
    return {"page": page, "limit": limit, "total": total, "data": items}
