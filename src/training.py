import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split, cross_val_score, GridSearchCV
from sklearn.metrics import mean_squared_error, mean_absolute_percentage_error, accuracy_score, r2_score
from fetchdata import get_data
import joblib
import os
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def dataPreprocessing(data):
    data.dropna(inplace=True)
    data.drop_duplicates(inplace=True)
    X = data.drop(['Close'], axis=1)
    y = data[['Close']]
    feature_scaler = StandardScaler()
    X_scaled = feature_scaler.fit_transform(X)
    X_scaled_df = pd.DataFrame(X_scaled, columns=X.columns)
    target_scaler = StandardScaler()
    y_scaled = target_scaler.fit_transform(y)
    y_scaled_df = pd.DataFrame(y_scaled, columns=y.columns)
    scaled_df = pd.concat([X_scaled_df, y_scaled_df], axis=1)
    return scaled_df, feature_scaler, target_scaler

def trainingdata(data):
    data, feature_scaler, target_scaler = dataPreprocessing(data)
    X = data.drop(['Close'], axis=1)
    y = data['Close']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    rf_model = RandomForestRegressor()
    rf_model.fit(X_train, y_train)
    y_pred = rf_model.predict(X_test)

    mse = mean_squared_error(y_test, y_pred)
    mape = mean_absolute_percentage_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)
    
    logger.info(f'MSE: {mse}')
    logger.info(f'MAPE: {mape}')
    logger.info(f'R2 Score: {r2}')

    # Save the trained model and scalers
    model_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../models'))
    os.makedirs(model_dir, exist_ok=True)
    
    joblib.dump(rf_model, os.path.join(model_dir, 'trained_model.pkl'))
    joblib.dump(feature_scaler, os.path.join(model_dir, 'scaler.pkl'))
    joblib.dump(target_scaler, os.path.join(model_dir, 'target_scaler.pkl'))

if __name__ == "__main__":
    data = get_data(symbol='PSX', period='max')
    trainingdata(data)