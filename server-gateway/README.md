# Gateway Server & API Services Documentation

## Overview
<p align="justify">
The Gateway Server acts as an intermediary between the client (mobile app, frontend, etc.) and various backend services (e.g., user management, expenses, reviews). It forwards requests to the respective backend services, consolidating responses and handling errors.
</p>

Backend URLs during development:

User Data Service: ```http://localhost:5000```

Model Service: ```http://localhost:4000```

## Important Notes

The APIs URL in documentation its still in local development ```http://localhost:3000/```, if the backend is already deployed, then the mobile development team just need to change the domain name that will be provided by cloud computing team.

## User Account Management APIs Endpoint

### API Endpoint: ```/api/data/user/account/register```

Method: ```POST```

Example Body Request:
```json
{
  "username": "admin",
  "email": "admin@eztrip.com",
  "password": "admin123",
  "confirm_password": "admin123",
  "phone_number": "1234567890"
}
```

cURL:
```bash
curl -X POST http://localhost:3000/api/data/user/account/register -H "Content-Type: application/json" -d "{\"username\": \"admin\", \"email\": \"admin@eztrip.com\", \"password\": \"admin123\", \"confirm_password\": \"admin123\", \"phone_number\": \"1234567890\"}"
```

Response (Success):
```json
{
  "message": "User registered successfully!"
}
```

### API Endpoint: ```/api/data/user/account/login```

Method: ```POST```

Example Body Request:
```json
{
  "username": "admin",
  "password": "admin123"
}
```

cURL:
```bash
curl -X POST http://localhost:3000/api/data/user/account/login -H "Content-Type: application/json" -d "{\"username\": \"admin\", \"password\": \"admin123\"}" 
```

Response:
```json
{
  "message": "Login successful",
  "user_id": "xODpZq4mFEaTG6eGzy1dc7nk30iyD3fHrDmT"
}
```

### API Endpoint: ```/api/data/user/account/update```

Method: ```PUT```

Example Body Request:
```json
{
  "username": "admin",
  "current_password": "admin123",
  "new_password": "newpassword123", (optional)
  "new_email": "admin@eztrip-example.com", (optional)
  "new_phone": 88839924232, (optional)
}
```

cURL:
```bash
curl -X PUT http://localhost:3000/api/data/user/account/update -H "Content-Type: application/json" -d "{\"username\": \"admin\", \"current_password\": \"admin123\", \"new_password\": \"newpassword123\"}"
```

Response (Success):
```json
{
  "message": "User information updated successfully."
}
```

### API Endpoint: ```/api/data/user/account/delete```

Method: ```DELETE```

Example Body Request:
```json
{
  "username": "admin",
  "password": "newpassword123"
}
```

cURL:
```bash
curl -X DELETE http://localhost:3000/api/data/user/account/delete -H "Content-Type: application/json" -d "{\"username\":\"admin\",\"password\":\"newpassword123\"}"
```

Response (Success):
```json
{
  "message": "User account and all related data deleted successfully. Thankyou for using EzTrip!, Sorry we have to see you go :("
}
```

## Features API Endpoints

### API Endpoint: ```/api/data/features/itineraries```

Method: ```POST```

Example Body Request:
```json
{   
    user_id: "xODpZq4mFEaTG6eGzy1dc7nk30iyD3fHrDmT",
    budget: 1000000,
    city: "Badung" (optional)
}
```

cURL:

- Based On ```budget``` + ```city```:
```bash
curl -X POST http://localhost:3000/api/data/features/itineraries -H "Content-Type: application/json" -d "{\"user_id\": \"xODpZq4mFEaTG6eGzy1dc7nk30iyD3fHrDmT\", \"budget\": 1000000, \"city\": \"Badung\"}"
```

- Based On ```budget``` Only:
```bash
curl -X POST http://localhost:3000/api/data/features/itineraries -H "Content-Type: application/json" -d "{\"user_id\": \"xODpZq4mFEaTG6eGzy1dc7nk30iyD3fHrDmT\", \"budget\": 1000000}"
```

