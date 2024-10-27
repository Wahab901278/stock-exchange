from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
import os
import sys
import pandas as pd
import joblib
import yfinance as yf
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, mean_absolute_percentage_error, r2_score
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Set the models directory path
MODELS_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '../models'))

def get_data(symbol='AAPL', period='1mo'):
    """Fetch historical stock data from Yahoo Finance."""
    ticker = yf.Ticker(symbol)
    historical_data = ticker.history(period=period)
    return historical_data

def dataPreprocessing(data):
    """Preprocess the data for training."""
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
    """Train the model and save it."""
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
    os.makedirs(MODELS_DIR, exist_ok=True)
    joblib.dump(rf_model, os.path.join(MODELS_DIR, 'trained_model.pkl'))
    joblib.dump(feature_scaler, os.path.join(MODELS_DIR, 'scaler.pkl'))
    joblib.dump(target_scaler, os.path.join(MODELS_DIR, 'target_scaler.pkl'))

def extract_data(**kwargs):
    """Extract data using the get_data function."""
    data = get_data(symbol='PSX', period='max')
    return data.to_json()

def train_model(**kwargs):
    """Train the model using the extracted data."""
    ti = kwargs['ti']
    data_json = ti.xcom_pull(task_ids='extract_data')
    data = pd.read_json(data_json)

    trainingdata(data)

# Default arguments for the DAG
default_args = {
    'owner': 'Wahab901278',
    'depends_on_past': False,
    'start_date': datetime(2023, 10, 1),
    'email_on_failure': False,
}

# Define the DAG
dag = DAG('ETL_training_pipeline', default_args=default_args, schedule='@daily')

# Define the tasks
extract_task = PythonOperator(
    task_id='extract_data',
    python_callable=extract_data,
    dag=dag,
)

train_task = PythonOperator(
    task_id='train_model',
    python_callable=train_model,
    dag=dag,
)

# Set task dependencies
extract_task >> train_task
