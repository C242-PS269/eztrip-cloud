import mysql.connector
import datetime
import random
import string
import re
import os

from flask import Flask, request, jsonify
from flask_mail import Mail, Message
from config.config import Config
from dotenv import load_dotenv

# Load configurations
load_dotenv()

app = Flask(__name__)

# Load configurations
app.config.from_object(Config)

# # Flask-Mail configuration
# app.config['MAIL_SERVER'] = 'smtp.gmail.com'
# app.config['MAIL_PORT'] = 465
# app.config['MAIL_USERNAME'] = 'your-email@gmail.com'
# app.config['MAIL_PASSWORD'] = 'your-email-password'
# app.config['MAIL_USE_TLS'] = False
# app.config['MAIL_USE_SSL'] = True

mail = Mail(app)

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

    # Validate the input
    if not username or not password:
        return jsonify({'message': 'Username and password are required'}), 400

    # Query the database for the user
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
    user = cursor.fetchone()

    # If user not found
    if not user:
        return jsonify({'message': 'User not found'}), 404

    stored_password = user[3]  # Assuming password is stored in the 4th column (index 3)

    # Compare the plain text password directly with the stored password
    if password != stored_password:
        return jsonify({'message': 'Incorrect password'}), 401

    conn.close()
    return jsonify({'message': 'Login successful', 'username': username}), 200

# # API endpoint for forgot password
# @app.route('/forgot-password', methods=['POST'])
# def forgot_password():
#     data = request.get_json()

#     email = data.get('email')

#     # Validate email
#     if not email:
#         return jsonify({'error': 'Email is required.'}), 400

#     # Find user by email
#     conn = get_db_connection()
#     cursor = conn.cursor()
#     cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
#     user = cursor.fetchone()
#     conn.close()

#     if not user:
#         return jsonify({'error': 'Email not found.'}), 404

#     # Generate random password reset code
#     reset_code = ''.join(random.choices(string.ascii_letters + string.digits, k=6))

#     # Store the reset code and its expiration in the database
#     conn = get_db_connection()
#     cursor = conn.cursor()
#     expiration_time = datetime.datetime.now() + datetime.timedelta(hours=1)  # Set expiration time (1 hour)
#     cursor.execute(
#         "INSERT INTO password_resets (email, reset_code, expiration_time) VALUES (%s, %s, %s)",
#         (email, reset_code, expiration_time)
#     )
#     conn.commit()
#     conn.close()

#     # Send reset code via email
#     msg = Message('Password Reset Code', sender='your-email@gmail.com', recipients=[email])
#     msg.body = f'Your password reset code is: {reset_code}. It will expire in 1 hour.'
#     try:
#         mail.send(msg)
#         return jsonify({'message': f'Password reset code sent to {email}.'}), 200
#     except Exception as e:
#         return jsonify({'error': f'Failed to send email: {str(e)}'}), 500

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

if __name__ == '__main__':
    app.run(host=os.getenv('SERVER_HOST'), port=os.getenv('SERVER_PORT'), debug=True)