import joblib  # or use 'import pickle' if your model was saved using pickle
from predict_house_value.config.config import ColumnNames, FilePathConstants

# Load the trained model from the file
model = joblib.load(FilePathConstants.MODEL_FILE_PATH / 'old' / 'model.joblib')  # Replace with the actual path

# Check if the model has a 'feature_importances_' attribute
if hasattr(model, 'feature_importances_'):
    # If available, get feature names and importances
    feature_importances = model.feature_importances_
    pass
else:
    print("Model does not have 'feature_importances_' attribute.")