Response (Success):
```json
{
  "itinerary": {
    "accommodation": {
      "city": "Badung",
      "name": "The Legian 777",
      "price": 194793.0
    },
    "culinary_1": {
      "city": "Badung",
      "name": "Sang Ria Grill Bali",
      "price": 300000.0
    },
    "culinary_2": {
      "city": "Badung",
      "name": "Sang Ria Grill Bali",
      "price": 300000.0
    },
    "culinary_3": {
      "city": "Badung",
      "name": "The Luhron",
      "price": 100000.0
    },
    "remaining_budget": 1785.4200000000274,
    "total_cost": 998214.58,
    "tour_1": {
      "city": "Badung",
      "name": "ART WOOD NIKINI",
      "price": 34473.86
    },
    "tour_2": {
      "city": "Badung",
      "name": "ART WOOD NIKINI",
      "price": 34473.86
    },
    "tour_3": {
      "city": "Badung",
      "name": "Nunggalan Beach",
      "price": 34473.86
    },
    "tour_free_36": {
      "city": "Badung",
      "name": "Nelayan Beach",
      "price": 0.0
    },
    "tour_free_39": {
      "city": "Badung",
      "name": "Pantai Nusa Dua",
      "price": 0.0
    },
    "tour_free_9": {
      "city": "Badung",
      "name": "Pantai Batu Belig",
      "price": 0.0
    }
  },
  "message": "Itinerary saved successfully",
  "remaining_budget": 1785.420000000042,
  "total_cost": 998214.58
}
```

### API Endpoint: ```/api/data/features/itineraries/user/<user_id>```

Method: ```GET```

cURL
```bash
curl -X GET http://localhost:3000/api/data/features/itineraries/user/<user_id>
```

Example cURL:
```bash
curl -X GET http://localhost:3000/api/data/features/itineraries/user/xODpZq4mFEaTG6eGzy1dc7nk30iyD3fHrDmT
```

Response (Success):
```json
{
  "itineraries": [
    {
      "budget": "1000000.00",
      "created_at": "2024-12-07 18:40:00",
      "id": "3f42a662-2b23-48f9-86d8-a60b34f7f8ed",
      "itinerary_data": {
        "itinerary": {
          "accommodation": {
            "city": "Badung",
            "name": "The Legian 777",
            "price": 194793.0
          },
          "culinary_1": {
            "city": "Badung",
            "name": "Sang Ria Grill Bali",
            "price": 300000.0
          },
          "culinary_2": {
            "city": "Badung",
            "name": "Sang Ria Grill Bali",
            "price": 300000.0
          },
          "culinary_3": {
            "city": "Badung",
            "name": "The Luhron",
            "price": 100000.0
          },
          "remaining_budget": 1785.4200000000274,
          "total_cost": 998214.58,
          "tour_1": {
            "city": "Badung",
            "name": "ART WOOD NIKINI",
            "price": 34473.86
          },
          "tour_2": {
            "city": "Badung",
            "name": "ART WOOD NIKINI",
            "price": 34473.86
          },
          "tour_3": {
            "city": "Badung",
            "name": "Nunggalan Beach",
            "price": 34473.86
          },
          "tour_free_36": {
            "city": "Badung",
            "name": "Nelayan Beach",
            "price": 0.0
          },
          "tour_free_39": {
            "city": "Badung",
            "name": "Pantai Nusa Dua",
            "price": 0.0
          },
          "tour_free_9": {
            "city": "Badung",
            "name": "Pantai Batu Belig",
            "price": 0.0
          }
        }
      },
      "remaining_budget": "1785.42",
      "total_cost": "998214.58"
    },
    {
      "budget": "1000000.00",
      "created_at": "2024-12-07 00:06:30",
      "id": "d53f609e-d164-4a7e-b9da-2740196a1d15",
      "itinerary_data": {
        "itinerary": {
          "accommodation": {
            "city": "Badung",
            "name": "The Legian 777",
            "price": 194793.0
          },
          "culinary_1": {
            "city": "Badung",
            "name": "Sang Ria Grill Bali",
            "price": 300000.0
          },
          "culinary_2": {
            "city": "Badung",
            "name": "Sang Ria Grill Bali",
            "price": 300000.0
          },
          "culinary_3": {
            "city": "Badung",
            "name": "The Luhron",
            "price": 100000.0
          },
          "remaining_budget": 1785.4200000000274,
          "total_cost": 998214.58,
          "tour_1": {
            "city": "Badung",
            "name": "ART WOOD NIKINI",
            "price": 34473.86
          },
          "tour_2": {
            "city": "Badung",
            "name": "ART WOOD NIKINI",
            "price": 34473.86
          },
          "tour_3": {
            "city": "Badung",
            "name": "Nunggalan Beach",
            "price": 34473.86
          },
          "tour_free_36": {
            "city": "Badung",
            "name": "Nelayan Beach",
            "price": 0.0
          },
          "tour_free_39": {
            "city": "Badung",
            "name": "Pantai Nusa Dua",
            "price": 0.0
          },
          "tour_free_9": {
            "city": "Badung",
            "name": "Pantai Batu Belig",
            "price": 0.0
          }
        }
      },
      "remaining_budget": "1785.42",
      "total_cost": "998214.58"
    }
  ]
}
```

