# Import required libraries
import tensorflow as tf
import pandas as pd
import numpy as np

from dotenv import load_dotenv
from sklearn.preprocessing import MinMaxScaler, OneHotEncoder
from sklearn.metrics.pairwise import cosine_similarity
from config.sql_engine import engine

# Load env
load_dotenv()

# Load the trained TensorFlow model
tour_recommendation = tf.keras.models.load_model("models/tour.h5")

# Load your dataset (if still in local development)
data_tour = pd.read_sql_query("SELECT * FROM tour", engine)

def preprocess_tour_data(data):

    """
    Preprocess the tour dataset by normalizing numerical features and encoding categorical features.
    
    Args:
    - data (DataFrame): The raw dataset containing tour data
    
    Returns:
    - data (DataFrame): Processed dataset with normalized price and rating
    - encoded_category (ndarray): One-hot encoded category column
    - encoded_city (ndarray): One-hot encoded city column
    - scaler (MinMaxScaler): Fitted scaler for price and rating
    - encoder_category (OneHotEncoder): Fitted encoder for category
    - encoder_city (OneHotEncoder): Fitted encoder for city
    """

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
data, encoded_category, encoded_city, scaler, encoder_category, encoder_city = preprocess_tour_data(data_tour)

# Combine the features into the final input matrix (X)
X = np.hstack((encoded_category, encoded_city, data[['price_wna', 'rating']].values))

# Function to preprocess user input in the same way as training data
def preprocess_user_input(user_input, scaler, encoder_category, encoder_city):

    """
    Preprocess user input for making recommendations by normalizing and encoding input values.
    
    Args:
    - user_input (dict): User input containing 'max_price', 'min_rating', 'category', 'city'
    - scaler (MinMaxScaler): Fitted scaler for normalizing price and rating
    - encoder_category (OneHotEncoder): Fitted encoder for category
    - encoder_city (OneHotEncoder): Fitted encoder for city
    
    Returns:
    - user_input_processed (ndarray): Processed input ready for recommendation prediction
    """

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
def tour_recommendations(user_input, top_n=5):

    """
    Generate top N tour recommendations based on user input.
    
    Args:
    - user_input (dict): User input containing 'max_price', 'min_rating', 'category', 'city'
    - top_n (int): Number of recommendations to return (default is 5)
    
    Returns:
    - recommendations (DataFrame): Top N recommended tours with selected columns
    """

    # Preprocess the user input
    processed_input = preprocess_user_input(user_input, scaler, encoder_category, encoder_city)

    # Predict the scores using the model
    scores = tour_recommendation.predict(X)  # Use the entire dataset for prediction

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

# Function for recommendations based on previously visited places
def visited_tour_recommendations(tour_name, city_filter=None, max_price=None, top_n=5):

    """
    Generate recommendations based on a previously visited tour and calculate similarity with other tours.
    
    Args:
    - tour_name (str): Name of the tour that the user has visited
    - city_filter (str, optional): City filter to narrow down recommendations
    - max_price (float, optional): Maximum price filter for recommendations
    - top_n (int): Number of top recommendations to return (default is 5)
    
    Returns:
    - recommendations (list): List of top N recommended tours based on similarity
    """

    # Ensure the tour_name exists in the data
    if tour_name not in data['name'].values:
        return {"error": f"Tour place '{tour_name}' is is not found."}

    # Choose features for similarity calculation
    features = np.hstack((
        encoded_category,
        encoded_city,
        data[['price_wna', 'rating']].values
    ))

    # Get the index of the input destination
    tour_idx = data[data['name'] == tour_name].index[0]

    # Calculate cosine similarity between the input destination and all others
    similarity_scores = cosine_similarity(features[tour_idx].reshape(1, -1), features).flatten()

    # Add similarity scores to the data
    data['similarity'] = similarity_scores

    # Filter data based on max_price or city_filter
    filtered_data = data[data['name'] != tour_name]
    if city_filter:
        filtered_data = filtered_data[filtered_data['city'] == city_filter]
    if max_price is not None:
        max_price_scaled = scaler.transform([[max_price, 0]])[0][0]
        filtered_data = filtered_data[filtered_data['price_wna'] <= max_price_scaled]

    # Inverse transform the price and rating to their original scale
    if not filtered_data.empty:
        filtered_data.loc[:, ['price_wna', 'rating']] = scaler.inverse_transform(
            filtered_data[['price_wna', 'rating']]
        )

    # Sort by similarity and select top N
    recommendations = filtered_data.nlargest(top_n, 'similarity') if not filtered_data.empty else pd.DataFrame()

    # Return the recommendations with selected columns
    return recommendations[['name', 'rating', 'price_wna', 'city', 'category', 'address', 'google_maps']].to_dict(orient='records')