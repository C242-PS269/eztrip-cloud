# Data Server & API Services Documentation

### Overview

<p align=justify>
This documentation provides a guide to the available API endpoints for user account management and data operations. It details the requests, parameters, and example usage for each endpoint. The APIs are designed to handle user registration, login, profile updates, and account deletion.
</p>

### Important Notes

The APIs URL in documentation its still in local development ```http://localhost:5000/```, if the backend is already deployed, then the mobile development team just need to change the domain name that will be provided by cloud computing team.

### API Endpoint: ```/register```

Overview:

The ```/register``` endpoint allows a new user to create an account by providing necessary details such as username, email, password, and phone number.

Base URL:
```bash
http://localhost:5000/register
```

Method: ```POST```

Example Body Request:
```json
{
  "username": "john_doe",
  "email": "john@example.com",
  "password": "password123",
  "confirm_password": "password123",
  "phone_number": "1234567890"
}
```

cURL:
```bash
curl -X POST http://localhost:5000/register -H "Content-Type: application/json" -d "{\"username\":\"john_doe\",\"email\":\"john@example.com\",\"password\":\"password123\",\"confirm_password\":\"password123\",\"phone_number\":\"1234567890\"}"
```

### API Endpoint: ```/login```

Overview:

The ```/login``` endpoint authenticates a user based on their username and password.

Base URL:
```bash
http://localhost:5000/login
```

Method: ```POST```

Example Body Request:
```json
{
  "username": "john_doe",
  "password": "password123"
}
```

cURL:
```bash
curl -X POST http://localhost:5000/login -H "Content-Type: application/json" -d "{\"username\":\"john_doe\",\"password\":\"password123\"}"
```

### API Endpoint: ```/update```

Overview:

The ```/update``` endpoint allows a user to update their profile information, such as changing their password or phone number.

Base URL:
```bash
http://localhost:5000/update
```

Method: ```/update```

Example Body Request:
```json
{
  "username": "john_doe",
  "current_password": "password123",
  "new_password": "newpassword456",
  "new_phone": "9876543210"
}
```

cURL:
```bash
curl -X PUT http://localhost:5000/update -H "Content-Type: application/json" -d "{\"username\":\"john_doe\",\"current_password\":\"password123\",\"new_password\":\"newpassword456\",\"new_phone\":\"9876543210\"}"
```

### API Endpoint: ```/delete```

Overview:

The ```/delete``` endpoint allows a user to delete their account by providing their username and password for authentication.

Base URL:
```bash
http://localhost:5000/delete
```

Method: ```DELETE```

Example Body Request:
```json
{
  "username": "john_doe",
  "password": "newpassword456"
}
```

cURL:
```bash
curl -X DELETE http://localhost:5000/delete -H "Content-Type: application/json" -d "{\"username\":\"john_doe\",\"password\":\"newpassword456\"}"
```

### API Endpoint: ```/itineraries```

Overview:

The ```/itineraries``` endpoint is used to generate a personalized itinerary based on the user’s budget and preferred city. The system uses external services to generate a list of accommodation, culinary spots, and tours for the user. It then calculates the total cost and the remaining budget, and saves this information to the database.

Base URL:
```bash
http://localhost:5000/itineraries
```

Method: ```POST```

Example Body Request:
```json
{
  "user_id": "3L11NyTgVoOK6sVp5WyrNKPmUqISRQAHsoMl",
  "budget": 2200000,
  "city": "Denpasar"
}
```

cURL:
```bash
curl -X POST http://localhost:5000/itineraries -H "Content-Type: application/json" -d "{\"user_id\": \"3L11NyTgVoOK6sVp5WyrNKPmUqISRQAHsoMl\", \"budget\": 2200000, \"city\": \"Denpasar\"}"
```

Response:
```json
{
  "message": "Itinerary saved successfully",
  "itinerary": {
    "accommodation": {
      "city": "Denpasar",
      "name": "Mars City Hotel",
      "price": 592200.0
    },
    "culinary_1": {
      "city": "Denpasar",
      "name": "Three Monkeys Sanur",
      "price": 300000.0
    },
    "culinary_2": {
      "city": "Denpasar",
      "name": "Three Monkeys Sanur",
      "price": 300000.0
    },
    "culinary_3": {
      "city": "Denpasar",
      "name": "Naughty Nuri's Sanur",
      "price": 300000.0
    },
    "culinary_4": {
      "city": "Denpasar",
      "name": "Warung Baby Monkeys",
      "price": 100000.0
    },
    "culinary_5": {
      "city": "Denpasar",
      "name": "Warung Amphibia Seafood",
      "price": 100000.0
    },
    "culinary_6": {
      "city": "Denpasar",
      "name": "Warung Makan SMS",
      "price": 100000.0
    },
    "tour_1": {
      "city": "Denpasar",
      "name": "Upside Down World Bali",
      "price": 150000.0
    },
    "tour_2": {
      "city": "Denpasar",
      "name": "Upside Down World Bali",
      "price": 150000.0
    },
    "tour_3": {
      "city": "Denpasar",
      "name": "Big Garden Corner",
      "price": 50000.0
    },
    "tour_4": {
      "city": "Denpasar",
      "name": "Barong Tanah Kilap - Sari Wisata Budaya BALI",
      "price": 15000.0
    },
    "tour_5": {
      "city": "Denpasar",
      "name": "Bali Festival Park, Padang Galak",
      "price": 10000.0
    },
    "tour_6": {
      "city": "Denpasar",
      "name": "Bali Museum",
      "price": 5000.0
    },
    "tour_7": {
      "city": "Denpasar",
      "name": "Munduk Tutub Waterfall",
      "price": 20000.0
    },
    "tour_free_15": {
      "city": "Denpasar",
      "name": "Daerah tujuan wisata tukad bindu",
      "price": 0.0
    },
    "tour_free_25": {
      "city": "Denpasar",
      "name": "Werdhi Budaya Art Centre",
      "price": 0.0
    },
    "tour_free_40": {
      "city": "Denpasar",
      "name": "Biaung Beach",
      "price": 0.0
    }
  },
  "remaining_budget": 7800.0,
  "total_cost": 2192200.0
}
```