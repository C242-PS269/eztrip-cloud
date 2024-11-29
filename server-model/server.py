import config.tour_preprocessing
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
        recommendations = config.tour_preprocessing.recommend(user_input)

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

if __name__ == '__main__':
    app.run(host=os.getenv('SERVER_HOST'), port=os.getenv('SERVER_PORT'))
