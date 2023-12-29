from fastapi import APIRouter, Depends, File, UploadFile, HTTPException
from sqlalchemy.orm import Session
import pandas as pd
from predict_house_value.db.database import get_session
from predict_house_value.app.schema import PropertyParameters, Prediction
from predict_house_value.preprocess.preprocess_data import preprocess_data
from predict_house_value.prediction.prediction import load_regressor_model, predict
from predict_house_value.config.config import ColumnNames, FilePathConstants

prediction_router = APIRouter()


@prediction_router.post("/add_prediction/", response_model=Prediction)
async def add_prediction(
    params: PropertyParameters,
    db: Session = Depends(get_session)
):
    # Preprocess the input data
    property_params = params.model_dump()
    input_data = pd.DataFrame([property_params], index=[0])  # Convert the Pydantic model to a DataFrame
    input_data = input_data.drop([ColumnNames.MEDIAN_HOUSE_VALUE], axis=1)
    preprocessed_data = preprocess_data(input_data)

    # Load the trained model
    model = load_regressor_model(FilePathConstants.MODEL_FILE_PATH / 'old' / 'model.joblib')
    columns_in_model = list(model.feature_names_in_)

    for column in columns_in_model:
        if column not in preprocessed_data.columns:
            preprocessed_data[column] = 0

    # Perform the prediction
    prediction_value = predict(preprocessed_data, model)
    property_params[ColumnNames.PREDICTED_HOUSE_VALUE] = prediction_value[0]
    new_prediction = Prediction(**property_params)

    # Add the new record to the database
    db.add(new_prediction)
    db.commit()
    db.refresh(new_prediction)

    return new_prediction


@prediction_router.post("/add_prediction_to_file/", response_model=Prediction)
async def add_prediction_to_file(
    file: UploadFile = File(...),
    db: Session = Depends(get_session)
):
    try:
        # Read the uploaded file into a DataFrame
        input_data = pd.read_csv(file.file, na_values=['Null'])

        # Preprocess the input data
        preprocessed_data = preprocess_data(input_data)
        preprocessed_data = preprocessed_data.drop([ColumnNames.MEDIAN_HOUSE_VALUE, ColumnNames.AGENCY], axis=1)

        # Ensure all columns expected by the model are present
        model = load_regressor_model(FilePathConstants.MODEL_FILE_PATH / 'old' / 'model.joblib')
        columns_in_model = list(model.feature_names_in_)
        for column in columns_in_model:
            if column not in preprocessed_data.columns:
                preprocessed_data[column] = 0

        # Perform the predictions
        predictions = predict(preprocessed_data, model)

        # Create Prediction objects for each row
        prediction_objects = []
        for i, prediction_value in enumerate(predictions):
            params_dict = input_data.iloc[i].to_dict()
            params_dict[ColumnNames.PREDICTED_HOUSE_VALUE] = prediction_value
            prediction_objects.append(Prediction(**params_dict))

        # Add the new records to the database
        db.bulk_save_objects(prediction_objects)
        db.commit()

        return prediction_objects[0]

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
