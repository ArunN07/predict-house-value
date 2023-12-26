# project_root/src/preprocess/preprocess_data.py
import pandas as pd
from predict_house_value.config.config import FilePathConstants, ColumnNames


def preprocess_data(input_data):
    # Remove rows with any null values, including "Null" strings
    input_data = input_data.dropna()

    # Encode categorical variables using get_dummies
    input_data = pd.get_dummies(input_data, columns=[ColumnNames.OCEAN_PROXIMITY])

    # Add any additional preprocessing steps here

    return input_data


def write_processed_data(data, output_path):
    # Save the processed data
    data.to_csv(output_path, index=False)


if __name__ == "__main__":
    # Example usage
    raw_data = pd.read_csv(FilePathConstants.TRAIN_DATA)
    processed_data = preprocess_data(raw_data)
    write_processed_data(processed_data, FilePathConstants.PROCESSED_DATA)
