from pathlib import Path
import joblib
import pandas as pd
from sklearn.ensemble import RandomForestRegressor


def load_regressor_model(model_path: Path) -> RandomForestRegressor:
    return joblib.load(model_path)


def predict(preprocessed_data: pd.DataFrame, model: RandomForestRegressor):
    return model.predict(preprocessed_data)
