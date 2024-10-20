import unittest
import pandas as pd
import os
import sys
import numpy as np

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from app import dataPreprocessing, make_predictions
import joblib

class TestApp(unittest.TestCase):

    def setUp(self):
        self.scaler = joblib.load(os.path.abspath(os.path.join(os.path.dirname(__file__), '../models/scaler.pkl')))
        self.target_scaler = joblib.load(os.path.abspath(os.path.join(os.path.dirname(__file__), '../models/target_scaler.pkl')))
        self.model = joblib.load(os.path.abspath(os.path.join(os.path.dirname(__file__), '../models/trained_model.pkl')))
    def test_data_preprocessing(self):
        data = pd.DataFrame({
            'Open': [133.0],
            'High': [135.0],
            'Low': [131.0],
            'Volume': [88888],
            'Dividends': [0.0],
            'Stock Splits': [0.0]
        })
        
        scaled_data = dataPreprocessing(data, self.scaler)

        self.assertListEqual(list(scaled_data.columns), list(data.columns))

    def test_make_predictions(self):
        data = pd.DataFrame({
            'Open': [133.0],
            'High': [135.0],
            'Low': [131.0],
            'Volume': [88888],
            'Dividends': [0.0],
            'Stock Splits': [0.0]
        })

        predictions = make_predictions(data)
        
        self.assertEqual(len(predictions), 1)
        self.assertIsInstance(predictions, np.ndarray)
        self.assertIsInstance(predictions[0][0], np.float64, float)  

if __name__ == '__main__':
    unittest.main()