# Import the required libraries
import requests 

from flask import Flask, request, jsonify
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

# Create a Flask application
app = Flask(__name__)

# Define the base URLs for the data APIs
DATA_API_BASE_URL = 'http://localhost:5000' # change this with deployed data server
MODEL_API_BASE_URL = 'http://localhost:4000' # change this with deployed model server

""" START OF USER DATA APIs """

# Register user
@app.route('/api/data/user/account/register', methods=['POST'])
def register_user():
    try:
        # Forward the request to the user registration API
        response = requests.post(f'{DATA_API_BASE_URL}/user/account/register', json=request.get_json())
        return jsonify(response.json()), response.status_code
    except requests.exceptions.RequestException as e:
        return jsonify({"error": str(e)}), 500

# Login user
@app.route('/api/data/user/account/login', methods=['POST'])
def login_user():
    try:
        # Forward the login request to the login API
        response = requests.post(f'{DATA_API_BASE_URL}/user/account/login', json=request.get_json())
        return jsonify(response.json()), response.status_code
    except requests.exceptions.RequestException as e:
        return jsonify({"error": str(e)}), 500

# Update user info
@app.route('/api/data/user/account/update', methods=['PUT'])
def update_user():
    try:
        # Forward the update user information request to the update API
        response = requests.put(f'{DATA_API_BASE_URL}/user/account/update', json=request.get_json())
        return jsonify(response.json()), response.status_code
    except requests.exceptions.RequestException as e:
        return jsonify({"error": str(e)}), 500

# Delete user account
@app.route('/api/data/user/account/delete', methods=['DELETE'])
def delete_user():
    try:
        # Forward the delete account request to the delete API
        response = requests.delete(f'{DATA_API_BASE_URL}/user/account/delete', json=request.get_json())
        return jsonify(response.json()), response.status_code
    except requests.exceptions.RequestException as e:
        return jsonify({"error": str(e)}), 500
    
""" END OF USER DATA APIs """

""" START OF ITINERARIES APIs """

# Generate itineraries and save the user preferences
@app.route('/api/data/features/itineraries', methods=['POST'])
def generate_and_save_itinerary_recommendations():
    try:
        # Forward the request to the backend API
        response = requests.post(f'{DATA_API_BASE_URL}/features/itineraries', json=request.get_json())
        return jsonify(response.json()), response.status_code
    except requests.exceptions.RequestException as e:
        return jsonify({"error": f"Failed to forward the request: {str(e)}"}), 500

# Get all itineraries by user
@app.route('/api/data/features/itineraries/user/<user_id>', methods=['GET'])
def get_user_itineraries(user_id):
    try:
        # Forward the request to the backend API
        response = requests.get(f'{DATA_API_BASE_URL}/features/itineraries/user/{user_id}')
        return jsonify(response.json()), response.status_code
    except requests.exceptions.RequestException as e:
        return jsonify({"error": f"Failed to retrieve itineraries: {str(e)}"}), 500

# Delete an itinerary by UUID
@app.route('/api/data/features/itineraries/<uuid:id>', methods=['DELETE'])
def delete_itinerary(id):
    try:
        # Forward the delete request to the backend API
        response = requests.delete(f'{DATA_API_BASE_URL}/features/itineraries/{id}')
        return jsonify(response.json()), response.status_code
    except requests.exceptions.RequestException as e:
        return jsonify({"error": f"Failed to delete itinerary: {str(e)}"}), 500

""" END OF ITINERARIES APIs """

""" START OF REVIEWS APIs """

# Submit Review
@app.route('/api/data/reviews/submit', methods=['POST'])
def submit_review():
    try:
        # Forward the review submission request to the reviews API
        response = requests.post(f'{DATA_API_BASE_URL}/places/reviews', json=request.get_json())
        return jsonify(response.json()), response.status_code
    except requests.exceptions.RequestException as e:
        return jsonify({"error": str(e)}), 500

# Get Reviews for a Place
@app.route('/api/data/reviews/<place_type>/<place_id>', methods=['GET'])
def get_reviews(place_type, place_id):
    try:
        # Forward the request to fetch reviews for a place
        response = requests.get(f'{DATA_API_BASE_URL}/places/reviews/{place_type}/{place_id}')
        return jsonify(response.json()), response.status_code
    except requests.exceptions.RequestException as e:
        return jsonify({"error": str(e)}), 500

""" END OF REVIEWS APIs """

""" START OF EXPENSES APIs """

# Add Expense
@app.route('/api/data/user/expenses', methods=['POST'])
def add_expense():
    try:
        # Forward the request to the add expense API
        response = requests.post(f'{DATA_API_BASE_URL}/user/expenses', json=request.get_json())
        return jsonify(response.json()), response.status_code
    except requests.exceptions.RequestException as e:
        return jsonify({"error": str(e)}), 500

# Get All Expenses for a User
@app.route('/api/data/user/expenses/<user_id>', methods=['GET'])
def get_expenses(user_id):
    try:
        # Forward the request to get expenses for a user
        response = requests.get(f'{DATA_API_BASE_URL}/user/expenses/{user_id}')
        return jsonify(response.json()), response.status_code
    except requests.exceptions.RequestException as e:
        return jsonify({"error": str(e)}), 500

# Get Total Expenses by Category for a User
@app.route('/api/data/user/expenses/total/<user_id>', methods=['GET'])
def get_expenses_total(user_id):
    try:
        # Forward the request to get total expenses by category for a user
        response = requests.get(f'{DATA_API_BASE_URL}/user/expenses/total/{user_id}')
        return jsonify(response.json()), response.status_code
    except requests.exceptions.RequestException as e:
        return jsonify({"error": str(e)}), 500

# Update Expense
@app.route('/api/data/user/expenses/<expense_id>', methods=['PUT'])
def update_expense(expense_id):
    try:
        # Forward the request to update an expense
        response = requests.put(f'{DATA_API_BASE_URL}/user/expenses/{expense_id}', json=request.get_json())
        return jsonify(response.json()), response.status_code
    except requests.exceptions.RequestException as e:
        return jsonify({"error": str(e)}), 500

# Delete Expense
@app.route('/api/data/user/expenses/<expense_id>', methods=['DELETE'])
def delete_expense(expense_id):
    try:
        # Forward the request to delete an expense
        response = requests.delete(f'{DATA_API_BASE_URL}/expenses/{expense_id}')
        return jsonify(response.json()), response.status_code
    except requests.exceptions.RequestException as e:
        return jsonify({"error": str(e)}), 500

""" END OF EXPENSES APIs """

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