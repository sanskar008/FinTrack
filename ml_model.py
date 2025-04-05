import pandas as pd
from collections import Counter
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import make_pipeline

# Sample training data for fast food classification
TRAINING_DATA = [
    ("maggi", 1), ("pizza", 1), ("burger", 1), ("fries", 1), ("noodles", 1), ("chips", 1), ("soda", 1),
    ("apple", 0), ("bread", 0), ("milk", 0), ("chicken", 0), ("rice", 0)
]
X_train = [item for item, label in TRAINING_DATA]
y_train = [label for item, label in TRAINING_DATA]

# Train a simple Naive Bayes classifier
model = make_pipeline(CountVectorizer(), MultinomialNB())
model.fit(X_train, y_train)

# Health data for fast food items (calories per typical serving, sodium in mg)
HEALTH_DATA = {
    "maggi": {"calories": 400, "sodium": 1500},
    "pizza": {"calories": 800, "sodium": 1200},
    "burger": {"calories": 600, "sodium": 1000},
    "fries": {"calories": 300, "sodium": 500},
    "noodles": {"calories": 350, "sodium": 1400},
    "chips": {"calories": 200, "sodium": 300},
    "soda": {"calories": 150, "sodium": 50}
}

def is_fast_food(item):
    return model.predict([item.lower()])[0] == 1

def get_health_warning(item, count):
    item = item.lower()
    if item in HEALTH_DATA:
        total_calories = HEALTH_DATA[item]["calories"] * count
        total_sodium = HEALTH_DATA[item]["sodium"] * count
        return (
            f"That’s {total_calories} calories and {total_sodium}mg sodium—watch your health!"
        )
    return "Too much fast food isn’t great for you!"

def analyze_spending(expenses):
    if not expenses:
        return ["No expenses yet—start tracking!"]
    
    try:
        df = pd.DataFrame(expenses, columns=['id', 'amount', 'category', 'subcategory', 'description', 'date'])
    except ValueError as e:
        return [f"Error processing data: {str(e)}. Please reset the database."]
    
    fast_food_df = df[(df['category'] == 'Food') & (df['subcategory'] == 'Fast Food')]
    desc_counts = Counter(fast_food_df['description'].str.lower())
    
    notifications = []
    total_fast_food_count = len(fast_food_df)
    
    for desc, count in desc_counts.items():
        if is_fast_food(desc) and count >= 3:
            health_warning = get_health_warning(desc, count)
            notifications.append(
                f"Hey! You've bought {desc.capitalize()} {count} times this week. "
                f"It’s hitting your wallet and health—{health_warning}"
            )
    
    if total_fast_food_count >= 5:
        total_calories = sum(
            HEALTH_DATA.get(desc, {"calories": 0})["calories"] * cnt 
            for desc, cnt in desc_counts.items() if is_fast_food(desc)
        )
        notifications.append(
            f"Wow, you’ve had fast food {total_fast_food_count} times this week! "
            f"That’s around {total_calories} calories—time to cut back!"
        )
    
    all_desc_counts = Counter(df['description'].str.lower())
    for desc, count in all_desc_counts.items():
        if count > 5 and not is_fast_food(desc):
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