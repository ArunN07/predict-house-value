# project_root/predict_house_value/train/train_model.py
import joblib
import pandas as pd
from sklearn.ensemble import RandomForestRegressor

TRAIN_DATA = 'housing.csv'
MODEL_NAME = 'models/model.joblib'
RANDOM_STATE = 100

def train_model():
    df = pd.read_csv(TRAIN_DATA)
    df = df.dropna()

    # encode the categorical variables
    df = pd.get_dummies(df)

    df_features = df.drop(['median_house_value'], axis=1)
    y = df['median_house_value'].values

    regr = RandomForestRegressor(max_depth=12)
    regr.fit(df_features, y)

    # Save the trained model
    joblib.dump(regr, MODEL_NAME, compress=3)

if __name__ == "__main__":
    train_model()