### API Endpoint: ```/api/data/features/itineraries/<uuid:id>```

cURL:
```bash
curl -X DELETE http://localhost:3000/api/data/features/itineraries/40afda23-156f-41f9-b08b-4ee3b16f3a21
```

Response (Success):
```json
{
  "message": "Itinerary deleted successfully"
}
```

### API Endpoint: ```/api/data/reviews/submit```

Method: ```POST```

Example Body Request:
```json
{
  "user_id": "xODpZq4mFEaTG6eGzy1dc7nk30iyD3fHrDmT",
  "place_id": "04347b8e-772d-45af-96a4-aacaf62de41f",
  "place_type": "accommodations" (category: accommodations/tours/culinaries),
  "rating": 4,
  "reviews": "Good place!"
}
```

cURL:
```bash
curl -X POST http://localhost:3000/api/data/reviews/submit -H "Content-Type: application/json" -d "{\"user_id\": \"xODpZq4mFEaTG6eGzy1dc7nk30iyD3fHrDmT\", \"place_id\": \"04347b8e-772d-45af-96a4-aacaf62de41f\", \"place_type\": \"accommodations\", \"rating\": 4, \"reviews\": \"Good place!\"}"
```

Response (Success):
```json
{
  "message": "Review submitted successfully",
  "review_id": "56afe55e-2c85-44b6-a12f-8611a8b0c729"
}
```

### API Endpoint: ```/api/data/reviews/<place_type>/<place_id>```

Method: ```GET```

cURL:
```bash
curl -X GET http://localhost:3000/api/data/reviews/accommodations/04347b8e-772d-45af-96a4-aacaf62de41f
```

Response (Success):
```json
[
  {
    "rating": "5.00",
    "review_id": "1f3d6569-b562-4fe6-9124-26d31ba80935",
    "reviews": "Great place!",
    "sentiment": "positive",
    "username": "admin"
  },
  {
    "rating": "4.00",
    "review_id": "56afe55e-2c85-44b6-a12f-8611a8b0c729",
    "reviews": "Good place!",
    "sentiment": "positive",
    "username": "admin"
  },
  {
    "rating": "5.00",
    "review_id": "c97cf3fb-52ac-44eb-9cd8-e318360b57a7",
    "reviews": "Great place!",
    "sentiment": "positive",
    "username": "admin"
  }
]
```

### API Endpoint: ```/api/data/user/expenses```

Method: ```POST```

Example Body Request:
```json
{
  "user_id": "xODpZq4mFEaTG6eGzy1dc7nk30iyD3fHrDmT",
  "category": "drink",
  "amount": 5000,
  "description": "Drinking"
}
```

cURL:
```bash
curl -X POST http://localhost:3000/api/data/user/expenses -H "Content-Type: application/json" -d "{\"user_id\": \"xODpZq4mFEaTG6eGzy1dc7nk30iyD3fHrDmT\", \"category\": \"drink\", \"amount\": 5000, \"description\": \"Drinking\"}"
```

Response (Success):
```json
{
  "expense_id": "682b1f2e-37cd-4a06-b81f-0ea853fe4b41",
  "message": "Expense added successfully"
}
```

### API Endpoint: ```/api/data/user/expenses/<user_id>```

Method: ```GET```

cURL:
```bash
curl -X GET http://localhost:3000/api/data/user/expenses/xODpZq4mFEaTG6eGzy1dc7nk30iyD3fHrDmT
```

Response (Success):
```json
[
  {
    "amount": "50000.00",
    "category": "food",
    "created_at": "Sat, 07 Dec 2024 19:24:27 GMT",
    "description": "Dinner at restaurant",
    "expense_id": "d94c6761-d424-43f4-a0aa-5d795f7927b3",
    "updated_at": "Sat, 07 Dec 2024 19:24:27 GMT"
  }
]
```

### API Endpoint: ```/api/data/user/expenses/total/<user_id>```

Method: ```GET```

cURL:
```bash
curl -X GET http://localhost:3000/api/data/user/expenses/total/xODpZq4mFEaTG6eGzy1dc7nk30iyD3fHrDmT
```

