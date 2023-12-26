from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
import pandas as pd
from predict_house_value.db.database import get_session
from predict_house_value.app.schema import PropertyParameters, Prediction
from predict_house_value.preprocess.preprocess_data import preprocess_data
from predict_house_value.prediction.prediction import load_regression_model, predict

router = APIRouter()


@router.post("/add_prediction/", response_model=Prediction)
async def add_prediction(
    params: PropertyParameters,
    db: Session = Depends(get_session)
):
    # Preprocess the input data
    df = pd.DataFrame([params.dict()])  # Convert the Pydantic model to a DataFrame
    preprocessed_data = preprocess_data(df)

    # Load the trained model
    model = load_regression_model("path_to_your_model.joblib")  # Replace with the actual path

    # Perform the prediction
    prediction_value = predict(preprocessed_data, model)
    validated_preprocessed_data = PropertyParameters(**preprocessed_data)

    # Create a new Prediction instance
    new_prediction = Prediction(
        longitude=params.longitude,
        latitude=params.latitude,
        housing_median_age=params.housing_median_age,
        total_rooms=params.total_rooms,
        total_bedrooms=params.total_bedrooms,
        population=params.population,
        households=params.households,
        median_income=params.median_income,
        ocean_proximity=params.ocean_proximity,
        actual_house_value=params.actual_house_value,
        predicted_house_value=prediction_value
    )

    # Add the new record to the database
    db.add(new_prediction)
    db.commit()
    db.refresh(new_prediction)

    return new_prediction
