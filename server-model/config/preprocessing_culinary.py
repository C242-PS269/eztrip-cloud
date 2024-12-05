# Import required libraries
import tensorflow as tf
import pandas as pd
import numpy as np

from dotenv import load_dotenv
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import MinMaxScaler, OneHotEncoder
from config.sql_engine import engine

# Load env
load_dotenv()

# Load the trained TensorFlow model
culinary_recommendation = tf.keras.models.load_model("models/culinary.h5")

# Load your dataset (if still in local development)
data_culinary = pd.read_sql_query("SELECT * FROM culinaries", engine)

# Preprocessing function for culinary data
def preprocess_culinary_data(data):

    """
    Preprocesses the user's input to match the format expected by the recommendation model.

    Args:
        user_input (dict): A dictionary containing the user's input with keys:
            - 'max_price' (float): The maximum price for filtering the recommendations.
            - 'min_rating' (float): The minimum rating for filtering the recommendations.
            - 'category' (str): The category of the culinary place.
            - 'city' (str): The city where the culinary place is located.

    Returns:
        np.ndarray: A NumPy array containing the processed user input.
    """

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

    return data, X, scaler, encoder_category, encoder_city, encoded_category, encoded_city

# Preprocess the data
data, X, scaler, encoder_category, encoder_city, encoded_category, encoded_city = preprocess_culinary_data(data_culinary)

# Function to preprocess user input
def preprocess_user_input(user_input):

    """
    Preprocess the user's input to match the format required by the recommendation model.
    
    Parameters:
    - user_input (dict): A dictionary containing the user's input with keys:
        - "max_price" (float): The maximum price the user is willing to pay.
        - "min_rating" (float): The minimum rating the user is looking for.
        - "category" (str): The category of the culinary (e.g., "Hotel", "Hostel").
        - "city" (str): The city where the user is looking for culinary.
    
    Returns:
    - user_vector (ndarray): A NumPy array representing the preprocessed user input, which includes:
        - Normalized price and rating.
        - Encoded category and city.
    """

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

    """
    Recommends top N culinary places based on the user's input using a trained model.

    Args:
        user_input (dict): A dictionary containing the user's input with keys:
            - 'max_price' (float): The maximum price for filtering the recommendations.
            - 'min_rating' (float): The minimum rating for filtering the recommendations.
            - 'category' (str): The category of the culinary place.
            - 'city' (str): The city where the culinary place is located.
        top_n (int, optional): The number of top recommendations to return. Defaults to 5.

    Returns:
        pd.DataFrame: A DataFrame containing the top N culinary recommendations with columns:
            - 'name': The name of the culinary place.
            - 'rating': The rating of the culinary place.
            - 'price_wna': The price of the culinary place.
            - 'city': The city of the culinary place.
            - 'category': The category of the culinary place.
            - 'address': The address of the culinary place.
    """

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

# Function to recommend similar culinary places
def visited_culinary_recommendations(culinary_name, city_filter=None, max_price=None, top_n=5):

    """
    Recommends culinary places similar to the one the user has visited, based on cosine similarity.

    Args:
        culinary_name (str): The name of the culinary place the user has visited.
        city_filter (str, optional): The city to filter the recommendations by. Defaults to None.
        max_price (float, optional): The maximum price for filtering the recommendations. Defaults to None.
        top_n (int, optional): The number of top recommendations to return. Defaults to 5.

    Returns:
        list: A list of dictionaries containing the top N similar culinary places with the following keys:
            - 'name': The name of the culinary place.
            - 'rating': The rating of the culinary place.
            - 'price_wna': The price of the culinary place.
            - 'city': The city of the culinary place.
            - 'category': The category of the culinary place.
            - 'address': The address of the culinary place.
    """

    # Ensure the culinary place exists in the data
    if culinary_name not in data['name'].values:
        return {"error": f"Place '{culinary_name}' not found in data."}, 404

    # Feature extraction for similarity calculation
    features = np.hstack((
        encoded_category,
        encoded_city,
        data[['price_wna', 'rating']].values
    ))

    culinary_idx = data[data['name'] == culinary_name].index[0]

    # Cosine similarity calculation
    similarity_scores = cosine_similarity(features[culinary_idx].reshape(1, -1), features).flatten()
    data['similarity'] = similarity_scores

    # Handle optional filters for city and max_price
    if max_price is not None:
        max_price = float(max_price)

    filtered_data = data[data['name'] != culinary_name]
    
    if city_filter:
        filtered_data = filtered_data[filtered_data['city'] == city_filter]
    if max_price is not None:
        max_price_scaled = scaler.transform([[max_price, 0]])[0][0]
        filtered_data = filtered_data[filtered_data['price_wna'] <= max_price_scaled]

    # Return original scale for price_wna and rating
    if not filtered_data.empty:
        filtered_data[['price_wna', 'rating']] = scaler.inverse_transform(
            filtered_data[['price_wna', 'rating']]
        )

    recommendations = filtered_data.nlargest(top_n, 'similarity') if not filtered_data.empty else pd.DataFrame()

    return recommendations[['name', 'rating', 'price_wna', 'city', 'category', 'address']].to_dict(orient="records")