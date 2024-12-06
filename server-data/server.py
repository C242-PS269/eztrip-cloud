# Import the required libraries
import mysql.connector
import requests
import json
import random
import string
import uuid
from textblob import TextBlob
from googletrans import Translator
import datetime

import re
import os

from flask import Flask, request, jsonify
from config.sql_engine import Config, test_connection, get_engine  # Import the config and functions
from dotenv import load_dotenv

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

    conn = get_db_connection()
    cursor = conn.cursor()

    # Step 1: Find user by username
    cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
    user = cursor.fetchone()

    if not user or user[3] != password:  # user[3] is the password field (plain-text comparison)
        cursor.close()
        conn.close()
        return jsonify({'error': 'Invalid credentials.'}), 401

    user_id = user[0]  # Assuming user[0] is the user_id

    # Step 2: Delete related data from dependent tables
    cursor.execute("DELETE FROM itineraries WHERE user_id = %s", (user_id,))
    cursor.execute("DELETE FROM accommodations_reviews WHERE user_id = %s", (user_id,))
    cursor.execute("DELETE FROM tours_reviews WHERE user_id = %s", (user_id,))
    cursor.execute("DELETE FROM culinary_reviews WHERE user_id = %s", (user_id,))
    cursor.execute("DELETE FROM expenses WHERE user_id = %s", (user_id,))

    # Step 3: Delete the user from the users table
    cursor.execute("DELETE FROM users WHERE id = %s", (user_id,))
    conn.commit()

    cursor.close()
    conn.close()

    return jsonify({'message': 'User account and all related data deleted successfully. Thankyou for using EzTrip!, Sorry we have to see you go :('}), 200

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

# Function to analyze sentiment
def analyze_sentiment(text):
    blob = TextBlob(text)
    polarity = blob.sentiment.polarity

    if polarity > 0.1:
        return 'positive'
    elif polarity < -0.1:
        return 'negative'
    else:
        return 'neutral'

# Function to translate review to English (if needed)
def translate_to_english(text):
    translator = Translator()
    translated = translator.translate(text, src='auto', dest='en')
    return translated.text

