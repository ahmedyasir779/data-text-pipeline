import pandas as pd
import numpy as np
from pathlib import Path


# Set random seed for reproducibility
np.random.seed(42)

# Sample product reviews (varying lengths)
# Add more varied reviews at the top
negative_reviews = [
    "Terrible product. Complete waste of money. Don't buy this!",
    "Broke after two days. Very disappointed with the quality.",
    "Not worth it at all. Save your money.",
    "Worst purchase ever. Customer service was unhelpful too.",
    "Cheap materials, poor design. Regret buying this.",
]

neutral_reviews = [
    "It's okay. Nothing special but does the job.",
    "Average product. Works as described but nothing impressive.",
    "Decent for the price. Not great, not terrible.",
    "It works. That's about all I can say.",
    "Meets basic expectations. Could be better.",
]

positive_reviews = [
    "Love it! Excellent quality and great value for money. Highly recommend!",
    "Best purchase I've made this year. Works perfectly and looks amazing.",
    "Outstanding product! Exceeded all my expectations. Five stars!",
    "Incredible! Fast shipping, great packaging, and the product is fantastic.",
    "Absolutely perfect. Been using it daily and it's still like new.",
]

all_reviews = negative_reviews + neutral_reviews + positive_reviews


# Generate 50 products with realistic patterns
data = []

for i in range(50):
    # Pick a random review
    review = np.random.choice(all_reviews)
    
    # Generate rating based on review length (positive correlation)
    # Longer reviews tend to be more positive
    review_length = len(review.split())
    base_rating = min(5, max(1, 2 + (review_length / 10)))
    rating = round(base_rating + np.random.normal(0, 0.5), 1)
    rating = min(5.0, max(1.0, rating))  # Clamp to 1-5
    
    # Generate price (some correlation with rating)
    base_price = 50 + (rating * 100)
    price = round(base_price + np.random.normal(0, 100), 2)
    price = max(10, price)
    
    # Generate sales (higher rated = more sales)
    base_sales = int(rating * 50)
    sales = max(1, int(base_sales + np.random.normal(0, 20)))
    
    data.append({
        'product_id': f'PROD{i+1:03d}',
        'product_name': f'Product {i+1}',
        'rating': rating,
        'price': price,
        'sales': sales,
        'review': review,
        'review_length': review_length
    })

# Create DataFrame
df = pd.DataFrame(data)

# Save to CSV
Path('data').mkdir(exist_ok=True)
df.to_csv('data/customer_reviews.csv', index=False)

print("✓ Created customer_reviews.csv")
print(f"  - {len(df)} products")
print(f"  - Ratings: {df['rating'].min():.1f} to {df['rating'].max():.1f}")
print(f"  - Prices: ${df['price'].min():.2f} to ${df['price'].max():.2f}")
print(f"  - Review lengths: {df['review_length'].min()} to {df['review_length'].max()} words")
print(f"\nCorrelation between rating and review length: {df['rating'].corr(df['review_length']):.3f}")