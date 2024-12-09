-- Create the accommodations table
CREATE TABLE accommodations (
    id CHAR(36) PRIMARY KEY,
    name VARCHAR(255) NOT NULL,          -- Name of the accommodation
    rating FLOAT CHECK (rating >= 0 AND rating <= 5),  -- rating (1-5)
    price_wna DECIMAL(10, 2),            -- Price with no taxes (WNA)
    city VARCHAR(255) NOT NULL           -- City where the accommodation is located
);

-- Create the tours table
CREATE TABLE tours (
    id CHAR(36) PRIMARY KEY,
    name VARCHAR(255) NOT NULL,          -- Name of the tour
    rating FLOAT CHECK (rating >= 0 AND rating <= 5),  -- rating (1-5)
    category VARCHAR(255),               -- Category of the tour (e.g., adventure, culture)
    price_wna DECIMAL(10, 2),            -- Price with no taxes (WNA)
    city VARCHAR(255) NOT NULL,          -- City where the tour is available
    address VARCHAR(255),                -- Address of the tour
    google_maps VARCHAR(255)             -- Google Maps link for the tour location
);

-- Create the culinaries table
CREATE TABLE culinaries (
    id CHAR(36) PRIMARY KEY,
    name VARCHAR(255) NOT NULL,          -- Name of the culinary experience
    rating FLOAT CHECK (rating >= 0 AND rating <= 5),  -- rating (1-5)
    category VARCHAR(255),               -- Category of the culinary experience (e.g., fine dining)
    price_wna DECIMAL(10, 2),            -- Price with no taxes (WNA)
    city VARCHAR(255) NOT NULL,          -- City where the culinary experience is located
    address VARCHAR(255)                 -- Address of the culinary experience
);

-- Create the users table
CREATE TABLE users (
    id VARCHAR(255) PRIMARY KEY,           
    email VARCHAR(255) NOT NULL,         -- user's email address
    username VARCHAR(255) NOT NULL,      -- user's username
    password VARCHAR(255) NOT NULL,      -- user's password (should be stored securely)
    phone_number VARCHAR(20)            -- user's phone number
);

CREATE TABLE itineraries (
    id CHAR(36) PRIMARY KEY,                -- Unique identifier for the itinerary
    user_id VARCHAR(255) NOT NULL,      -- user id associated with the itinerary
    itinerary_data JSON NOT NULL,      -- JSON data containing the details of the itinerary
    total_cost DECIMAL(10, 2) NOT NULL, -- Total cost of the itinerary
    remaining_budget DECIMAL(10, 2) NOT NULL, -- Remaining budget after itinerary creation
    budget DECIMAL(10, 2) NOT NULL,     -- Original budget provided by the user
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, -- Timestamp for when the itinerary is created
    FOREIGN KEY (user_id) REFERENCES users(id) 
);

CREATE TABLE accommodations_reviews (
    id CHAR(36) PRIMARY KEY,
    user_id VARCHAR(255) NOT NULL,              -- user_id should be CHAR(36) like users(id)
    accommodations_id CHAR(36) NOT NULL,             -- Change INT to CHAR(36) to match accommodations(id)
    rating DECIMAL(3, 2),
    reviews TEXT,
    sentiment ENUM('positive', 'negative', 'neutral') DEFAULT 'neutral',
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (accommodations_id) REFERENCES accommodations(id)
);


CREATE TABLE tours_reviews (
    id CHAR(36) PRIMARY KEY,
    user_id VARCHAR(255) NOT NULL,
    tours_id CHAR(36) NOT NULL,
    rating DECIMAL(3, 2),
    reviews TEXT,
    sentiment ENUM('positive', 'negative', 'neutral') DEFAULT 'neutral',
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (tours_id) REFERENCES tours(id)
);

CREATE TABLE culinary_reviews (
    id CHAR(36) PRIMARY KEY, 
    user_id VARCHAR(255) NOT NULL,
    culinaries_id CHAR(36) NOT NULL,
    rating FLOAT CHECK (rating >= 0 AND rating <= 5),
    reviews TEXT,
    sentiment ENUM('positive', 'negative', 'neutral') DEFAULT 'neutral',
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (culinaries_id) REFERENCES culinaries(id)
);

CREATE TABLE expenses (
    expense_id CHAR(36) PRIMARY KEY,          -- UUID primary key for expenses
    user_id VARCHAR(255) NOT NULL,                -- UUID foreign key to user table
    category VARCHAR(50),                     -- Category of the expense (e.g., food, transport)
    amount DECIMAL(10, 2),                    -- Amount spent
    description TEXT,                         -- Description of the expense
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, -- Timestamp when the expense is created
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, -- Timestamp for when the itinerary is last updated
    FOREIGN KEY (user_id) REFERENCES users(id)  -- Foreign key referencing user table
    
);