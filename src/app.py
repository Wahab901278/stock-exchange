from flask import Flask, request, jsonify
import pandas as pd
import joblib
import logging
import os


app = Flask(__name__)

FEATURE_NAMES = ['Open', 'High', 'Low', 'Volume', 'Dividends', 'Stock Splits']

def dataPreprocessing(data, scaler):
    data = data[FEATURE_NAMES]
    data.dropna(inplace=True)
    data.drop_duplicates(inplace=True)
    scaled_data = scaler.transform(data)
    scaled_df = pd.DataFrame(scaled_data, columns=data.columns)
    return scaled_df

def make_predictions(data):
    model_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../models/trained_model.pkl'))
    scaler_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../models/scaler.pkl'))
    target_scaler_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../models/target_scaler.pkl'))

    model = joblib.load(model_path)
    scaler = joblib.load(scaler_path)
    target_scaler = joblib.load(target_scaler_path)
    
    data = dataPreprocessing(data, scaler)
    X = data.drop(['Close'], axis=1, errors='ignore')
    
    scaled_predictions = model.predict(X)
    predictions = target_scaler.inverse_transform(scaled_predictions.reshape(-1, 1))
    return predictions

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json(force=True)
        app.logger.info(f"Received data: {data}")
        df = pd.DataFrame(data)
        app.logger.info(f"DataFrame: {df}")
        predictions = make_predictions(df)
        app.logger.info(f"Predictions: {predictions}")
        return jsonify(predictions.tolist())
    except Exception as e:
        app.logger.error(f"Error: {e}", exc_info=True)
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    app.run(host='0.0.0.0', port=5000)