Response (Success):
```json
[
  {
    "category": "food",
    "total_amount": "50000.00"
  }
]
```

### API Endpoint: ```/api/data/user/expenses/<expense_id>``` PUT

Method: ```PUT```
Example Body Request:
```json
{
  "category": "food" (optional), 
  "amount": 250.00 (optional),
  "description": "Wrong menu" (optional)
}
```

cURL:
```bash
curl -X PUT http://localhost:3000/api/data/user/expenses/d94c6761-d424-43f4-a0aa-5d795f7927b3 -H "Content
-Type: application/json" -d "{\"category\": \"food\", \"amount\": 250.00, \"description\": \"Wrong menu\"}"
```

Response (Success):
```json
{
  "message": "Expense updated successfully"
}
```

### API Endpoint: ```/api/data/user/expenses/<expense_id>``` DELETE

Method: ```DELETE```

Example Body Request:
```json
{
    expense_id: 30d3448a-ddda-4848-9d1d-504262206589 
}
```

cURL:
```bash
curl -X DELETE http://localhost:3000/api/data/user/expenses/682b1f2e-37cd-4a06-b81f-0ea853fe4b41
```

Response (Success):
```json
{
  "message": "Expense deleted successfully"
}
```
## Get Data Management APIs Endpoints

## API Endpoint: ```/api/data/places/<category>/all```

Method: ```GET```

cURL:

- Tours

```bash
curl -X GET http://localhost:3000/api/data/places/tours/all
```

- Accommodations

```bash
curl -X GET http://localhost:3000/api/data/places/accommodations/all
```

- Culinaries:

```bash
curl -X GET http://localhost:3000/api/data/places/culinaries/all
```

Response (Success) - Retrive All Data From Tables:
```json
{
  "items": [
    {
      "address": "Jalan Raya Pasut",
      "category": "Beach",
      "city": "Tabanan",
      "google_maps": "https://www.google.com/maps/place/Pantai+Pasut/data=!4m7!3m6!1s0x2dd23122e42d049b:0xb8644744b2f08ac3!8m2!3d-8.563438!4d115.0367423!16s%2Fg%2F11cmsv_ydb!19sChIJmwQt5CIx0i0Rw4rwskRHZLg?authuser=0&hl=en&rclk=1",
      "id": "001b583e-ef93-4f10-8139-025dd37b97e0",
      "name": "Pantai Pasut",
      "price_wna": 15000.0,
      "rating": 4.5
    },
    {
      "address": "Jl. Kaliasem lingk.kelod kangin",
      "category": "Tourist attraction",
      "city": "Gianyar",
      "google_maps": "https://www.google.com/maps/place/Kanto+Lampo+Waterfall/data=!4m7!3m6!1s0x2dd217ff9adc01a1:0xea08b2e84ad7ab23!8m2!3d-8.5321802!4d115.3312408!16s%2Fg%2F11lrkjx_fc!19sChIJoQHcmv8X0i0RI6vXSuiyCOo?authuser=0&hl=en&rclk=1",
      "id": "00cacf23-0b33-49fa-8778-08735cd5a12e",
      "name": "Kanto Lampo Waterfall",
      "price_wna": 15000.0,
      "rating": 4.4
    },
    ...
  ]
}
```

## API Endpoint: ```/api/data/places/<category>/random```

Method: ```GET```

cURL:

- Tours

```bash
curl -X GET http://localhost:3000/api/data/places/tours/random
```

- Accommodations

```bash
curl -X GET http://localhost:3000/api/data/places/accommodations/random
```

- Culinaries:

```bash
curl -X GET http://localhost:3000/api/data/places/culinaries/random
```

Response (Success) - Retrive All Data From Tables, Randomly (LIMIT 10):
```json
{
  "items": [
    {
      "address": "Jalan Raya Pasut",
      "category": "Beach",
      "city": "Tabanan",
      "google_maps": "https://www.google.com/maps/place/Pantai+Pasut/data=!4m7!3m6!1s0x2dd23122e42d049b:0xb8644744b2f08ac3!8m2!3d-8.563438!4d115.0367423!16s%2Fg%2F11cmsv_ydb!19sChIJmwQt5CIx0i0Rw4rwskRHZLg?authuser=0&hl=en&rclk=1",
      "id": "001b583e-ef93-4f10-8139-025dd37b97e0",
      "name": "Pantai Pasut",
      "price_wna": 15000.0,
      "rating": 4.5
    },
    {
      "address": "Jl. Kaliasem lingk.kelod kangin",
      "category": "Tourist attraction",
      "city": "Gianyar",
      "google_maps": "https://www.google.com/maps/place/Kanto+Lampo+Waterfall/data=!4m7!3m6!1s0x2dd217ff9adc01a1:0xea08b2e84ad7ab23!8m2!3d-8.5321802!4d115.3312408!16s%2Fg%2F11lrkjx_fc!19sChIJoQHcmv8X0i0RI6vXSuiyCOo?authuser=0&hl=en&rclk=1",
      "id": "00cacf23-0b33-49fa-8778-08735cd5a12e",
      "name": "Kanto Lampo Waterfall",
      "price_wna": 15000.0,
      "rating": 4.4
    },
    ...
  ]
}
```

