from sqlmodel import SQLModel, Field
from pydantic import BaseModel
from typing import Optional


class PropertyParameters(BaseModel):
    longitude: float
    latitude: float
    housing_median_age: float
    total_rooms: float
    total_bedrooms: float
    population: float
    households: float
    median_income: float
    ocean_proximity: str
    median_house_value: Optional[float] = None

    class Config:
        json_schema_extra = {
            'example': {
                'longitude': 0.0,
                'latitude': 0.0,
                'housing_median_age': 0.0,
                'total_rooms': 0.0,
                'total_bedrooms': 0.0,
                'population': 0.0,
                'households': 0.0,
                'median_income': 0.0,
                'ocean_proximity': '',
                'median_house_value': 0.0
            }
        }


class Prediction(PropertyParameters, SQLModel, table=True):
    id: int = Field(primary_key=True, index=True)
    predicted_house_value: float
