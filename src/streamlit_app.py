import streamlit as st
import pandas as pd
import requests

st.title('Stock Price Prediction')


open_price = st.number_input('Open Price', min_value=0.0, step=0.01)
high_price = st.number_input('High Price', min_value=0.0, step=0.01)
low_price = st.number_input('Low Price', min_value=0.0, step=0.01)
volume = st.number_input('Volume', min_value=0, step=1)
dividends = st.number_input('Dividends', min_value=0.0, step=0.01)
stock_splits = st.number_input('Stock Splits', min_value=0.0, step=0.01)


if st.button('Predict'):
    input_data = pd.DataFrame({
        'Open': [open_price],
        'High': [high_price],
        'Low': [low_price],
        'Volume': [volume],
        'Dividends': [dividends],
        'Stock Splits': [stock_splits]
    })
    


    response = requests.post('http://localhost:5000/predict', json=input_data.to_dict(orient='records'))

    if response.status_code == 200:
        prediction = response.json()
        price=prediction[0]
        st.success(f'Predicted Close Price: {price[0]}')
    else:
        st.error('Error making prediction')
        st.write(response.text)