## API Endpoint: ```/api/data/places/detail/<category>/<uuid:id>```

Method: ```GET```

- Tours
```bash
curl -X GET http://localhost:3000/api/data/places/detail/tours/id
```

- Accommodations
```bash
curl -X GET http://localhost:3000/api/data/places/detail/accommodations/id
```

- Culinaries
```bash
curl -X GET http://localhost:3000/api/data/places/detail/culinaries/id
```

Response (Success):

```json
{
  "place_detail": {
    "address": "Jl. Kaliasem lingk.kelod kangin",
    "category": "Tourist attraction",
    "city": "Gianyar",
    "google_maps": "https://www.google.com/maps/place/Kanto+Lampo+Waterfall/data=!4m7!3m6!1s0x2dd217ff9adc01a1:0xea08b2e84ad7ab23!8m2!3d-8.5321802!4d115.3312408!16s%2Fg%2F11lrkjx_fc!19sChIJoQHcmv8X0i0RI6vXSuiyCOo?authuser=0&hl=en&rclk=1",
    "id": "00cacf23-0b33-49fa-8778-08735cd5a12e",
    "name": "Kanto Lampo Waterfall",
    "price_wna": 15000.0,
    "rating": 4.4
  }
}
```

## Model APIs Endpoint

### API Endpoint: ```/api/model/recommendations/tours```

Method: ```POST```

Example Body Request:
```json
{
    "max_price": 100000,
    "min_rating": 4,
    "category": "Beach",
    "city": "Denpasar"
}
```

cURL:
```bash
curl -X POST http://localhost:3000/api/model/recommendations/tours -H "Content-Type: application/json" -d "{\"max_price\": 100000, \"min_rating\": 4, \"category\": \"Beach\", \"city\": \"Denpasar\"}"
```

Response (Success):
```json
{
  "tours": [
    {
      "category": "Beach",
      "city": "Denpasar",
      "google_maps": "https://www.google.com/maps/place/Karang+Beach/data=!4m7!3m6!1s0x2dd214573b2294d5:0x33316987ae56a9ce!8m2!3d-8.693729!4d115.266016!16s%2Fg%2F11f5dft94s!19sChIJ1ZQiO1cU0i0RzqlWrodpMTM?authuser=0&hl=en&rclk=1",
      "name": "Karang Beach",
      "price_wna": 34473.86,
      "rating": 4.6
    },
    {
      "category": "Beach",
      "city": "Denpasar",
      "google_maps": "https://www.google.com/maps/place/Srilanka+Beach/data=!4m7!3m6!1s0x2dd2431916164c67:0x9a06b9d3762c3eb2!8m2!3d-8.7874067!4d115.2288724!16s%2Fg%2F11d_yt0ygw!19sChIJZ0wWFhlD0i0Rsj4sdtO5Bpo?authuser=0&hl=en&rclk=1",
      "name": "Srilanka Beach",
      "price_wna": 34473.86,
      "rating": 4.6
    },
    {
      "category": "Beach",
      "city": "Denpasar",
      "google_maps": "https://www.google.com/maps/place/Pantai+Segara+Ayu/data=!4m7!3m6!1s0x2dd2403423ab0659:0xaf4e05330cf34456!8m2!3d-8.6824631!4d115.2643001!16s%2Fg%2F11cjj09j0w!19sChIJWQarIzRA0i0RVkTzDDMFTq8?authuser=0&hl=en&rclk=1",
      "name": "Pantai Segara Ayu",
      "price_wna": 0.0,
      "rating": 4.5
    },
    {
      "category": "Beach",
      "city": "Denpasar",
      "google_maps": "https://www.google.com/maps/place/Mertasari+Beach/data=!4m7!3m6!1s0x2dd24196daee874b:0x7baf80e112bad8ca!8m2!3d-8.7125026!4d115.2517831!16s%2Fg%2F1q62g5t4r!19sChIJS4fu2pZB0i0Ryti6EuGAr3s?authuser=0&hl=en&rclk=1",
      "name": "Mertasari Beach",
      "price_wna": 34473.86,
      "rating": 4.4
    },
    {
      "category": "Beach",
      "city": "Denpasar",
      "google_maps": "https://www.google.com/maps/place/Sanur+Beach/data=!4m7!3m6!1s0x2dd2403905cb5bb3:0x71c81e3c44b1b241!8m2!3d-8.6746703!4d115.2640329!16s%2Fg%2F1q5ccc3nd!19sChIJs1vLBTlA0i0RQbKxRDweyHE?authuser=0&hl=en&rclk=1",
      "name": "Sanur Beach",
      "price_wna": 0.0,
      "rating": 4.4
    }
  ]
}
```

