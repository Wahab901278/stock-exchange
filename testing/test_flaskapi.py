import unittest
import json
import sys
import os
import warnings

import numpy as np
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from app import app
class TestFlaskAPI(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_predict_endpoint(self):
        warnings.filterwarnings("ignore", category=UserWarning, module='sklearn')
        input_data = [{
            'Open': 133.0,
            'High': 135.0,
            'Low': 131.0,
            'Volume': 88888,
            'Dividends': 0.0,
            'Stock Splits': 0.0
        }]
        
        response = self.app.post('/predict', json=input_data)
        

        self.assertEqual(response.status_code, 200, msg=f"Response data: {response.data}")
        
        
 
        data = json.loads(response.data)
        self.assertEqual(len(data), 1)
        self.assertIsInstance(data[0], list)
        self.assertIsInstance(data[0][0], float)

if __name__ == '__main__':
    unittest.main()