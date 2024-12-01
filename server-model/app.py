from flask import Flask, request, jsonify
import pandas as pd
import tensorflow as tf
import numpy as np
import json
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import MinMaxScaler

app = Flask(__name__)

# Load dataset
DATASET_PATH = "data/Wisata.xlsx"
MODEL_PATH = "models/tour_recommendation_v1.1.h5"

data = pd.read_excel(DATASET_PATH)
model = tf.keras.models.load_model(MODEL_PATH)

# Rename columns to match the required format
selected_columns = {
    'Name': 'name',
    'Rating': 'rating',
    'Kategori': 'category',
    'Harga Tiket Masuk WNA Dewasa': 'price_wna',
    'Kota/Kabupaten': 'city',
    'Jalan': 'address',
    'Google.Maps': 'google_maps'
}

# Rename column
data = data.rename(columns=selected_columns)

# Drop rows with missing values in important columns
data.dropna(subset=['name', 'rating', 'category', 'price_wna', 'city', 'address', 'google_maps'], inplace=True)

# Normalize price and rating
scaler = MinMaxScaler()
data[['price_wna', 'rating']] = scaler.fit_transform(data[['price_wna', 'rating']])

# Encode categorical features
category_encoder = LabelEncoder()
data['category_encoded'] = category_encoder.fit_transform(data['category'])

city_encoder = LabelEncoder()
data['city_encoded'] = city_encoder.fit_transform(data['city'])

# Data preprocessing function
def preprocess_input(user_input, dataset):
    # Convert input to vector representation (dummy implementation)
    vector = np.zeros((1, dataset.shape[1]))  # Replace with proper encoding logic
    return vector

# Recommend similar wisata based on previous visits
def recommend_similar_wisata(wisata_name, city_filter=None, max_price=None, top_n=5):
    # Ensure the wisata name is in the dataset
    if wisata_name not in data['name'].values:
        print(f"Tempat wisata '{wisata_name}' tidak ditemukan dalam data.")
        return pd.DataFrame()

    # Prepare features for cosine similarity calculation
    features = np.hstack((
        data[['category_encoded', 'city_encoded']].values,
        data[['price_wna', 'rating']].values
    ))

    # Get the index of the visited wisata
    wisata_idx = data[data['name'] == wisata_name].index[0]

    # Compute cosine similarity with all other wisata
    similarity_scores = cosine_similarity(features[wisata_idx].reshape(1, -1), features).flatten()

    # Add similarity scores to the dataframe
    data['similarity'] = similarity_scores

    # Filter based on max_price and city_filter
    filtered_data = data[data['name'] != wisata_name]
    if city_filter:
        filtered_data = filtered_data[filtered_data['city'] == city_filter]
    if max_price is not None:
        filtered_data = filtered_data[filtered_data['price_wna'] <= max_price]

    # Return the top-N most similar wisata
    recommendations = filtered_data.nlargest(top_n, 'similarity') if not filtered_data.empty else pd.DataFrame()

    return recommendations[['name', 'rating', 'price_wna', 'city', 'category', 'address', 'google_maps', 'similarity']]

# API endpoint
@app.route('/recommend', methods=['POST'])
def recommend():
    user_data = request.json
    
    # Ensure 'visited' key is in input data
    if not user_data or "visited" not in user_data:
        return jsonify({"error": "Invalid input. Please provide 'visited' key."}), 400
    
    visited_tours = user_data["visited"]  # List of visited tours
    
    # Additional optional filters
    city_filter = user_data.get('city', None)
    max_price = user_data.get('max_price', None)

    recommendations = []
    for wisata in visited_tours:
        # Get recommendations for each visited wisata
        wisata_recommendations = recommend_similar_wisata(wisata, city_filter, max_price)
        recommendations.extend(wisata_recommendations.to_dict(orient="records"))
    
    return jsonify({"recommendations": recommendations})

if __name__ == '__main__':
    app.run(debug=True)