### API Endpoint: ```/api/model/recommendations/tours/visited```

Example Body Request:
```json
{
    "tour_name": "Balangan Beach",
    "city_filter": "Badung" (Optinal),
    "max_price": 100000 (Optional)
}
```

cURL:
```bash
curl -X POST http://localhost:3000/api/model/recommendations/tours/visited -H "Content-Type: application/json" -d "{\"tour_name\":\"Balangan Beach\", \"city_filter\":\"Badung\", \"max_price\":100000}"
```

Response (Success):
```json
{
  "tours": [
    {
      "address": "Jl. Batu Belig",
      "category": "Beach",
      "city": "Badung",
      "google_maps": "https://www.google.com/maps/place/Pantai+Batu+Belig/data=!4m7!3m6!1s0x2dd24774c0a631b1:0x9d16e84a9b99cabd!8m2!3d-8.6742449!4d115.1459553!16s%2Fg%2F11byfljfj1!19sChIJsTGmwHRH0i0RvcqZm0roFp0?authuser=0&hl=en&rclk=1",
      "name": "Pantai Batu Belig",
      "price_wna": 0.0,
      "rating": 4.5
    },
    {
      "address": "Jl. Nelayan No.31",
      "category": "Beach",
      "city": "Badung",
      "google_maps": "https://www.google.com/maps/place/Nelayan+Beach/data=!4m7!3m6!1s0x2dd2478440974ee7:0x6bba90d306ec0b42!8m2!3d-8.6618096!4d115.132987!16s%2Fg%2F11bymxb52q!19sChIJ506XQIRH0i0RQgvsBtOQums?authuser=0&hl=en&rclk=1",
      "name": "Nelayan Beach",
      "price_wna": 0.0,
      "rating": 4.5
    },
    {
      "address": "Nusa Dua",
      "category": "Beach",
      "city": "Badung",
      "google_maps": "https://www.google.com/maps/place/Pantai+Nusa+Dua/data=!4m7!3m6!1s0x2dd2432985d2b7d9:0x5e21cb0eb654ba09!8m2!3d-8.8051695!4d115.2339136!16s%2Fg%2F11bwflbrl4!19sChIJ2bfShSlD0i0RCbpUtg7LIV4?authuser=0&hl=en&rclk=1",
      "name": "Pantai Nusa Dua",
      "price_wna": 0.0,
      "rating": 4.5
    },
    {
      "address": "",
      "category": "Beach",
      "city": "Badung",
      "google_maps": "https://www.google.com/maps/place/Kuta+Beach/data=!4m7!3m6!1s0x2dd246bc2ab70d43:0x82feaae12f4ab48e!8m2!3d-8.7184926!4d115.1686322!16s%2Fg%2F11c1p6r11n!19sChIJQw23KrxG0i0RjrRKL-Gq_oI?authuser=0&hl=en&rclk=1",
      "name": "Kuta Beach",
      "price_wna": 0.0,
      "rating": 4.5
    },
    {
      "address": "",
      "category": "Beach",
      "city": "Badung",
      "google_maps": "https://www.google.com/maps/place/Pantai+Samuh/data=!4m7!3m6!1s0x2dd243213c648795:0x6c4c8c1ba601a2b1!8m2!3d-8.7871671!4d115.2284909!16s%2Fg%2F11ckwbjgd5!19sChIJlYdkPCFD0i0RsaIBphuMTGw?authuser=0&hl=en&rclk=1",
      "name": "Pantai Samuh",
      "price_wna": 0.0,
      "rating": 4.5
    }
  ]
}
```

