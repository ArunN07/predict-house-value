from pathlib import Path


class ColumnNames:
    # Define column names
    LONGITUDE = "longitude"
    LATITUDE = "latitude"
    HOUSING_MEDIAN_AGE = "housing_median_age"
    TOTAL_ROOMS = "total_rooms"
    TOTAL_BEDROOMS = "total_bedrooms"
    POPULATION = "population"
    HOUSEHOLDS = "households"
    MEDIAN_INCOME = "median_income"
    MEDIAN_HOUSE_VALUE = "median_house_value"
    OCEAN_PROXIMITY = "ocean_proximity"
    AGENCY = "agency"
    PREDICTED_HOUSE_VALUE = "predicted_house_value"


class FilePathConstants:
    # Define file paths
    RAW_DATA_PATH = Path(__file__).parent.parent.parent / 'data' / 'raw'
    MODEL_FILE_PATH = Path(__file__).parent.parent.parent / 'models'
    PROCESSED_DATA_PATH = Path(__file__).parent.parent.parent / 'data' / 'processed' / 'housing.csv'


class URLs:
    DATABASE_URL = "postgresql://postgres:arun@localhost/house_value"
