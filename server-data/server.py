# Import the required libraries
import mysql.connector
import requests
import json
import random
import string
import uuid

import re
import os

from flask import Flask, request, jsonify
from config.sql_engine import Config, test_connection, get_engine  # Import the config and functions
from dotenv import load_dotenv
from decimal import Decimal

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Load configurations from config.sql_engine
app.config.from_mapping({
    'MYSQL_HOST': Config['host'],
    'MYSQL_USER': Config['username'],
    'MYSQL_PASSWORD': Config['password'],
    'MYSQL_DATABASE': Config['database'],
    'SERVER_HOST': os.getenv('SERVER_HOST'),
    'SERVER_PORT': os.getenv('SERVER_PORT')
})

# Test database connection at startup (optional)
test_connection()

# MySQL database connection setup using the engine from config.sql_engine
def get_db_connection():
    engine = get_engine()  # Get the engine from config
    return engine.connect()

# MySQL database connection setup
def get_db_connection():
    return mysql.connector.connect(
        host=app.config['MYSQL_HOST'],
        user=app.config['MYSQL_USER'],
        password=app.config['MYSQL_PASSWORD'],
        database=app.config['MYSQL_DATABASE']
    )

# Helper function for username validation
def validate_username(username):
    return bool(re.match(r'^[A-Za-z0-9._]+$', username))

# Function to generate a random alphanumeric ID
def generate_random_id(length=36):
    """Generate a random alphanumeric string for the user ID."""
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))

# API endpoint for registration
@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()

    username = data.get('username')
    email = data.get('email')
    password = data.get('password')
    confirm_password = data.get('confirm_password')
    phone_number = data.get('phone_number')

    # Validate data
    if not validate_username(username):
        return jsonify({'error': 'Username can only contain letters, numbers, ".", and "_".'}), 400
    if len(password) < 8:
        return jsonify({'error': 'Password must be at least 8 characters long.'}), 400
    if password != confirm_password:
        return jsonify({'error': 'Passwords do not match.'}), 400
    if not email or not phone_number:
        return jsonify({'error': 'Email and phone number are required.'}), 400

    # Check if user already exists
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username = %s OR email = %s", (username, email))
    existing_user = cursor.fetchone()
    conn.close()

    if existing_user:
        return jsonify({'error': 'Username or email already exists.'}), 400

    # Generate random user ID
    user_id = generate_random_id()

    # Store the plain-text password (not recommended for production)
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO users (id, username, email, password, phone_number) VALUES (%s, %s, %s, %s, %s)",
                   (user_id, username, email, password, phone_number))
    conn.commit()
    conn.close()

    return jsonify({'message': 'User registered successfully!'}), 201

# API endpoint for login
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()

    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({'error': 'Username and password are required'}), 400

    # Check the database for the user
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
    user = cursor.fetchone()

    # If user not found or password doesn't match
    if not user or user[3] != password:  # Assuming password is stored in the 4th column (index 3)
        conn.close()
        return jsonify({'error': 'Invalid username or password'}), 401

    # Return success and user_id (assuming user[0] is user_id)
    user_id = user[0]
    conn.close()
    return jsonify({'message': 'Login successful', 'user_id': user_id}), 200

# API endpoint to update user info (email, phone, password)
@app.route('/update', methods=['PUT'])
def update_user():
    data = request.get_json()

    username = data.get('username')
    current_password = data.get('current_password')
    new_password = data.get('new_password')
    new_email = data.get('new_email')
    new_phone = data.get('new_phone')

    # Validate data
    if not username or not current_password:
        return jsonify({'error': 'Username and current password are required.'}), 400

    # Find user by username
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
    user = cursor.fetchone()

    if not user or user[3] != current_password:  # user[3] is the password field (plain-text comparison)
        conn.close()
        return jsonify({'error': 'Invalid credentials.'}), 401

    # Update user information
    if new_password:
        cursor.execute("UPDATE users SET password = %s WHERE username = %s", (new_password, username))

    if new_email:
        cursor.execute("UPDATE users SET email = %s WHERE username = %s", (new_email, username))

    if new_phone:
        cursor.execute("UPDATE users SET phone_number = %s WHERE username = %s", (new_phone, username))

    conn.commit()
    conn.close()

    return jsonify({'message': 'User information updated successfully.'}), 200