### API Endpoint: ```/api/model/recommendations/accommodations```

Example Body Request:
```json
{
    "city": "Denpasar",
    "min_rating": 4 (optional),
    "max_price": 2000000 (optional)
}
```

cURL:
```bash
curl -X POST http://localhost:3000/api/model/recommendations/accommodations -H "Content-Type: application/json" -d "{\"city\": \"Denpasar\", \"min_rating\": 4, \"max_price\": 2000000}"
```

Response (Success):
```json
{
  "accomodations": [
    {
      "city": "Denpasar",
      "name": "Villa Bebek Cottages Sanur",
      "price_wna": 1019999.9999999999,
      "rating": 4.7
    },
    {
      "city": "Denpasar",
      "name": "Arena Living",
      "price_wna": 1260000.0,
      "rating": 4.45
    },
    {
      "city": "Denpasar",
      "name": "Jukung Guest House",
      "price_wna": 450000.0,
      "rating": 4.45
    },
    {
      "city": "Denpasar",
      "name": "The Alantara Sanur",
      "price_wna": 1362060.0,
      "rating": 4.4
    },
    {
      "city": "Denpasar",
      "name": "Artotel Sanur - Bali",
      "price_wna": 1182600.0,
      "rating": 4.4
    }
  ]
}
```

### API Endpoint: ```/api/model/recommendations/accommodations/visited```

Example Body Request:
```json
{
    "accommodation_name": "The Seiryu Boutique Villas",
    "city_filter": "Badung" (optional),
    "max_price": 500000 (optional)
}
```

cURL:
```bash
curl -X POST http://localhost:3000/api/model/recommendations/accommodations/visited -H "Content-Type: application/json" -d "{\"accommodation_name\":\"The Seiryu Boutique Villas\", \"city_filter\":\"Badung\", \"max_price\":500000}"
```

Request (Success):
```json
{
  "accomodations": [
    {
      "city": "Badung",
      "name": "Cara Cara Inn",
      "price_wna": 390600.0,
      "rating": 4.4
    },
    {
      "city": "Badung",
      "name": "Interconnection Kuta",
      "price_wna": 417999.99999999994,
      "rating": 4.45
    },
    {
      "city": "Badung",
      "name": "Legian Bisma Suite",
      "price_wna": 407333.0,
      "rating": 4.35
    },
    {
      "city": "Badung",
      "name": "Royal Regantris Kuta",
      "price_wna": 465483.0,
      "rating": 4.3
    },
    {
      "city": "Badung",
      "name": "SEAHOUSE BALI INDAH BEACH INN",
      "price_wna": 450000.0,
      "rating": 4.5
    }
  ]
}
```

### API Endpoint: ```/api/model/recommendations/culinaries```

Example Body Request:
```json
{
    "max_price": 1000000,
    "min_rating": 4.0,
    "category": "Bar",
    "city": "Denpasar"
}
```

cURL:
```bash
curl -X POST http://localhost:3000/api/model/recommendations/culinaries -H "Content-Type: application/json" -d "{\"category\": \"Bar\", \"city\": \"Denpasar\", \"min_rating\": 4.0, \"max_price\": 1000000}"
```

Response (Success):
```json
{
  "culinaries": [
    {
      "address": "Jl. Segara Ayu, Sanur, Denpasar 80228 Indonesia",
      "category": "Bar",
      "city": "Denpasar",
      "name": "Byrd House Bali",
      "price_wna": 300000.0,
      "rating": 4.0
    },
    {
      "address": "Jl. Danau Tamblingan 120, Sanur, Denpasar 80223 Indonesia",
      "category": "Bar",
      "city": "Denpasar",
      "name": "Casablanca Dine Drink Dance",
      "price_wna": 300000.0,
      "rating": 4.5
    },
    {
      "address": "Jl. Pantai Sindhu No.11, Sanur, Denpasar 80228 Indonesia",
      "category": "Bar",
      "city": "Denpasar",
      "name": "Shotgun Social Bali",
      "price_wna": 300000.0,
      "rating": 4.5
    },
    {
      "address": "Jalan Duyung Jalan Sanur Beach Street Walk, Sanur, Denpasar 80228 Indonesia",
      "category": "Bar",
      "city": "Denpasar",
      "name": "Lilla Pantai",
      "price_wna": 300000.0,
      "rating": 4.5
    },
    {
      "address": "Jalan Kusuma Sari No. 8, Sanur, Denpasar 80227 Indonesia",
      "category": "Bar",
      "city": "Denpasar",
      "name": "Pier Eight Bali",
      "price_wna": 300000.0,
      "rating": 4.5
    }
  ]
}
```

