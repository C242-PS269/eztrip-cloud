# Data Server & API Services Documentation

### Overview

<p align=justify>
This documentation outlines the available API endpoints in the application, including their functionality, request methods, and example usage. These endpoints are designed to handle user account management, data-related tasks, and other operations that the application may require.
</p>

### API Endpoint: ```/register```

```
curl -X POST http://localhost:5000/register -H "Content-Type: application/json" -d "{\"username\":\"john_doe\",\"email\":\"john@example.com\",\"password\":\"password123\",\"confirm_password\":\"password123\",\"phone_number\":\"1234567890\"}"
```

### API Endpoint: ```/login```

```
curl -X POST http://localhost:5000/login -H "Content-Type: application/json" -d "{\"username\":\"john_doe\",\"password\":\"password123\"}"
```

### API Endpoint: ```/update```

```
curl -X PUT http://localhost:5000/update -H "Content-Type: application/json" -d "{\"username\":\"john_doe\",\"current_password\":\"password123\",\"new_password\":\"newpassword456\",\"new_phone\":\"9876543210\"}"
```

### API Endpoint: ```/delete```

```
curl -X DELETE http://localhost:5000/delete -H "Content-Type: application/json" -d "{\"username\":\"john_doe\",\"password\":\"newpassword456\"}"
```