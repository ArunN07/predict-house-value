import joblib
import pandas as  pd
from sklearn.linear_model import LinearRegression


def load_regression_model(model_path) -> LinearRegression:
    return joblib.load(model_path)


def predict(preprocessed_data: pd.Dataframe, model: LinearRegression):
    return model.predict(preprocessed_data)