### API Endpoint: ```/api/model/recommendations/culinaries/visited```

Example Body Request:
```json
{
    "culinary_name": "Koral Restaurant",
    "city_filter": "Badung" (optional),
    "max_price": 500000 (optional)
}
```

cURL:
```bash
curl -X POST http://localhost:3000/api/model/recommendations/culinaries/visited -H "Content-Type: application/json" -d "{\"culinary_name\":\"Koral Restaurant\", \"city_filter\":\"Badung\", \"max_price\":500000}"
```

Response (Success):
```json
{
  "culinaries": [
    {
      "address": "Kawasan Pariwisata Nusa Dua Lot S6, Nusa Dua, Benoa 80363 Indonesia",
      "category": "International",
      "city": "Badung",
      "name": "Boneka Restaurant at The St. Regis Bali Resort",
      "price_wna": 499999.99999999994,
      "rating": 5.0
    },
    {
      "address": "Jl. Petitenget W Bali - Seminyak, Kerobokan 80361 Indonesia",
      "category": "International",
      "city": "Badung",
      "name": "Fire",
      "price_wna": 499999.99999999994,
      "rating": 5.0
    },
    {
      "address": "Jl Yoga Perkanthi, Jimbaran 80364 Indonesia",
      "category": "International",
      "city": "Badung",
      "name": "Cuca Restaurant",
      "price_wna": 499999.99999999994,
      "rating": 4.5
    },
    {
      "address": "Lot N5, ITDC Tourism Complex Nusa Dua Sofitel Bali Nusa Dua Beach Resort, Nusa Dua, Benoa 80363 Indonesia",
      "category": "International",
      "city": "Badung",
      "name": "Kwee Zeen",
      "price_wna": 300000.0,
      "rating": 5.0
    },
    {
      "address": "Jl. Munduk Catu No.8, Canggu 80361 Indonesia",
      "category": "International",
      "city": "Badung",
      "name": "Beach Boy Canggu",
      "price_wna": 300000.0,
      "rating": 5.0
    }
  ]
}
```

### API Endpoint: ```/api/model/recommendations/itineraries```

Method: ```POST```

Example Body Request:
```json
{   
    budget: 1000000,
    city: "Denpasar" (optional)
}
```
cURL:
```bash
curl -X POST http://localhost:3000/api/model/recommendations/itineraries -H "Content-Type: application/json" -d "{\"budget\": 1000000, \"city\": \"Denpasar\"}"
```

Response (Success):
```json
{
  "itinerary": {
    "accommodation": {
      "city": "Denpasar",
      "name": "Bali Eco Living Dormitory",
      "price": 102000.0
    },
    "culinary_1": {
      "city": "Denpasar",
      "name": "Kayumanis Seaside Sanur",
      "price": 300000.0
    },
    "culinary_2": {
      "city": "Denpasar",
      "name": "Kayumanis Seaside Sanur",
      "price": 300000.0
    },
    "culinary_3": {
      "city": "Denpasar",
      "name": "Jack Fish",
      "price": 100000.0
    },
    "remaining_budget": 104.56000000002678,
    "total_cost": 999895.44,
    "tour_1": {
      "city": "Denpasar",
      "name": "Karang Beach",
      "price": 34473.86
    },
    "tour_2": {
      "city": "Denpasar",
      "name": "Karang Beach",
      "price": 34473.86
    },
    "tour_3": {
      "city": "Denpasar",
      "name": "CitraLand Waterpark",
      "price": 50000.0
    },
    "tour_4": {
      "city": "Denpasar",
      "name": "MUSEUM AGUNG PANCASILA",
      "price": 34473.86
    },
    "tour_5": {
      "city": "Denpasar",
      "name": "Bali Festival Park, Padang Galak",
      "price": 10000.0
    },
    "tour_6": {
      "city": "Denpasar",
      "name": "Srilanka Beach",
      "price": 34473.86
    },
    "tour_free_166": {
      "city": "Denpasar",
      "name": "Werdhi Budaya Art Centre",
      "price": 0.0
    },
    "tour_free_181": {
      "city": "Denpasar",
      "name": "Pantai Segara Ayu",
      "price": 0.0
    },
    "tour_free_21": {
      "city": "Denpasar",
      "name": "Daerah tujuan wisata tukad bindu",
      "price": 0.0
    }
  }
}
```
