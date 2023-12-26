# project_root/tests/test_app.py
from fastapi.testclient import TestClient
from predict_house_value.app.app import app
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from predict_house_value.db.database import Base, engine

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_test_db():
    Base.metadata.create_all(bind=engine)
    try:
        yield
    finally:
        Base.metadata.drop_all(bind=engine)

def test_predict_json():
    client = TestClient(app)

    input_data = {
        "longitude": -122.25,
        "latitude": 37.85,
        "housing_median_age": 41.0,
        "total_rooms": 880.0,
        "total_bedrooms": 129.0,
        "population": 322.0,
        "households": 126.0,
        "median_income": 8.3252,
        "ocean_proximity": "NEAR BAY"
    }

    response = client.post
