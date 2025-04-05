import pandas as pd
from collections import Counter

def analyze_spending(expenses):
    # Convert expenses to DataFrame
    df = pd.DataFrame(expenses, columns=['id', 'amount', 'category', 'description', 'date'])
    
    # Filter for the current week (simplified: assume all data is this week)
    # In a real app, you'd filter by date range
    
    # Count occurrences of descriptions (e.g., "Maggi")
    desc_counts = Counter(df['description'])
    
    # Generate notifications based on simple rules
    notifications = []
    for desc, count in desc_counts.items():
        if desc.lower() == "maggi" and count >= 3:
            notifications.append(
                f"Hey! You've bought Maggi {count} times this week. "
                "It’s heavy on your pocket and health—lead can harm you!"
            )
        elif count > 5:  # General rule for any item
            notifications.append(
                f"You’ve spent on {desc} {count} times this week—watch out!"
            )
    
    return notifications

# Test the function
if __name__ == "__main__":
    sample_expenses = [
        (1, 2.0, "Food", "Maggi", "2025-04-01"),
        (2, 2.0, "Food", "Maggi", "2025-04-02"),
        (3, 2.0, "Food", "Maggi", "2025-04-03"),
        (4, 5.0, "Transport", "Bus", "2025-04-04")
    ]
    print(analyze_spending(sample_expenses))