# Machine Learning Models Server & API Services Documentation

### Overview

<p align=justify>
This repo contains the machine learning models API service and demonstrates how to use them for generating personalized recommendations. It provides endpoints for recommending various items (e.g., recommendations, culinaries, accommodations, generate itineraies) based on user inputs like price, rating, category, and city. The API integrates machine learning models to process user data and deliver tailored suggestions.
</p>

### Important Notes

The APIs URL in documentation its still in local development ```http://localhost:4000/```, if the backend is already deployed, then the mobile development team just need to change the domain name that will be provided by cloud computing team.

### API Endpoint: ```/tours```

Overview:

The ```/tours``` API endpoint is used to fetch tour recommendations based on various filters such as ```max_price```, ```min_rating```, ```category```, and ```city```. It accepts ```POST``` requests and returns a list of tours that match the specified criteria.

Base URL:
```bash
http://localhost:4000/tours
```

Method: ```POST```

- Giving 5 Recommendations Based On ```max_price``` + ```min_rating``` + ```city``` + ```category``` :

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
    curl -X POST http://localhost:4000/tours -H "Content-Type: application/json" -d "{\"max_price\": 100000, \"min_rating\": 4, \"category\": \"Beach\", \"city\": \"Denpasar\"}"
    ```

### API Endpoint: ```/tours/visited```

Overview:

The ```/tours/visited``` API endpoint provides recommendations for tours based on user input, such as ```tour_name```, ```city_filter```, and ```max_price```. The endpoint accepts ```POST``` requests and returns the top 5 recommended tours that match the given inputs.

Base URL:
```bash
http://localhost:4000/tours/visited
```

Method: ```POST```

- Giving Top 5 Recommendations Based On ```tour_name``` + ```city_filter``` + ```max_price``` :

    Example Body Request:
    ```json
    {
        "tour_name": "Balangan Beach",
        "city_filter": "Badung",
        "max_price": 100000
    }
    ```

    cURL:
    ```bash
    curl -X POST http://localhost:4000/tours/visited -H "Content-Type: application/json" -d "{\"tour_name\":\"Balangan Beach\", \"city_filter\":\"Badung\", \"max_price\":100000}"
    ````

- Giving Top 5 Recommendations Based On ```tour_name``` + ```city_filter``` :

    Example Body Request:
    ```json
    {
        "tour_name": "Balangan Beach",
        "city_filter": "Badung"
    }
    ```

    cURL:
    ```bash
    curl -X POST http://localhost:4000/tours/visited -H "Content-Type: application/json" -d "{\"tour_name\":\"Balangan Beach\", \"city_filter\":\"Badung\"}"
    ```

- Giving Top 5 Recommendations Based On ```tour_name``` + ```max_price``` :

    Example Body Request:
    ```json
    {
        "tour_name": "Balangan Beach",
        "max_price": 100000
    }
    ```

    cURL:
    ```bash
    curl -X POST http://localhost:4000/tours/visited -H "Content-Type: application/json" -d "{\"tour_name\":\"Balangan Beach\", \"max_price\":100000}"

- Giving Top 5 Recommendations Based On ```tour_name``` :

    Example Body Request:
    ```json
    {
        "tour_name": "Balangan Beach"
    }
    ```
    
    cURL:
    ```bash
    curl -X POST http://localhost:4000/tours/visited -H "Content-Type: application/json" -d "{\"tour_name\":\"Balangan Beach\"}"
    ```

### API Endpoint: ```/accommodations```

Overview:
The ```/accommodations``` API endpoint provides accommodation recommendations based on the user's input, including filters for ```city```, ```min_rating```, and ```max_price```. It accepts ```POST``` requests and returns a list of recommended accommodations that match the specified filters.

Base URL:
```bash
http://localhost:4000/accommodations
```

Method: ```POST```

- Giving Top 5 Recommendations Based On ```city``` + ```min_rating``` + ```max_price``` :

    Example Body Request:
    ```json
    {
        "city": "Denpasar",
        "min_rating": 4,
        "max_price": 100000
    }
    ```

    cURL:
    ```bash
    curl -X POST http://localhost:4000/accommodations -H "Content-Type: application/json" -d "{\"city\": \"Denpasar\", \"min_rating\": 4, \"max_price\": 100000}"
    ```

### API Endpoint: ```/accommodations/visited```

Overview:
The ```/accommodations/visited``` API endpoint provides recommendations for accommodations based on the user's input, including filters for ```accommodation_name```, ```city_filter```, and ```max_price```. It returns the top 5 recommendations that match the provided intpus.

Method: ```POST```

Base URL:
```bash
http://localhost:4000/accommodations/visited
```

- Giving Top 5 Recommendations Based On ```accommodation_name``` + ```city_filter``` + ```max_price```:

    Example Body Request:
    ```json
    {
        "accommodation_name": "The Seiryu Boutique Villas",
        "city_filter": "Badung",
        "max_price": 500000
    }
    ```

    cURL:
    ```bash
    curl -X POST http://localhost:4000/accommodations/visited -H "Content-Type: application/json" -d "{\"accommodation_name\":\"The Seiryu Boutique Villas\", \"city_filter\":\"Badung\", \"max_price\":500000}"
    ```

- Giving Top 5 Recommendations Based On ```accommodation_name``` + ```city_filter``` :

    Example Body Request:
    ```json
    {
        "accommodation_name": "The Seiryu Boutique Villas",
        "city_filter": "Badung",
    }
    ```

    cURL:
    ```bash
    curl -X POST http://localhost:4000/accommodations/visited -H "Content-Type: application/json" -d "{\"accommodation_name\":\"The Seiryu Boutique Villas\", \"city_filter\":\"Badung\"}"
    ```
- Giving Top 5 Recommendations Based On ```accommodation_name``` + ```max_price```:

    Example Body Request:
    ```json
    {
        "accommodation_name": "The Seiryu Boutique Villas",
        "max_price": 500000
    }
    ```

    cURL:
    ```bash
    curl -X POST http://localhost:4000/accommodations/visited -H "Content-Type: application/json" -d "{\"accommodation_name\":\"The Seiryu Boutique Villas\", \"max_price\":500000}"

