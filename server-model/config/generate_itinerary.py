# Import required libraries
import sqlalchemy as sa
import pandas as pd


# Load datasets (replace with your dataset paths)
# Load data once at startup
tours = pd.read_csv("data/tour.csv", usecols=["name", "price_wna", "city"])
culinary = pd.read_csv("data/culinary.csv", usecols=["name", "price_wna", "city"])
accommodations = pd.read_csv("data/accommodation.csv", usecols=["name", "price_wna", "city"])

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

    # Remove the selected items from the lists to prevent re-adding the same items
    tours_filtered = tours_filtered[tours_filtered['name'] != selected_tour['name']]
    culinary_filtered = culinary_filtered[culinary_filtered['name'] != selected_culinary['name']]
    accommodations_filtered = accommodations_filtered[accommodations_filtered['name'] != selected_accommodation['name']]

    # Initialize index for additional items
    tour_index = 2
    culinary_index = 2

    # Only add more items if there is enough budget left
    added_item = False  # To track if we add any item in each iteration

    while remaining_budget >= 0:
        # Break if no affordable item found in either category
        if remaining_budget <= 0:
            print("Remaining budget is exhausted. Stopping itinerary generation.")
            break

        added_item = False  # Reset added_item flag

        # Add additional tours if affordable
        affordable_tours = tours_filtered[tours_filtered['price_wna'] <= remaining_budget]
        if not affordable_tours.empty:
            additional_tour = affordable_tours.iloc[0]
            itinerary[f"tour_{tour_index}"] = {
                "name": additional_tour['name'],
                "price": additional_tour['price_wna'],
                "city": additional_tour['city'],
            }
            remaining_budget -= additional_tour['price_wna']  # Subtract only after adding
            print(f"Added tour: {additional_tour['name']}, Remaining budget: {remaining_budget}")
            added_item = True
            tour_index += 1
            # Remove the added tour from the list
            tours_filtered = tours_filtered[tours_filtered['name'] != additional_tour['name']]
        else:
            print("No more affordable tours can be added.")
        
        # Add additional culinary if affordable
        affordable_culinary = culinary_filtered[culinary_filtered['price_wna'] <= remaining_budget]
        if not affordable_culinary.empty:
            additional_culinary = affordable_culinary.iloc[0]
            itinerary[f"culinary_{culinary_index}"] = {
                "name": additional_culinary['name'],
                "price": additional_culinary['price_wna'],
                "city": additional_culinary['city'],
            }
            remaining_budget -= additional_culinary['price_wna']  # Subtract only after adding
            print(f"Added culinary: {additional_culinary['name']}, Remaining budget: {remaining_budget}")
            added_item = True
            culinary_index += 1
            # Remove the added culinary from the list
            culinary_filtered = culinary_filtered[culinary_filtered['name'] != additional_culinary['name']]
        else:
            print("No more affordable culinary can be added.")

        # Check if no items were added in the iteration
        if not added_item:
            print("No more items can be added within the remaining budget.")
            break

    # Log final itinerary
    total_cost = user_budget - remaining_budget
    itinerary["total_cost"] = total_cost
    itinerary["remaining_budget"] = remaining_budget
    print(f"Final itinerary: {itinerary}")

    return itinerary