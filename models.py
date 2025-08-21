from sqlalchemy import Column, Integer, Float, String
from sqlalchemy.dialects.postgresql import JSONB
from .database import Base

class Recipe(Base):
    __tablename__ = "recipes"

    id = Column(Integer, primary_key=True, index=True)
    cuisine = Column(String(255), nullable=True, index=True)
    title = Column(String(255), nullable=True, index=True)
    rating = Column(Float, nullable=True, index=True)
    prep_time = Column(Integer, nullable=True)
    cook_time = Column(Integer, nullable=True)
    total_time = Column(Integer, nullable=True, index=True)
    description = Column(String, nullable=True)
    nutrients = Column(JSONB, nullable=True)  # stores string values like "389 kcal"
    serves = Column(String(50), nullable=True)
