import streamlit as st
import pandas as pd
import joblib
import os
# Construct path to model relative to app.py
model_path = os.path.join('..', 'car_price', 'car_model.pkl')
pipe = joblib.load(model_path)

st.title('Car Price Predictor 🚗')

# Input fields
name = st.text_input('Car Name', 'Maruti Suzuki Swift')
company = st.selectbox('Company', ['Maruti', 'Hyundai', 'Honda', 'Toyota', 'Ford'])
year = st.number_input('Purchase Year', min_value=1990, max_value=2025, value=2019)
kms_driven = st.number_input('Kilometers Driven', value=100)
fuel_type = st.selectbox('Fuel Type', ['Petrol', 'Diesel', 'CNG', 'Electric'])

if st.button('Predict Price'):
    input_df = pd.DataFrame([[name, company, year, kms_driven, fuel_type]],
                            columns=['name', 'company', 'year', 'kms_driven', 'fuel_type'])
    prediction = pipe.predict(input_df)[0]
    st.success(f'Estimated Price: ₹ {round(prediction, 2)} Lakh')
