# Import the required libraries
import requests
import os

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
@app.route('/api/userData/register', methods=['POST'])
def register():
    try:
        # Forward the request to the user registration API
        response = requests.post(f'{DATA_API_BASE_URL}/register', json=request.get_json())
        return jsonify(response.json()), response.status_code
    except requests.exceptions.RequestException as e:
        return jsonify({"error": str(e)}), 500

# Login user
@app.route('/api/userData/login', methods=['POST'])
def login():
    try:
        # Forward the login request to the login API
        response = requests.post(f'{DATA_API_BASE_URL}/login', json=request.get_json())
        return jsonify(response.json()), response.status_code
    except requests.exceptions.RequestException as e:
        return jsonify({"error": str(e)}), 500

# Update user info
@app.route('/api/userData/update', methods=['PUT'])
def update_user():
    try:
        # Forward the update user information request to the update API
        response = requests.put(f'{DATA_API_BASE_URL}/update', json=request.get_json())
        return jsonify(response.json()), response.status_code
    except requests.exceptions.RequestException as e:
        return jsonify({"error": str(e)}), 500

# Delete user account
@app.route('/api/userData/delete', methods=['DELETE'])
def delete_user():
    try:
        # Forward the delete account request to the delete API
        response = requests.delete(f'{DATA_API_BASE_URL}/delete', json=request.get_json())
        return jsonify(response.json()), response.status_code
    except requests.exceptions.RequestException as e:
        return jsonify({"error": str(e)}), 500

""" END OF USER DATA APIs """


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000, debug=True)