- Giving Top 5 Recommendations Based On ```accommodation_name``` :

    Example Body Request:
    ```json
    {
        "accommodation_name": "The Seiryu Boutique Villas"
    }
    ```

    cURL:
    ```bash
    curl -X POST http://localhost:4000/accommodations/visited -H "Content-Type: application/json" -d "{\"accommodation_name\":\"The Seiryu Boutique Villas\"}"


### API Endpoint: ```/culinaries```

The ```/culinaries``` API endpoint provides culinary recommendations based on the user's input, including ```category```, ```city```, ```min_rating```, and ```max_price```. This endpoint accepts ```POST``` requests and returns a list of recommended culinary spots that match the specified inputs.

Base URL:
```bash
http://localhost:4000/culinaries
```

Method: ```POST```

- Giving Top 5 Recommendations Based On ```category``` + ```city``` + ```min_rating``` + ```max_price```: 

    Example Body Request:
    ```json
    {
        "max_price": 100000,
        "min_rating": 4.0,
        "category": "Bar",
        "city": "Denpasar"
    }
    ```

    cURL:
    ```bash
    curl -X POST http://localhost:4000/culinaries -H "Content-Type: application/json" -d "{\"category\": \"Bar\", \"city\": \"Denpasar\", \"min_rating\": 4.0, \"max_price\": 100000}"
    ```

### API Endpoint: ```/culinaries/visited```

Overview:
The ```/culinaries/visited``` API endpoint provides recommendations for culinary spots based on the user's input, including ```culinary_name```, ```city_filter```, and ```max_price```. This endpoint accepts ```POST``` requests and returns the top 5 recommended culinary spots that match the provided inputs.

Base URL:
```bash
http://localhost:4000/culinaries/visited
```

Method: ```POST```

- Giving Top 5 Recommendation Based On ```culinary_name``` + ```city_filter``` + ```max_price``` :

    Example Body Request:
    ```json
    {
        "culinary_name": "Koral Restaurant",
        "city_filter": "Badung",
        "max_price": 500000
    }
    ```

    cURL:
    ```bash
    curl -X POST http://127.0.0.1:4000/culinaries/visited -H "Content-Type: application/json" -d "{\"culinary_name\":\"Koral Restaurant\", \"city_filter\":\"Badung\", \"max_price\":500000}"
    ```

- Giving Top 5 Recommendation Based On ```culinary_name``` + ```city_filter``` :

    Example Body Request:
    ```json
    {
        "culinary_name": "Koral Restaurant",
        "city_filter": "Badung"
    }
    ```

    cURL:
    ```bash
    curl -X POST http://127.0.0.1:4000/culinaries/visited -H "Content-Type: application/json" -d "{\"culinary_name\":\"Koral Restaurant\", \"city_filter\":\"Badung\"}"

- Giving Top 5 Recommendation Based On ```culinary_name``` + ```max_price``` :

    Example Body Request:
    ```json
    {
        "culinary_name": "Koral Restaurant",
        "max_price": 500000
    }
    ```

    cURL:
    ```bash
    curl -X POST http://127.0.0.1:4000/culinaries/visited -H "Content-Type: application/json" -d "{\"culinary_name\":\"Koral Restaurant\", \"max_price\":500000}"

- Giving Top 5 Recommendation Based On ```culinary_name``` :

    Example Body Request:
    ```json
    {
        "culinary_name": "Koral Restaurant"
    }
    ```

    cURL:
    ```bash
    curl -X POST http://127.0.0.1:4000/culinaries/visited -H "Content-Type: application/json" -d "{\"culinary_name\":\"Koral Restaurant\"}"

### API Endpoint: ```/itineraries```

Overview:

The ```/itineraries``` API endpoint generates automatic travel itineraries based on the user's input, including ```budget``` and optional ```city```. This endpoint accepts POST requests and returns a list of recommended itineraries based on the specified ```budget``` (and ```city```, if provided).

Base URL:
```bash
http://localhost:4000/itineraries
```

Method: ```POST```

- Generate Automatic Itineraries Based On ```Budget``` + ```City``` :

    Example Body Request:
    ```json
    {
        "budget": 1000000,
        "city": "Denpasar"
    }
    ```

    cURL:
    ```bash
    curl -X POST http://localhost:4000/itineraries -H "Content-Type: application/json" -d "{\"budget\": 1000000, \"city\": \"Denpasar\"}"
    ```

- Generate Automatic Itineraries Based On ```Budget``` :

    Example Body Request:
    ```json
    {
        "budget": 1000000
    }
    ```

    cURL:
    ```bash
    curl -X POST http://localhost:4000/itineraries -H "Content-Type: application/json" -d "{\"budget\": 1000000}"
    ```