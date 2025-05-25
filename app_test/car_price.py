import streamlit as st
import pandas as pd
import joblib
import os


st.title("🚗 Car Price Predictor App")

# Load model
model_path = os.path.join('..', 'car_price', 'car_model.pkl')
pipe = joblib.load(model_path)

# Load dataset
data_path = os.path.join('..', 'car_price', 'cleaned_car.csv')
df = pd.read_csv(data_path)

# Drop the 'Unnamed: 0' column if it exists
if 'Unnamed: 0' in df.columns:
    df = df.drop(columns=['Unnamed: 0'])

# Clean column names
df.columns = (
    df.columns.str.strip()
    .str.lower()
    .str.replace(' ', '_')
    .str.replace(r'\W+', '', regex=True)
)

# Handle NaN in 'fuel_type'
df['fuel_type'] = df['fuel_type'].fillna('Unknown').astype(str)

# Extract unique values
car_names = sorted(df['name'].unique())
companies = sorted(df['company'].unique())
fuel_types = sorted(df['fuel_type'].unique())
min_year, max_year = int(df['year'].min()), int(df['year'].max())

# User Input UI
car_names_display = ['Select Car Name'] + car_names
companies_display = ['Select Company'] + companies
fuel_types_display = ['Select Fuel Type'] + fuel_types
years_display = ['Select Year'] + list(range(max_year, min_year - 1, -1))

name = st.selectbox('Car Name', car_names_display)
company = st.selectbox('Company', companies_display)
year = st.selectbox('Purchase Year', years_display)
fuel_type = st.selectbox('Fuel Type', fuel_types_display)
kms_driven = st.number_input('Kilometers Driven', min_value=0, value=500, step=50)

# Only one Predict button with logic
if st.button('Predict Price', key='predict_button'):
    if (
        name == 'Select Car Name' or 
        company == 'Select Company' or 
        year == 'Select Year' or 
        fuel_type == 'Select Fuel Type'
    ):
        st.warning('Please select all fields before predicting.')
    else:
        input_df = pd.DataFrame([[name, company, int(year), kms_driven, fuel_type]],
                                columns=['name', 'company', 'year', 'kms_driven', 'fuel_type'])
        prediction = pipe.predict(input_df)[0]
        st.success(f'Estimated Price: ₹ {round(prediction, 2)} Lakh')
