# Import the required libraries
import requests 

from flask import Flask, request, jsonify
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

# Create a Flask application
app = Flask(__name__)

# Define the base URLs for the data APIs
DATA_API_BASE_URL = 'http://localhost:5000'
MODEL_API_BASE_URL = 'http://localhost:4000'

""" START OF USER DATA APIs """

# Register user
@app.route('/api/data/user/register', methods=['POST'])
def register_user():
    try:
        # Forward the request to the user registration API
        response = requests.post(f'{DATA_API_BASE_URL}/register', json=request.get_json())
        return jsonify(response.json()), response.status_code
    except requests.exceptions.RequestException as e:
        return jsonify({"error": str(e)}), 500

# Login user
@app.route('/api/data/user/login', methods=['POST'])
def login_user():
    try:
        # Forward the login request to the login API
        response = requests.post(f'{DATA_API_BASE_URL}/login', json=request.get_json())
        return jsonify(response.json()), response.status_code
    except requests.exceptions.RequestException as e:
        return jsonify({"error": str(e)}), 500

# Update user info
@app.route('/api/data/user/update', methods=['PUT'])
def update_user():
    try:
        # Forward the update user information request to the update API
        response = requests.put(f'{DATA_API_BASE_URL}/update', json=request.get_json())
        return jsonify(response.json()), response.status_code
    except requests.exceptions.RequestException as e:
        return jsonify({"error": str(e)}), 500

# Delete user account
@app.route('/api/data/user/account/delete', methods=['DELETE'])
def delete_user():
    try:
        # Forward the delete account request to the delete API
        response = requests.delete(f'{DATA_API_BASE_URL}/delete', json=request.get_json())
        return jsonify(response.json()), response.status_code
    except requests.exceptions.RequestException as e:
        return jsonify({"error": str(e)}), 500

""" END OF USER DATA APIs """

""" START OF MODEL APIs """

@app.route('/api/model/recommendations/tours', methods=['POST'])
def get_tour_recommendations():
    try:
        response = requests.post(f'{MODEL_API_BASE_URL}/tours', json=request.get_json())
        return jsonify(response.json()), response.status_code
    except requests.exceptions.RequestException as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/model/recommendations/tours/visited', methods=['POST'])
def get_visited_tour_recommendations():
    try:
        response = requests.post(f'{MODEL_API_BASE_URL}/tours/visited', json=request.get_json())
        return jsonify(response.json()), response.status_code
    except requests.exceptions.RequestException as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/model/recommendations/accommodations', methods=['POST'])
def get_accommodation_recommendations():
    try:
        response = requests.post(f'{MODEL_API_BASE_URL}/accommodations', json=request.get_json())
        return jsonify(response.json()), response.status_code
    except requests.exceptions.RequestException as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/model/recommendations/accommodations/visited', methods=['POST'])
def get_visited_accommodation_recommendations():
    try:
        response = requests.post(f'{MODEL_API_BASE_URL}/accommodations/visited', json=request.get_json())
        return jsonify(response.json()), response.status_code
    except requests.exceptions.RequestException as e:
        return jsonify({"error": str(e)}), 500
    
@app.route('/api/model/recommendations/culinaries', methods=['POST'])
def get_culinary_recommendations():
    try:
        response = requests.post(f'{MODEL_API_BASE_URL}/culinaries', json=request.get_json())
        return jsonify(response.json()), response.status_code
    except requests.exceptions.RequestException as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/model/recommendations/culinaries/visited', methods=['POST'])
def get_visited_culinary_recommendations():
    try:
        response = requests.post(f'{MODEL_API_BASE_URL}/culinaries/visited', json=request.get_json())
        return jsonify(response.json()), response.status_code
    except requests.exceptions.RequestException as e:
        return jsonify({"error": str(e)}), 500
    
@app.route('/api/model/recommendations/itineraries', methods=['POST'])
def generate_itinerary_recommendations():
    try:
        response = requests.post(f'{MODEL_API_BASE_URL}/itineraries', json=request.get_json())
        return jsonify(response.json()), response.status_code
    except requests.exceptions.RequestException as e:
        return jsonify({"error": str(e)}), 500

""" END OF MODEL APIs """

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000, debug=True)