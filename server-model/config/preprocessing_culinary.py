# Import required libraries
import tensorflow as tf
import sqlalchemy as sa
import pandas as pd
import numpy as np

from sqlalchemy import create_engine
from dotenv import load_dotenv
from sklearn.preprocessing import MinMaxScaler, OneHotEncoder

# Load env
load_dotenv

# Load the trained TensorFlow model
culinary_recommendation = tf.keras.models.load_model("models/culinary.h5")

# Load your dataset (if still in local development)
data_culinary = pd.read_csv("data/culinary.csv")

# Load the dataset using database if its already hosted in cloud

"""
# Define the connection
username = 'GCP-SQL-ISNTANCE-USER'
password = 'GCP-SQL-ISNTANCE-PASSWORD'
database = 'DB-NAME'
host = 'GCP-SQL-INSTANCE'
port = '3306'

# Create the connection string
engineURL = f"mysql+mysqlconnector://{username}:{password}@{host}:{port}/{database}"
# Create the engine
engine = sa.create_engine(engineURL)

# Test the connection
try:
    with engine.connect() as connection:
        print("Connected to MySQL database successfully!")
except Exception as e:
    print("Connection failed:", e)

data_tour = pd.read_sql_query("SELECT * FROM culinary", engine)
"""

# Load and preprocess the dataset
def preprocess_culinary_data(data):
    # Normalize price_wna and rating
    scaler = MinMaxScaler()
    data[['price_wna', 'rating']] = scaler.fit_transform(data[['price_wna', 'rating']])

    # One-hot encode category and city
    encoder_category = OneHotEncoder(sparse_output=False, handle_unknown='ignore')
    encoder_city = OneHotEncoder(sparse_output=False, handle_unknown='ignore')

    encoded_category = encoder_category.fit_transform(data[['category']])
    encoded_city = encoder_city.fit_transform(data[['city']])

    # Combine features
    X = np.hstack((encoded_category, encoded_city, data[['price_wna', 'rating']].values))

    return data, X, scaler, encoder_category, encoder_city

# Preprocess the data
data, X, scaler, encoder_category, encoder_city = preprocess_culinary_data(data_culinary)

# Function to preprocess user input
def preprocess_user_input(user_input):
    user_df = pd.DataFrame([{
        "price_wna": user_input["max_price"],
        "rating": user_input["min_rating"]
    }])
    normalized_input = scaler.transform(user_df)
    user_category = encoder_category.transform([[user_input['category']]])
    user_city = encoder_city.transform([[user_input['city']]])
    user_vector = np.hstack((user_category, user_city, normalized_input))
    return user_vector

# Function to recommend top 5 culinary options
def culinary_recommendations(user_input, top_n=5):
     # Preprocess the user input to match model's input format
    user_input_vector = preprocess_user_input(user_input)

    # Predict scores for all data
    scores = culinary_recommendation.predict(X)
    data['score'] = scores.flatten()

    # Normalize input for filtering
    user_df = pd.DataFrame([{
        "price_wna": user_input["max_price"],
        "rating": user_input["min_rating"]
    }])
    normalized_input = scaler.transform(user_df)
    max_price_scaled, min_rating_scaled = normalized_input[0]

    # Filter data based on user's criteria
    filtered_data = data[
        (data['rating'] >= min_rating_scaled) &
        (data['price_wna'] <= max_price_scaled) &
        (data['city'] == user_input['city']) &
        (data['category'] == user_input['category'])
    ]

    # Debug: Ensure the processed user input is meaningful
    print("Processed User Input Vector:", user_input_vector)

    # Return original scale for rating and price_wna
    if not filtered_data.empty:
        filtered_data[['price_wna', 'rating']] = scaler.inverse_transform(
            filtered_data[['price_wna', 'rating']]
        )

    # Get top N recommendations or as many as available
    if not filtered_data.empty:
        recommendations = filtered_data.nlargest(min(top_n, len(filtered_data)), 'score')
    else:
        recommendations = pd.DataFrame()  # Empty DataFrame if no recommendations

    # Select relevant columns for output
    required_columns = ['name', 'rating', 'price_wna', 'city', 'category', 'address']
    available_columns = recommendations.columns.tolist()
    selected_columns = [col for col in required_columns if col in available_columns]

    return recommendations[selected_columns]