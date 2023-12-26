from typing import List
from enum import Enum
from sqlmodel import SQLModel, UniqueConstraint
from pydantic import BaseModel


class InputType(Enum):
    CSV = "csv"
    JSON = "json"


class TrainingData(BaseModel, SQLModel, table=True):
    training_columns: List[str]
    column_to_be_predicted: str
    model_name: str
    input_file_type: InputType
    input_file_name: str
    __table_args__ = (
        UniqueConstraint(
            "training_columns", "column_to_be_predicted", "model_name", "input_file_type", "input_file_name"
        ),
    )


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
    actual_house_value: float


class Prediction(PropertyParameters, SQLModel, table=True):
    predicted_house_value: float
