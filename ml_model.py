import pandas as pd
from collections import Counter

# List of fast food items (case-insensitive)
FAST_FOOD_ITEMS = {"maggi", "pizza", "burger", "fries", "noodles", "chips", "soda"}

def analyze_spending(expenses):
    if not expenses:
        return ["No expenses yet—start tracking!"]
    
    # Convert expenses to DataFrame
    try:
        df = pd.DataFrame(expenses, columns=['id', 'amount', 'category', 'subcategory', 'description', 'date'])
    except ValueError as e:
        return [f"Error processing data: {str(e)}. Please reset the database."]
    
    # Filter for Food category with Fast Food subcategory
    fast_food_df = df[(df['category'] == 'Food') & (df['subcategory'] == 'Fast Food')]
    
    # Count occurrences of fast food descriptions
    desc_counts = Counter(fast_food_df['description'].str.lower())
    
    # Generate notifications
    notifications = []
    total_fast_food_count = len(fast_food_df)
    
    # Check individual fast food items
    for desc, count in desc_counts.items():
        if desc in FAST_FOOD_ITEMS and count >= 3:
            notifications.append(
                f"Hey! You've bought {desc.capitalize()} {count} times this week. "
                "It’s hitting your wallet and health—too much fast food isn’t great!"
            )
    
    # General fast food warning
    if total_fast_food_count >= 5:
        notifications.append(
            f"Wow, you’ve had fast food {total_fast_food_count} times this week! "
            "Time to cut back—it’s heavy on your pocket and body."
        )
    
    # General excessive spending warning (any item)
    all_desc_counts = Counter(df['description'].str.lower())
    for desc, count in all_desc_counts.items():
        if count > 5 and desc not in FAST_FOOD_ITEMS:
            notifications.append(
                f"You’ve spent on {desc.capitalize()} {count} times this week—watch out!"
            )
    
    return notifications if notifications else ["All good for now—keep tracking!"]

if __name__ == "__main__":
    sample_expenses = [
        (1, 2.0, "Food", "Fast Food", "Maggi", "2025-04-01"),
        (2, 3.0, "Food", "Fast Food", "Pizza", "2025-04-02"),
        (3, 2.0, "Food", "Fast Food", "Maggi", "2025-04-03"),
        (4, 2.0, "Food", "Fast Food", "Maggi", "2025-04-04"),
        (5, 5.0, "Transport", "Public Transport", "Bus", "2025-04-05"),
        (6, 2.0, "Food", "Fast Food", "Burger", "2025-04-06")
    ]
    print(analyze_spending(sample_expenses))