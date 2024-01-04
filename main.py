import sys
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error
import joblib
import logging

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

TRAIN_DATA = 'housing.csv'
MODEL_NAME = 'model.joblib'
RANDOM_STATE = 100


def prepare_data(input_data_path):
    df = pd.read_csv(input_data_path, na_values=['Null'])
    df = df.dropna()
    df = df[df["ocean_proximity"] != "OUT OF REACH"]

    # encode the categorical variables
    df = pd.get_dummies(df, columns=["ocean_proximity"])

    df_features = df.drop(['median_house_value', "agency"], axis=1)
    y = df['median_house_value'].values

    X_train, X_test, y_train, y_test = train_test_split(df_features, y, test_size=0.2, random_state=RANDOM_STATE)

    return (X_train, X_test, y_train, y_test)


def train(X_train, y_train):
    # what columns are expected by the models
    X_train.columns

    regr = RandomForestRegressor(max_depth=12)
    regr.fit(X_train, y_train)

    return regr


def predict(X, model):
    Y = model.predict(X)
    return Y


def save_model(model, filename):
    with open(filename, 'wb'):
        joblib.dump(model, filename, compress=3)


def load_model(filename):
    model = joblib.load(filename)
    return model


if __name__ == '__main__':
    logging.info('Preparing the data...')
    X_train, X_test, y_train, y_test = prepare_data(TRAIN_DATA)

    # the models was already trained before
    # logging.info('Training the models...')
    # regr = train(X_train, y_train)

    # the models was already saved before into file 'models.joblib'
    # logging.info('Exporting the models...')
    # save_model(regr, MODEL_NAME)

    logging.info('Loading the models...')
    model = load_model(MODEL_NAME)

    logging.info('Calculating train dataset predictions...')
    y_pred_train = predict(X_train, model)
    logging.info('Calculating test dataset predictions...')
    y_pred_test = predict(X_test, model)

    # evaluate models
    logging.info('Evaluating the models...')
    train_error = mean_absolute_error(y_train, y_pred_train)
    test_error = mean_absolute_error(y_test, y_pred_test)

    logging.info('First 5 predictions:')
    logging.info(f'\n{X_test.head()}')
    logging.info(y_pred_test[:5])
    logging.info(f'Train error: {train_error}')
    logging.info(f'Test error: {test_error}')

    my_dict = {
        'longitude': -122.64,
        'latitude': 38.01,
        'housing_median_age': 36.0,
        'total_rooms': 1336.0,
        'total_bedrooms': 258.0,
        'population': 678.0,
        'households': 249.0,
        'median_income': 5.5789,
        'ocean_proximity': 'NEAR OCEAN'
    }
    input_data = pd.DataFrame([my_dict], index=[0])  # Convert the Pydantic model to a DataFrame
    #input_data = input_data.drop(['median_house_value'], axis=1)
    preprocessed_data = pd.get_dummies(input_data, columns=["ocean_proximity"])
    columns_in_model = list(model.feature_names_in_)

    for column in columns_in_model:
        if column not in preprocessed_data.columns:
            preprocessed_data[column] = 0

    # Perform the prediction
    prediction_value = predict(preprocessed_data, model)
    print(prediction_value)
