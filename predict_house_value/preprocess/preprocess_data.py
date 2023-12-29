import pandas as pd
from sklearn.model_selection import train_test_split
from predict_house_value.config.config import FilePathConstants, ColumnNames


def preprocess_data(input_data):
    input_data = input_data.dropna()

    # Encode categorical variables using get_dummies
    input_data = input_data[input_data[ColumnNames.OCEAN_PROXIMITY] != "OUT OF REACH"]
    input_data = pd.get_dummies(input_data, columns=[ColumnNames.OCEAN_PROXIMITY])
    return input_data


def write_processed_data(data, output_path):
    # Save the processed data
    data.to_csv(output_path, index=False)


def prepare_data_to_train(input_data):
    field_to_predict = input_data[ColumnNames.MEDIAN_HOUSE_VALUE].values
    input_data = input_data.drop([ColumnNames.MEDIAN_HOUSE_VALUE, ColumnNames.AGENCY], axis=1)

    x_training_data, x_test_data, y_training_data, y_test_data = train_test_split(
        input_data, field_to_predict, test_size=0.2, random_state=100)

    return x_training_data, x_test_data, y_training_data, y_test_data
