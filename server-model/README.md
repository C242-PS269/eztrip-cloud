# Machine Learning Models Server & API Services Documentation

### Overview



### API Endpoint: ```/recommendations```
- POST:
```
curl -X POST http://localhost:3000/recommendations -H "Content-Type: application/json" -d "{\"max_price\": 100000, \"min_rating\": 4, \"category\": \"Beach\", \"city\": \"Denpasar\"}"
```

### API Endpoint: ```/accommodations```
- POST:
```
curl -X POST http://localhost:3000/accommodations -H "Content-Type: application/json" -d "{\"city\": \"Denpasar\", \"min_rating\": 4, \"max_price\": 100000}"
```

### API Endpoint: ```/culinaries```
- POST:
```
curl -X POST http://localhost:3000/culinaries \ -H "Content-Type: application/json" \ -d "{\"category\": \"Bar\", \"city\": \"Denpasar\", \"min_rating\": 4.0, \"max_price\": 100000}"
```

### API Endpoint: ```/itineraries```
- POST:
    - Generate Automatic Itineraries Based On ```Budget``` Only:
        ```
        curl -X POST http://localhost:3000/itineraries -H "Content-Type: application/json" -d "{\"budget\": 1000000}"
        ```
    - Generate Automatic Itineraries Based On ```Budget``` + ```City``` :
        ```
        curl -X POST http://localhost:3000/itineraries -H "Content-Type: application/json" -d "{\"budget\": 1000000, \"city\": \"Denpasar\"}"
        ```