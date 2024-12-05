-- Create the accommodations table
CREATE TABLE accommodations (
    name VARCHAR(255) NOT NULL,          -- Name of the accommodation
    rating FLOAT CHECK (rating >= 0 AND rating <= 5),  -- Rating (1-5)
    price_wna DECIMAL(10, 2),            -- Price with no taxes (WNA)
    city VARCHAR(255) NOT NULL           -- City where the accommodation is located
);

-- Create the tours table
CREATE TABLE tours (
    name VARCHAR(255) NOT NULL,          -- Name of the tour
    rating FLOAT CHECK (rating >= 0 AND rating <= 5),  -- Rating (1-5)
    category VARCHAR(255),               -- Category of the tour (e.g., adventure, culture)
    price_wna DECIMAL(10, 2),            -- Price with no taxes (WNA)
    city VARCHAR(255) NOT NULL,          -- City where the tour is available
    address VARCHAR(255),                -- Address of the tour
    google_maps VARCHAR(255)             -- Google Maps link for the tour location
);

-- Create the culinaries table
CREATE TABLE culinaries (
    name VARCHAR(255) NOT NULL,          -- Name of the culinary experience
    rating FLOAT CHECK (rating >= 0 AND rating <= 5),  -- Rating (1-5)
    category VARCHAR(255),               -- Category of the culinary experience (e.g., fine dining)
    price_wna DECIMAL(10, 2),            -- Price with no taxes (WNA)
    city VARCHAR(255) NOT NULL,          -- City where the culinary experience is located
    address VARCHAR(255)                 -- Address of the culinary experience
);

-- Create the users table
CREATE TABLE users (
    id CHAR(36) PRIMARY KEY,             -- Unique ID using Python UUID format (36 characters)
    email VARCHAR(255) NOT NULL,         -- User's email address
    username VARCHAR(255) NOT NULL,      -- User's username
    password VARCHAR(255) NOT NULL,      -- User's password (should be stored securely)
    phone_number VARCHAR(20)            -- User's phone number
);

CREATE TABLE itineraries (
    id CHAR(36) PRIMARY KEY,                -- Unique identifier for the itinerary
    user_id VARCHAR(255) NOT NULL,      -- User ID associated with the itinerary
    itinerary_data JSON NOT NULL,      -- JSON data containing the details of the itinerary
    total_cost DECIMAL(10, 2) NOT NULL, -- Total cost of the itinerary
    remaining_budget DECIMAL(10, 2) NOT NULL, -- Remaining budget after itinerary creation
    budget DECIMAL(10, 2) NOT NULL,     -- Original budget provided by the user
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, -- Timestamp for when the itinerary is created
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP -- Timestamp for when the itinerary is last updated
);