# POST /reviews (Submit Review)
@app.route('/reviews', methods=['POST'])
def submit_review():
    data = request.get_json()
    user_id = data['user_id']
    place_id = data['place_id']
    place_type = data['place_type']
    rating = data['rating']
    reviews = data['reviews']

    # Step 1: Check if the user_id exists in the users table
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))
    user = cursor.fetchone()
    
    if not user:
        cursor.close()
        conn.close()
        return jsonify({"error": "User does not exist"}), 400
    
    # Step 2: Translate review to English (if necessary)
    translated_review = translate_to_english(reviews)
    
    # Step 3: Analyze sentiment of the translated review
    sentiment = analyze_sentiment(translated_review)

    # Step 4: Proceed with review submission
    review_id = str(uuid.uuid4())
    if place_type == 'accommodations':
        cursor.execute("""
            INSERT INTO accommodations_reviews (id, user_id, accommodations_id, rating, reviews, sentiment)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (review_id, user_id, place_id, rating, translated_review, sentiment))
    elif place_type == 'tours':
        cursor.execute("""
            INSERT INTO tours_reviews (id, user_id, tours_id, rating, reviews, sentiment)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (review_id, user_id, place_id, rating, translated_review, sentiment))
    elif place_type == 'culinaries':
        cursor.execute("""
            INSERT INTO culinary_reviews (id, user_id, culinaries_id, rating, reviews, sentiment)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (review_id, user_id, place_id, rating, translated_review, sentiment))
    else:
        cursor.close()
        conn.close()
        return jsonify({"error": "Invalid place type"}), 400
    
    conn.commit()
    cursor.close()
    conn.close()
    
    return jsonify({"message": "Review submitted successfully", "review_id": review_id}), 201

# GET /reviews/{place_type}/{place_id} (Get Reviews for a Place)
@app.route('/reviews/<place_type>/<place_id>', methods=['GET'])
def get_reviews(place_type, place_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    if place_type == 'accommodations':
        cursor.execute("""
            SELECT ar.id, u.username, ar.rating, ar.reviews, ar.sentiment 
            FROM accommodations_reviews ar
            JOIN users u ON ar.user_id = u.id
            WHERE ar.accommodations_id = %s
        """, (place_id,))
    elif place_type == 'tours':
        cursor.execute("""
            SELECT tr.id, u.username, tr.rating, tr.reviews, tr.sentiment 
            FROM tours_reviews tr
            JOIN users u ON tr.user_id = u.id
            WHERE tr.tours_id = %s
        """, (place_id,))
    elif place_type == 'culinaries':
        cursor.execute("""
            SELECT cr.id, u.username, cr.rating, cr.reviews, cr.sentiment 
            FROM culinary_reviews cr
            JOIN users u ON cr.user_id = u.id
            WHERE cr.culinaries_id = %s
        """, (place_id,))
    else:
        return jsonify({"error": "Invalid place type"}), 400
    
    reviews = cursor.fetchall()
    cursor.close()
    conn.close()
    
    review_list = []
    for review in reviews:
        review_list.append({
            "review_id": review[0],
            "username": review[1],   # Show username instead of user_id
            "rating": review[2],
            "reviews": review[3],
            "sentiment": review[4]
        })
    
    return jsonify(review_list)

@app.route('/expenses', methods=['POST'])
def add_expense():
    data = request.get_json()
    user_id = data['user_id']
    category = data['category']
    amount = data['amount']
    description = data.get('description', '')  # Optional

    # Step 1: Check if the user_id exists in the users table
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))
    user = cursor.fetchone()
    
    if not user:
        cursor.close()
        conn.close()
        return jsonify({"error": "User does not exist"}), 400

    # Step 2: Insert the expense into the expenses table
    expense_id = str(uuid.uuid4())
    created_at = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    updated_at = created_at  # Use the same timestamp for both created_at and updated_at

    cursor.execute("""
        INSERT INTO expenses (expense_id, user_id, category, amount, description, created_at, updated_at)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """, (expense_id, user_id, category, amount, description, created_at, updated_at))
    
    conn.commit()
    cursor.close()
    conn.close()

    return jsonify({"message": "Expense added successfully", "expense_id": expense_id}), 201

# GET /expenses/<user_id> (Get All Expenses for a User)
@app.route('/expenses/<user_id>', methods=['GET'])
def get_expenses(user_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM expenses WHERE user_id = %s", (user_id,))
    
    expenses = cursor.fetchall()
    cursor.close()
    conn.close()

    expense_list = []
    for expense in expenses:
        expense_list.append({
            "expense_id": expense[0],
            "category": expense[2],
            "amount": expense[4],
            "description": expense[5],
            "created_at": expense[6],
            "updated_at": expense[7]  # Add updated_at field to the response
        })

    return jsonify(expense_list)

# GET /expenses/total/<user_id> (Get Total Expenses by Category)
@app.route('/expenses/total/<user_id>', methods=['GET'])
def get_expenses_total(user_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT category, SUM(amount) as total_amount
        FROM expenses
        WHERE user_id = %s
        GROUP BY category
    """, (user_id,))
    
    totals = cursor.fetchall()
    cursor.close()
    conn.close()

    total_expenses = []
    for total in totals:
        total_expenses.append({
            "category": total[0],
            "total_amount": total[1]
        })

    return jsonify(total_expenses)

@app.route('/expenses/<expense_id>', methods=['PUT'])
def update_expense(expense_id):
    data = request.get_json()
    category = data.get('category', None)  # Default to None if not provided
    amount = data.get('amount', None)
    description = data.get('description', None)

    # Step 1: Check if the expense_id exists in the expenses table
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM expenses WHERE expense_id = %s", (expense_id,))
    expense = cursor.fetchone()

    if not expense:
        cursor.close()
        conn.close()
        return jsonify({"error": "Expense not found"}), 404

    # Step 2: Update the expense in the expenses table
    updated_at = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    if category is not None:
        cursor.execute("UPDATE expenses SET category = %s, updated_at = %s WHERE expense_id = %s", (category, updated_at, expense_id))
    if amount is not None:
        cursor.execute("UPDATE expenses SET amount = %s, updated_at = %s WHERE expense_id = %s", (amount, updated_at, expense_id))
    if description is not None:
        cursor.execute("UPDATE expenses SET description = %s, updated_at = %s WHERE expense_id = %s", (description, updated_at, expense_id))

    conn.commit()
    cursor.close()
    conn.close()

    return jsonify({"message": "Expense updated successfully"})

# DELETE /expenses/<expense_id> (Delete an Expense)
@app.route('/expenses/<expense_id>', methods=['DELETE'])
def delete_expense(expense_id):
    # Step 1: Check if the expense_id exists in the expenses table
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM expenses WHERE expense_id = %s", (expense_id,))
    expense = cursor.fetchone()

    if not expense:
        cursor.close()
        conn.close()
        return jsonify({"error": "Expense not found"}), 404

    # Step 2: Delete the expense from the expenses table
    cursor.execute("DELETE FROM expenses WHERE expense_id = %s", (expense_id,))
    conn.commit()
    cursor.close()
    conn.close()

    return jsonify({"message": "Expense deleted successfully"})

if __name__ == '__main__':
    app.run(host=os.getenv('SERVER_HOST'), port=os.getenv('SERVER_PORT'), debug=True)