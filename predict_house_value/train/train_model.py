import joblib
from sklearn.ensemble import RandomForestRegressor


def train_model(fields_to_train, field_to_predict) -> RandomForestRegressor:
    regressor = RandomForestRegressor(max_depth=12)
    regressor.fit(fields_to_train, field_to_predict)
    return regressor


def save_model(model, filename):
    with open(filename, 'wb'):
        joblib.dump(model, filename, compress=3)
