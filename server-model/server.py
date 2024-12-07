# Import required libraries for model preprocessing, logging, and server setup
import config.preprocessing_accommodation
import config.preprocessing_culinary
import config.generate_itinerary
import config.preprocessing_tour

import json
import os

from dotenv import load_dotenv
from flask import Flask, request, jsonify

# Load environment variables from .env file
load_dotenv()

# Initialize Flask app
app = Flask(__name__)

# API endpoint for the home route
@app.route('/', methods=['GET'])
def home():
    """
    Home endpoint to check if the server is active.

    Returns:
        JSON: A message indicating that the server is active.
    """
    return jsonify({"message": "EzTrip ML-Model Server is Active"}), 200

# API endpoint for getting tour recommendations
@app.route('/tours', methods=['POST'])
def get_tours():
    """
    API endpoint to get top 5 tour recommendations based on user input.

    The user provides a JSON object with inputs such as 'category', 'city',
    'min_rating', and 'max_price'. The server returns a list of tour 
    recommendations based on these inputs.

    Returns:
        JSON: A list of tour recommendations with their details.
    """
    try:
        # Get input from the user in JSON format
        user_input = request.get_json()

        # Get top 5 recommendations for the tour
        recommendations = config.preprocessing_tour.tour_recommendations(user_input)

        if not recommendations.empty:
            # Convert the dataframe to JSON
            result = recommendations.to_dict(orient='records')

            # Return the recommendations in the response
            return jsonify({"tours": result}), 200
        else:
            return jsonify({"message": "No recommendations found."}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# API endpoint for getting visited tour recommendations
@app.route('/tours/visited', methods=['POST'])
def get_visited_recommendations():
    """
    API endpoint to get tour recommendations based on a previously visited tour.

    This function allows the user to find similar tours to a place they visited
    based on features like price, rating, category, and city.

    Returns:
        JSON: A list of tour recommendations based on the previously visited tour.
    """
    try:
        # Get the input from the user in JSON format
        user_input = request.get_json()

        # Extract 'tour_name', 'city_filter', and 'max_price' from the user input
        tour_name = user_input.get('tour_name')
        city_filter = user_input.get('city_filter', None)
        max_price = user_input.get('max_price', None)

        # Get the top 5 recommendations based on the previously visited place
        recommendations = config.preprocessing_tour.visited_tour_recommendations(tour_name, city_filter, max_price)

        if recommendations:
            # Return the recommendations in the response
            return jsonify({"tours": recommendations}), 200
        else:
            return jsonify({"message": "No recommendations found."}), 404

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# API endpoint for getting accommodation recommendations
@app.route('/accommodations', methods=['POST'])
def get_accomodations():
    """
    API endpoint to get top 5 accommodation recommendations based on user input.

    The user provides a JSON object with inputs like 'category', 'city',
    'min_rating', and 'max_price', and the server returns a list of accommodation 
    recommendations matching these criteria.

    Returns:
        JSON: A list of accommodation recommendations with details.
    """
    try:
        # Get input from the user in JSON format
        user_input = request.get_json()

        # Get top 5 recommendations for accommodations
        recommendations = config.preprocessing_accommodation.accommodation_recommendations(user_input)

        if not recommendations.empty:
            # Convert the dataframe to JSON
            result = recommendations.to_dict(orient='records')
            # Return the recommendations in the response
            return jsonify({"accomodations": result}), 200
        else:
            return jsonify({"message": "No accomodations found."}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# API endpoint for accommodation recommendations based on previously visited accommodation
@app.route('/accommodations/visited', methods=['POST'])
def get_visited_accommodation_recommendations():

    """
    API endpoint to recommend similar accommodations based on a previously visited accommodation.

    This endpoint receives a POST request containing user input with the name of a previously visited 
    accommodation, and optional filters for city and maximum price. It returns the top 5 recommendations 
    of similar accommodations.

    Returns:
    JSON:
        - A list of recommended accommodations, including the name, rating, price, and city.
        - An error message if the accommodation name is not found or another error occurs.
    """

    try:
        # Get the input from the user in JSON format
        user_input = request.get_json()

        # Extract the accommodation name, city filter, and max price
        accommodation_name = user_input.get('accommodation_name')
        city_filter = user_input.get('city_filter', None)
        max_price = user_input.get('max_price', None)

        # Get the top 5 recommendations based on previously visited accommodation
        recommendations = config.preprocessing_accommodation.visited_accommodation_recommendations(accommodation_name, city_filter, max_price)

        # Check if there's an error (e.g., accommodation not found)
        if isinstance(recommendations, dict) and 'error' in recommendations:
            return jsonify(recommendations), 404

        # Return the recommendations in the response
        return jsonify({"accomodations": recommendations}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# API endpoint for getting culinary recommendations
@app.route('/culinaries', methods=['POST'])
def get_culinaries():
    """
    API endpoint to get culinary recommendations based on user input.

    The user provides a JSON object with 'category', 'city', 'min_rating',
    and 'max_price'. The server returns culinary recommendations matching these 
    criteria.

    Returns:
        JSON: A list of culinary recommendations with details.
    """
    try:
        user_input = request.get_json()

        # Validate the required fields
        if not all(key in user_input for key in ['category', 'city', 'min_rating', 'max_price']):
            return jsonify({"error": "Missing one or more required fields: 'category', 'city', 'min_rating', 'max_price'"}), 400

        # Get the top 5 culinary recommendations
        recommendations = config.preprocessing_culinary.culinary_recommendations(user_input)
        
        if not recommendations.empty:
            # Convert the dataframe to JSON
            result = recommendations.to_dict(orient='records')
                
            return jsonify({"culinaries": result}), 200
        else:
            return jsonify({"message": "No recommendations found."}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
# API Endpoint for getting similar culinary recommendations
@app.route('/culinaries/visited', methods=['POST'])
def get_similar_culinary_recommendations():

    """
    API endpoint to get culinary recommendations based on a previously visited culinary place.

    This function allows the user to find similar culinary places to one they have already visited
    based on features like price, rating, category, and city.

    Returns:
        JSON: A list of culinary recommendations based on the previously visited culinary place.
    """

    try:
        # Get the input from the user in JSON format
        user_input = request.get_json()

        # Extract 'culinary_name', 'city_filter', and 'max_price' from the user input
        culinary_name = user_input.get('culinary_name')
        city_filter = user_input.get('city_filter', None)
        max_price = user_input.get('max_price', None)

        # Get the top 5 recommendations based on the previously visited place
        recommendations = config.preprocessing_culinary.visited_culinary_recommendations(culinary_name, city_filter, max_price)

        if recommendations:
            # Return the recommendations in the response
            return jsonify({"culinaries": recommendations}), 200
        else:
            return jsonify({"message": "No recommendations found."}), 404

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
# API endpoint for generating itineraries based on user budget
@app.route('/itineraries', methods=['POST'])
def get_itineraries():
    """
    API endpoint to generate an itinerary based on the user's budget.

    The user provides their budget and optionally a city. The server generates 
    an itinerary with a combination of tours, accommodations, and culinary 
    experiences based on the budget.

    Returns:
        JSON: A generated itinerary or error message.
    """
    try:
        # Get user input
        user_input = request.get_json()

        if not user_input:
            return jsonify({"error": "Invalid JSON in request."}), 400

        # Extract budget and city (optional)
        user_budget = user_input.get("budget")
        city = user_input.get("city")  # City is optional

        # Validate the budget field
        if not user_budget:
            return jsonify({"error": "Missing 'budget' field in the request."}), 400

        # Ensure budget is a valid number (int or float)
        if not isinstance(user_budget, (int, float)):
            return jsonify({"error": "'budget' must be a number."}), 400

        # Generate the itinerary
        try:
            itinerary = config.generate_itinerary.generate_itineraries(user_budget, city)

        except Exception as e:
            return jsonify({"error": "Failed to generate itinerary due to internal error."}), 500

        # Check if the itinerary is empty or invalid
        if not itinerary or isinstance(itinerary, dict) and 'error' in itinerary:
            return jsonify({"error": "No itinerary could be generated with the provided budget."}), 400

        # Return the generated itinerary in the response
        return jsonify({"itinerary": itinerary}), 200

    except Exception as e:
        return jsonify({"error": "An unexpected error occurred."}), 500

# Run the Flask app
if __name__ == '__main__':
    app.run(host=os.getenv('MODEL_HOST'), port=os.getenv('MODEL_PORT'), debug=True)