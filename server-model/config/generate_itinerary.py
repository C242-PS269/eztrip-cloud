import pandas as pd
from config.sql_engine import engine

# Load data from the database
tours = pd.read_sql_query("SELECT name, price_wna, city FROM tours", engine)
culinary = pd.read_sql_query("SELECT name, price_wna, city FROM culinaries", engine)
accommodations = pd.read_sql_query("SELECT name, price_wna, city FROM accommodations", engine)

def generate_itineraries(user_budget, city=None):
    """
    Generates an itinerary based on the user's budget, including tours, culinary experiences, and accommodation.
    
    Args:
        user_budget (float): The total budget for the itinerary.
        city (str, optional): The city where the itinerary should be generated. If None, no city filtering is applied.

    Returns:
        dict: A dictionary containing the generated itinerary with selected tours, culinary experiences, and accommodations, 
              along with the total cost and remaining budget.
    """
    if user_budget <= 0:
            return {"error": "Budget must be greater than 0."}

    try:
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

        # Filter data based on budget
        tours_filtered = tours_filtered[tours_filtered['price_wna'] <= tour_budget].reset_index(drop=True)
        culinary_filtered = culinary_filtered[culinary_filtered['price_wna'] <= culinary_budget].reset_index(drop=True)
        accommodations_filtered = accommodations_filtered[accommodations_filtered['price_wna'] <= accommodation_budget].reset_index(drop=True)
        
        print(f"Filtered data: Tours: {len(tours_filtered)}, Culinary: {len(culinary_filtered)}, Accommodations: {len(accommodations_filtered)}")

        # Handle case when no valid options are found
        if tours_filtered.empty or culinary_filtered.empty or accommodations_filtered.empty:
            print("Not enough options found within the budget.")
            return {"error": "Not enough options within the given budget and city"}

        # Initialize itinerary dictionary and remaining budget
        itinerary = {}
        remaining_budget = user_budget
        print(f"Initial remaining budget: {remaining_budget}")

        # Handle free/zero-cost tours (e.g., beaches)
        free_tours = tours_filtered[tours_filtered['price_wna'] == 0].head(3)  # Max 3 free tours
        for idx, free_tour in free_tours.iterrows():
            itinerary[f"tour_free_{idx+1}"] = {
                "name": free_tour['name'],
                "price": free_tour['price_wna'],
                "city": free_tour['city'],
            }

        # Exclude free tours from further processing
        tours_filtered = tours_filtered[tours_filtered['price_wna'] > 0]

        # Select one item from each category
        if not tours_filtered.empty:
            selected_tour = tours_filtered.iloc[0]
            itinerary["tour_1"] = {
                "name": selected_tour['name'],
                "price": selected_tour['price_wna'],
                "city": selected_tour['city'],
            }
            remaining_budget -= selected_tour['price_wna']
        else:
            selected_tour = None

        if not culinary_filtered.empty:
            selected_culinary = culinary_filtered.iloc[0]
            itinerary["culinary_1"] = {
                "name": selected_culinary['name'],
                "price": selected_culinary['price_wna'],
                "city": selected_culinary['city'],
            }
            remaining_budget -= selected_culinary['price_wna']
        else:
            selected_culinary = None

        if not accommodations_filtered.empty:
            selected_accommodation = accommodations_filtered.iloc[0]
            itinerary["accommodation"] = {
                "name": selected_accommodation['name'],
                "price": selected_accommodation['price_wna'],
                "city": selected_accommodation['city'],
            }
            remaining_budget -= selected_accommodation['price_wna']
        else:
            selected_accommodation = None

        # Additional items only if budget permits
        print(f"Remaining budget after initial selections: {remaining_budget}")

        tour_index = 2
        culinary_index = 2

        while remaining_budget > 0:
            added_item = False

            # Add additional tours if affordable
            affordable_tours = tours_filtered[tours_filtered['price_wna'] <= remaining_budget]
            if not affordable_tours.empty:
                additional_tour = affordable_tours.iloc[0]
                itinerary[f"tour_{tour_index}"] = {
                    "name": additional_tour['name'],
                    "price": additional_tour['price_wna'],
                    "city": additional_tour['city'],
                }
                remaining_budget -= additional_tour['price_wna']
                print(f"Added tour: {additional_tour['name']}, Remaining budget: {remaining_budget}")
                tour_index += 1
                added_item = True
                tours_filtered = tours_filtered[tours_filtered['name'] != additional_tour['name']]

            # Add additional culinary if affordable
            affordable_culinary = culinary_filtered[culinary_filtered['price_wna'] <= remaining_budget]
            if not affordable_culinary.empty:
                additional_culinary = affordable_culinary.iloc[0]
                itinerary[f"culinary_{culinary_index}"] = {
                    "name": additional_culinary['name'],
                    "price": additional_culinary['price_wna'],
                    "city": additional_culinary['city'],
                }
                remaining_budget -= additional_culinary['price_wna']
                print(f"Added culinary: {additional_culinary['name']}, Remaining budget: {remaining_budget}")
                culinary_index += 1
                added_item = True
                culinary_filtered = culinary_filtered[culinary_filtered['name'] != additional_culinary['name']]

            if not added_item:
                print("No more items can be added within the remaining budget.")
                break

        # Log final itinerary
        total_cost = user_budget - remaining_budget
        itinerary["total_cost"] = total_cost
        itinerary["remaining_budget"] = remaining_budget
        print(f"Final itinerary: {itinerary}")

        return itinerary
    except Exception as e:
        print(f"Error during itinerary generation: {str(e)}")
        return {"error": "Failed to generate itinerary due to internal error."}