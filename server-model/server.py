# Import required libraries
import config.preprocessing_tour
import config.preprocessing_accommodation
import config.preprocessing_culinary
import config.setup_logging
import config.generate_itinerary

import json
import os

from dotenv import load_dotenv
from flask import Flask, request, jsonify

# Load environment variables
load_dotenv()

# Logging varibles
logger = config.setup_logging.log()

# Initialize Flask app
app = Flask(__name__)

# API endpoint for recommendations
@app.route('/tours', methods=['POST'])
def get_tours():
    try:
        # Get input from the user in JSON format
        user_input = request.get_json()

        # Get top 5 recommendations
        recommendations = config.preprocessing_tour.tour_recommendations(user_input)

        if not recommendations.empty:
            # Convert the dataframe to JSON
            result = recommendations.to_dict(orient='records')

            # Pretty print and save to file
            with open('tours.json', 'w') as f:
                json.dump(result, f, indent=4)  # Pretty print with indentation

            # Return the recommendations in the response
            return jsonify({"recommendations": result}), 200
        else:
            return jsonify({"message": "No recommendations found."}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# API endpoint for visited recommendations
@app.route('/tours/visited', methods=['POST'])
def get_visited_recommendations():
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
            # Pretty print and save the result to a file
            with open('visited.json', 'w') as f:
                json.dump(recommendations, f, indent=4)  # Pretty print with indentation

            # Return the recommendations in the response
            return jsonify({"recommendations": recommendations}), 200
        else:
            return jsonify({"message": "No recommendations found."}), 404

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
# API endpoint for accommodations
@app.route('/accommodations', methods=['POST'])
def get_accomodations():
    try:
        # Get input from the user in JSON format
        user_input = request.get_json()

        # Get top 5 recommendations
        recommendations = config.preprocessing_accommodation.accommodation_recommendations(user_input)

        if not recommendations.empty:
            # Convert the dataframe to JSON
            result = recommendations.to_dict(orient='records')

            # Pretty print and save to file
            with open('accomodations.json', 'w') as f:
                json.dump(result, f, indent=4)  # Pretty print with indentation

            # Return the recommendations in the response
            return jsonify({"accomodations": result}), 200
        else:
            return jsonify({"message": "No accomodations found."}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/culinaries', methods=['POST'])
def get_culinaries():
    try:
        user_input = request.get_json()
        if not all(key in user_input for key in ['category', 'city', 'min_rating', 'max_price']):
            return jsonify({"error": "Missing one or more required fields: 'category', 'city', 'min_rating', 'max_price'"}), 400

        recommendations = config.preprocessing_culinary.culinary_recommendations(user_input)
        if not recommendations.empty:
            # Convert the dataframe to JSON
            result = recommendations.to_dict(orient='records')

            # Pretty print and save to file
            with open('culinaries.json', 'w') as f:
                json.dump(result, f, indent=4)  # Pretty print with indentation
                
            return jsonify({"culinaries": result}), 200
        else:
            return jsonify({"message": "No recommendations found."}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
# Define the /itineraries endpoint
@app.route('/itineraries', methods=['POST'])
def get_itineraries():
    try:
        # Get user input
        user_input = request.get_json()
        
        if not user_input:
            return jsonify({"error": "Invalid JSON in request."}), 400
        
        # Debug log to verify input
        print(f"User Input: {user_input}")

        user_budget = user_input.get("budget")
        city = user_input.get("city")  # City is optional

        if not user_budget:
            return jsonify({"error": "Missing 'budget' field in the request."}), 400

        # Validate that user_budget is a number (int or float)
        if not isinstance(user_budget, (int, float)):
            return jsonify({"error": "'budget' must be a number."}), 400

        # Generate itinerary
        try:
            itinerary = config.generate_itinerary.generate_itineraries(user_budget, city)
        except Exception as e:
            print(f"Error in generating itinerary: {str(e)}")  # Log error
            return jsonify({"error": "Failed to generate itinerary due to internal error."}), 500

        # Check if the itinerary is empty or None
        if not itinerary or isinstance(itinerary, dict) and 'error' in itinerary:
            return jsonify({"error": "No itinerary could be generated with the provided budget."}), 400

        # Debug log to verify generated itinerary
        print(f"Generated Itinerary: {itinerary}")

        # Return the generated itinerary in the response
        return jsonify({"itinerary": itinerary}), 200

    except Exception as e:
        # Log any unexpected error
        print(f"Unexpected Error: {str(e)}")
        return jsonify({"error": "An unexpected error occurred."}), 500

# Run the Flask app
if __name__ == '__main__':
    app.run(host=os.getenv('MODEL_HOST'), port=os.getenv('MODEL_PORT'), debug=True)