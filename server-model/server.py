# Import required libraries
import config.preprocessing_tour
import config.preprocessing_accommodation
import config.preprocessing_culinary
import config.setup_logging
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
@app.route('/recommendations', methods=['POST'])
def get_recommendations():
    try:
        # Get input from the user in JSON format
        user_input = request.get_json()

        # Get top 5 recommendations
        recommendations = config.preprocessing_tour.tour_recommendations(user_input)

        if not recommendations.empty:
            # Convert the dataframe to JSON
            result = recommendations.to_dict(orient='records')

            # Pretty print and save to file
            with open('recommendations.json', 'w') as f:
                json.dump(result, f, indent=4)  # Pretty print with indentation

            # Return the recommendations in the response
            return jsonify({"recommendations": result}), 200
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
def culinaries():
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

# Run the Flask app
if __name__ == '__main__':
    app.run(host=os.getenv('SERVER_HOST'), port=os.getenv('SERVER_PORT'))