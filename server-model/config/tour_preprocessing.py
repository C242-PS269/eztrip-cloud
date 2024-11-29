import tensorflow as tf
import pandas as pd
import numpy as np
import os
from dotenv import load_dotenv
from sklearn.preprocessing import MinMaxScaler, OneHotEncoder

# Load env
load_dotenv

# Load the trained TensorFlow model
model = tf.keras.models.load_model("models/recommendation.h5")

# Load your dataset (if still in local development)
# Load the dataset using database if its already hosted in cloud
data = pd.read_excel("data/tour.xlsx")

def preprocess_data(data):
    # Define the columns used in the dataset
    selected_columns = {
        "Name": "name",
        "Rating": "rating",
        "Kategori": "category",
        "Harga Tiket Masuk WNA Dewasa": "price_wna",  # Harga yang digunakan hanya harga WNA dewasa
        "Kota/Kabupaten": "city",
        "Jalan": "address",
        "Google.Maps": "google_maps"
    }

    # Rename columns
    data = data.rename(columns=selected_columns)

    # Drop rows with missing values in important columns
    data = data.dropna(subset=["name", "rating", "category", "price_wna", "city"])

    # Normalize price and rating
    scaler = MinMaxScaler()
    data[['price_wna', 'rating']] = scaler.fit_transform(data[['price_wna', 'rating']])

    # One-hot encode 'category' and 'city'
    encoder_category = OneHotEncoder(sparse_output=False, handle_unknown='ignore')
    encoder_city = OneHotEncoder(sparse_output=False, handle_unknown='ignore')

    encoded_category = encoder_category.fit_transform(data[['category']])
    encoded_city = encoder_city.fit_transform(data[['city']])

    # Return the encoded data, scaler, and encoders for use in other parts of the pipeline
    return data, encoded_category, encoded_city, scaler, encoder_category, encoder_city

# Process the dataset using the new function
data, encoded_category, encoded_city, scaler, encoder_category, encoder_city = preprocess_data(data)

# Combine the features into the final input matrix (X)
X = np.hstack((encoded_category, encoded_city, data[['price_wna', 'rating']].values))

# Function to preprocess user input in the same way as training data
def preprocess_user_input(user_input, scaler, encoder_category, encoder_city):
    # Normalize 'price_wna' and 'rating' values
    user_input_df = pd.DataFrame([{
        "price_wna": user_input["max_price"],
        "rating": user_input["min_rating"],
        "category": user_input["category"],
        "city": user_input["city"]
    }])

    # Normalize 'price_wna' and 'rating' using the same scaler
    user_input_df[['price_wna', 'rating']] = scaler.transform(user_input_df[['price_wna', 'rating']])

    # One-hot encode 'category' and 'city' using the same encoders
    encoded_category = encoder_category.transform(user_input_df[['category']])
    encoded_city = encoder_city.transform(user_input_df[['city']])

    # Combine all features into a single array
    user_input_processed = np.hstack((encoded_category, encoded_city, user_input_df[['price_wna', 'rating']].values))

    return user_input_processed

# Function for recommendations
def recommend(user_input, top_n=5):
    # Preprocess the user input
    processed_input = preprocess_user_input(user_input, scaler, encoder_category, encoder_city)

    # Predict the scores using the model
    scores = model.predict(X)  # Use the entire dataset for prediction

    # Add the predicted scores to the dataframe
    data['score'] = scores.flatten()

    # Normalize user input based on the scaler
    max_price_scaled, min_rating_scaled = processed_input[0, -2], processed_input[0, -1]  # Extract the normalized price and rating

    # Filter data based on user input
    filtered_data = data[
        (data['rating'] >= min_rating_scaled) &
        (data['price_wna'] <= max_price_scaled) &
        (data['category'] == user_input['category']) &
        (data['city'] == user_input['city'])
    ]

    # Inverse transform to get original scale for price and rating
    if not filtered_data.empty:
        filtered_data[['price_wna', 'rating']] = scaler.inverse_transform(filtered_data[['price_wna', 'rating']])

    # Get top N recommendations
    recommendations = filtered_data.nlargest(top_n, 'score')

    # Return the recommendations with selected columns
    required_columns = ['name', 'rating', 'price_wna', 'city', 'category', 'google_maps']
    available_columns = recommendations.columns.tolist()

    selected_columns = [col for col in required_columns if col in available_columns]
    return recommendations[selected_columns]