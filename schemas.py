from pydantic import BaseModel, Field
from typing import Optional, Dict, Any, List

class RecipeBase(BaseModel):
    cuisine: Optional[str] = None
    title: Optional[str] = None
    rating: Optional[float] = None
    prep_time: Optional[int] = None
    cook_time: Optional[int] = None
    total_time: Optional[int] = None
    description: Optional[str] = None
    nutrients: Optional[Dict[str, Any]] = None
    serves: Optional[str] = None

class RecipeOut(RecipeBase):
    id: int

    class Config:
        from_attributes = True

class PaginatedRecipes(BaseModel):
    page: int
    limit: int
    total: int
    data: List[RecipeOut]
