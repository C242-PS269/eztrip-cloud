# Import required libraries
import sqlalchemy as sa
import pandas as pd


# Load datasets (replace with your dataset paths)
# Load data once at startup
tours = pd.read_csv("data/tour.csv", usecols=["name", "price_wna", "city"])
culinary = pd.read_csv("data/culinary.csv", usecols=["name", "price_wna", "city"])
accommodations = pd.read_csv("data/accommodation.csv", usecols=["name", "price_wna", "city"])

"""
# Define the connection
username = 'GCP-SQL-ISNTANCE-USER'
password = 'GCP-SQL-ISNTANCE-PASSWORD'
database = 'DB-NAME'
host = 'GCP-SQL-INSTANCE'
port = '3306'

# Create the connection string
engineURL = f"mysql+mysqlconnector://{username}:{password}@{host}:{port}/{database}"
# Create the engine
engine = sa.create_engine(engineURL)

# Test the connection
try:
    with engine.connect() as connection:
        print("Connected to MySQL database successfully!")
except Exception as e:
    print("Connection failed:", e)

data_tour = pd.read_sql_query("SELECT * FROM itinerary", engine)
"""
def generate_itineraries(user_budget, city=None):
    print(f"Starting itinerary generation with budget: {user_budget}, city: {city}")
    
    # Allocate budget: 40% for tours, 30% for culinary, 30% for accommodation
    tour_budget = user_budget * 0.4
    culinary_budget = user_budget * 0.3
    accommodation_budget = user_budget * 0.3
    print(f"Allocated budgets: Tour: {tour_budget}, Culinary: {culinary_budget}, Accommodation: {accommodation_budget}")

    # Pre-filter data based on city (if given) and budget for all categories
    if city:
        tours_filtered = tours[tours['city'] == city]
        culinary_filtered = culinary[culinary['city'] == city]
        accommodations_filtered = accommodations[accommodations['city'] == city]
    else:
        tours_filtered = tours
        culinary_filtered = culinary
        accommodations_filtered = accommodations

    # Budget filtering once per category
    tours_filtered = tours_filtered[tours_filtered['price_wna'] <= tour_budget]
    culinary_filtered = culinary_filtered[culinary_filtered['price_wna'] <= culinary_budget]
    accommodations_filtered = accommodations_filtered[accommodations_filtered['price_wna'] <= accommodation_budget]
    
    print(f"Filtered data: Tours: {len(tours_filtered)}, Culinary: {len(culinary_filtered)}, Accommodations: {len(accommodations_filtered)}")

    # Handle case when no valid options are found
    if tours_filtered.empty or culinary_filtered.empty or accommodations_filtered.empty:
        print("Not enough options found within the budget.")
        return {"error": "Not enough options within the given budget and city"}

    # Initialize itinerary dictionary and remaining budget
    itinerary = {}
    remaining_budget = user_budget
    print(f"Initial remaining budget: {remaining_budget}")
    
    # Select the first item from each category
    selected_tour = tours_filtered.iloc[0]
    selected_culinary = culinary_filtered.iloc[0]
    selected_accommodation = accommodations_filtered.iloc[0]
    
    print(f"Selected: Tour: {selected_tour['name']}, Culinary: {selected_culinary['name']}, Accommodation: {selected_accommodation['name']}")

    # Add selected items to the itinerary
    itinerary["tour_1"] = {
        "name": selected_tour['name'],
        "price": selected_tour['price_wna'],
        "city": selected_tour['city'],
    }
    itinerary["culinary_1"] = {
        "name": selected_culinary['name'],
        "price": selected_culinary['price_wna'],
        "city": selected_culinary['city'],
    }
    itinerary["accommodation"] = {
        "name": selected_accommodation['name'],
        "price": selected_accommodation['price_wna'],
        "city": selected_accommodation['city'],
    }

    # Subtract costs from remaining budget only after adding to itinerary
    remaining_budget -= selected_tour['price_wna']
    remaining_budget -= selected_culinary['price_wna']
    remaining_budget -= selected_accommodation['price_wna']
    print(f"Remaining budget after initial selections: {remaining_budget}")

    # Try to add more items while remaining budget allows
    tour_index = 2
    culinary_index = 2

    affordable_tours = tours_filtered[tours_filtered['price_wna'] <= remaining_budget]
    affordable_culinary = culinary_filtered[culinary_filtered['price_wna'] <= remaining_budget]
    print(f"Affordable tours: {len(affordable_tours)}, Affordable culinary: {len(affordable_culinary)}")

    while remaining_budget > 0:
        added_item = False  # Flag to track if an item is added in this iteration
        
        # Add additional tours if affordable
        if not affordable_tours.empty:
            additional_tour = affordable_tours.iloc[0]
            itinerary[f"tour_{tour_index}"] = {
                "name": additional_tour['name'],
                "price": additional_tour['price_wna'],
                "city": additional_tour['city'],
            }
            remaining_budget -= additional_tour['price_wna']  # Subtract only after adding
            affordable_tours = affordable_tours[affordable_tours['price_wna'] <= remaining_budget]  # Re-filter
            tour_index += 1
            print(f"Added tour: {additional_tour['name']}, Remaining budget: {remaining_budget}")
            added_item = True
        
        # Add additional culinary if affordable
        if not affordable_culinary.empty:
            additional_culinary = affordable_culinary.iloc[0]
            itinerary[f"culinary_{culinary_index}"] = {
                "name": additional_culinary['name'],
                "price": additional_culinary['price_wna'],
                "city": additional_culinary['city'],
            }
            remaining_budget -= additional_culinary['price_wna']  # Subtract only after adding
            affordable_culinary = affordable_culinary[affordable_culinary['price_wna'] <= remaining_budget]  # Re-filter
            culinary_index += 1
            print(f"Added culinary: {additional_culinary['name']}, Remaining budget: {remaining_budget}")
            added_item = True

        # If no item is added, break the loop
        if not added_item:
            print("No more items can be added.")
            break

    # Log final itinerary
    total_cost = user_budget - remaining_budget
    itinerary["total_cost"] = total_cost
    itinerary["remaining_budget"] = remaining_budget
    print(f"Final itinerary: {itinerary}")

    return itinerary