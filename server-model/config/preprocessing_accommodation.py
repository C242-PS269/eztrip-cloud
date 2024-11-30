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
accommodation_recommendation = tf.keras.models.load_model("models/accommodation.h5")

# Load your dataset (if still in local development)
data_accommodation = pd.read_csv("data/accommodation.csv")

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

data_tour = pd.read_sql_query("SELECT * FROM accommodation", engine)
"""

# Define the preprocessing function
def preprocess_accommodation_data(data):

    # Normalize price_wna and rating
    scaler = MinMaxScaler()
    data[['price_wna', 'rating']] = scaler.fit_transform(data[['price_wna', 'rating']])

    # One-hot encode city
    encoder_city = OneHotEncoder(sparse_output=False, handle_unknown='ignore')
    encoded_city = encoder_city.fit_transform(data[['city']])

    # Combine selected features
    X = np.hstack((encoded_city, data[['price_wna', 'rating']].values))

    return X, scaler, encoder_city, data

# Preprocess the dataset
X, scaler, encoder_city, data = preprocess_accommodation_data(data_accommodation)

# Function to preprocess user input
def preprocess_user_input(user_input):
    # Create a DataFrame for normalization and encoding
    user_df = pd.DataFrame([{
        "price_wna": user_input["max_price"],
        "rating": user_input["min_rating"]
    }])

    # Normalize the user's input
    normalized_input = scaler.transform(user_df)

    # One-hot encode the city
    user_city = encoder_city.transform([[user_input['city']]])

    # Combine all features into a single vector
    user_vector = np.hstack((user_city, normalized_input))
    return user_vector

# Function to generate top 5 recommendations
def accommodation_recommendations(user_input, top_n=5):
    # Preprocess the user input
    user_input_vector = preprocess_user_input(user_input)

    # Predict scores for user input and dataset interaction
    combined_input = np.concatenate([user_input_vector] * len(X), axis=0)  # Repeat user input
    scores = accommodation_recommendation.predict(np.hstack((X, combined_input)))

    # Add scores to the dataset
    data['score'] = scores.flatten()

    # Filter data based on user's raw criteria
    filtered_data = data[
        (data['rating'] >= user_input["min_rating"]) &
        (data['price_wna'] <= user_input["max_price"]) &
        (data['city'] == user_input["city"])
    ]

    # Get top N recommendations based on score
    if not filtered_data.empty:
        recommendations = filtered_data.nlargest(top_n, 'score')
    else:
        recommendations = pd.DataFrame()  # Empty DataFrame if no recommendations

    # Select relevant columns for output
    selected_columns = ['name', 'rating', 'price_wna', 'city']
    available_columns = recommendations.columns.tolist()
    selected_columns = [col for col in selected_columns if col in available_columns]

    return recommendations[selected_columns]