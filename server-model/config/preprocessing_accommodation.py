# Import required libraries
import tensorflow as tf
import pandas as pd
import numpy as np

from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import MinMaxScaler, OneHotEncoder
from dotenv import load_dotenv

# Load env
load_dotenv()

# Load the trained TensorFlow model
accommodation_recommendation = tf.keras.models.load_model("models/accommodation.h5")

# Load your dataset
data_accommodation = pd.read_csv("data/accommodation.csv")

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

    print("Preprocessed data shape (X):", X.shape)  # Debugging step
    return X, scaler, encoder_city, encoded_city, data

# Preprocess the dataset
X, scaler, encoder_city, encoded_city, data = preprocess_accommodation_data(data_accommodation)

# Check the input shape of the model
print("Model input shape:", accommodation_recommendation.input_shape)  # Debugging step

# Function to generate top 5 recommendations based on user input
def accommodation_recommendations(user_input, top_n=5):
    # Normalize user input
    user_df = pd.DataFrame([{
        "price_wna": user_input["max_price"],
        "rating": user_input["min_rating"]
    }])
    normalized_input = scaler.transform(user_df)
    max_price_scaled, min_rating_scaled = normalized_input[0]

    # Predict scores for each data point before filtering
    scores = accommodation_recommendation.predict(X)
    data['score'] = scores.flatten()  # Add the scores to the data

    # Filter data based on user criteria
    filtered_data = data[
        (data['rating'] >= min_rating_scaled) & 
        (data['price_wna'] <= max_price_scaled) & 
        (data['city'] == user_input['city'])  # Filter based on city
    ]
    
    # If no accommodations meet the criteria, return an empty DataFrame
    if filtered_data.empty:
        print("No accommodations found based on the given criteria.")
        return pd.DataFrame()  # Return empty DataFrame if no results

    # Get top N recommendations based on score
    recommendations = filtered_data.nlargest(top_n, 'score')

    # Inverse the scaling for price_wna and rating
    recommendations[['price_wna', 'rating']] = scaler.inverse_transform(
        recommendations[['price_wna', 'rating']]
    )

    # Select relevant columns for output
    selected_columns = ['name', 'rating', 'price_wna', 'city']
    available_columns = recommendations.columns.tolist()
    selected_columns = [col for col in selected_columns if col in available_columns]

    return recommendations[selected_columns]

# Function to recommend similar accommodations
def visited_accommodation_recommendations(accommodation_name, city_filter=None, max_price=None, top_n=5):
    # Ensure the accommodation exists in the data
    if accommodation_name not in data['name'].values:
        return {"error": f"Accommodation '{accommodation_name}' not found in data."}, 404

    # Feature extraction for similarity calculation
    features = np.hstack((encoded_city, data[['price_wna', 'rating']].values))
    accommodation_idx = data[data['name'] == accommodation_name].index[0]

    # Cosine similarity calculation
    similarity_scores = cosine_similarity(features[accommodation_idx].reshape(1, -1), features).flatten()
    data['similarity'] = similarity_scores

    # Handle optional filters for city and max_price
    if max_price is not None:
        max_price = float(max_price)

    filtered_data = data[data['name'] != accommodation_name]
    
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

    return recommendations[['name', 'rating', 'price_wna', 'city']].to_dict(orient="records")