# API endpoint to delete a user account
@app.route('/delete', methods=['DELETE'])
def delete_user():
    data = request.get_json()

    username = data.get('username')
    password = data.get('password')

    # Validate data
    if not username or not password:
        return jsonify({'error': 'Username and password are required.'}), 400

    # Find user by username
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
    user = cursor.fetchone()

    if not user or user[3] != password:  # user[3] is the password field (plain-text comparison)
        conn.close()
        return jsonify({'error': 'Invalid credentials.'}), 401

    # Delete user from the database
    cursor.execute("DELETE FROM users WHERE username = %s", (username,))
    conn.commit()
    conn.close()

    return jsonify({'message': 'User account deleted successfully.'}), 200

# API endpoint to generate itineraries and save to the database
@app.route('/itineraries', methods=['POST'])
def generate_and_save_itinerary():
    data = request.get_json()

    user_id = data.get('user_id')  # Get user_id from the request
    budget = data.get('budget')
    city = data.get('city')

    if not user_id or not budget:
        return jsonify({'error': 'User ID and budget are required'}), 400

    # Check if the user exists in the database
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))
    user = cursor.fetchone()
    conn.close()

    if not user:
        return jsonify({'error': 'User not found'}), 404

    # Call the ML model server (localhost:4000) to generate itineraries
    itinerary_request = {
        'budget': budget,
        'city': city
    }

    try:
        # Make the request to the ML server for itinerary generation
        itinerary_response = requests.post('http://localhost:4000/itineraries', json=itinerary_request)
        
        if itinerary_response.status_code != 200:
            return jsonify({'error': 'Failed to generate itinerary from model server'}), 500

        itinerary_data = itinerary_response.json()

        total_cost = itinerary_data["itinerary"].get('total_cost', 0.00)
        remaining_budget = budget - total_cost

        itinerary_id = str(uuid.uuid4())

        # Save generated itinerary to the database
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute(""" 
            INSERT INTO itineraries (id, user_id, itinerary_data, total_cost, remaining_budget, budget)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (itinerary_id, user_id, json.dumps(itinerary_data), total_cost, remaining_budget, budget))

        conn.commit()
        conn.close()

        return jsonify({
            'message': 'Itinerary saved successfully',
            'itinerary': itinerary_data["itinerary"],
            'total_cost': total_cost,
            'remaining_budget': remaining_budget
        }), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

# API endpoint to get all itineraries for a specific user
@app.route('/itineraries/user/<user_id>', methods=['GET'])
def get_user_itineraries(user_id):
    try:
        # Connect to the database
        conn = get_db_connection()
        cursor = conn.cursor()

        # Query to get all itineraries for the specific user_id
        cursor.execute("SELECT id, itinerary_data, total_cost, remaining_budget, budget, created_at FROM itineraries WHERE user_id = %s", (user_id,))
        itineraries = cursor.fetchall()

        if not itineraries:
            return jsonify({'message': 'No itineraries found for this user'}), 404

        # Prepare the list of itineraries to return
        itineraries_list = []
        for itinerary in itineraries:
            itinerary_dict = {
                'id': itinerary[0],
                'itinerary_data': json.loads(str(itinerary[1])),  # Convert JSON string back to dictionary
                'total_cost': itinerary[2],
                'remaining_budget': itinerary[3],
                'budget': itinerary[4],
                'created_at': itinerary[5].strftime('%Y-%m-%d %H:%M:%S')  # Format created_at as string
            }
            itineraries_list.append(itinerary_dict)

        conn.close()

        return jsonify({'itineraries': itineraries_list}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

# API endpoint to delete an itinerary by UUID
@app.route('/itineraries/<uuid:id>', methods=['DELETE'])
def delete_itinerary(id):
    try:
        # Convert the UUID object to string if needed (for database operations)
        id_str = str(id)

        # Connect to the database
        conn = get_db_connection()
        cursor = conn.cursor()

        # Delete the itinerary from the database
        cursor.execute("DELETE FROM itineraries WHERE id = %s", (id_str,))
        conn.commit()

        # Check if any row was deleted
        if cursor.rowcount == 0:
            conn.close()
            return jsonify({'error': 'Itinerary not found'}), 404

        conn.close()

        return jsonify({'message': 'Itinerary deleted successfully'}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(host=os.getenv('SERVER_HOST'), port=os.getenv('SERVER_PORT'), debug=True)