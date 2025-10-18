import pandas as pd
import numpy as np
from pathlib import Path


# Set random seed for reproducibility
np.random.seed(42)

# Sample product reviews (varying lengths)
reviews = [
    # Short reviews (negative)
    "Terrible product. Don't buy.",
    "Not worth it.",
    "Broke after one week.",
    "Very disappointed.",
    "Poor quality.",
    
    # Medium reviews (mixed)
    "It's okay but nothing special. Works as expected.",
    "Decent product for the price. Had some minor issues.",
    "Good but could be better. Missing some features.",
    "Average quality. Not bad but not great either.",
    "Works fine. Installation was a bit tricky.",
    
    # Long reviews (positive)
    "Absolutely love this product! The quality is outstanding and it exceeded all my expectations. Been using it for months now with zero issues. Highly recommend to anyone looking for reliability and performance.",
    "Best purchase I've made this year. The build quality is exceptional, features are exactly what I needed, and customer service was fantastic. Worth every penny. Will definitely buy from this brand again.",
    "Incredible product! I was skeptical at first but after using it daily for several weeks, I'm completely sold. The attention to detail is remarkable and it just works flawlessly. My colleagues are asking where I got it.",
    "Five stars all the way! This has made my life so much easier. The design is intuitive, setup was straightforward, and performance is top-notch. Can't imagine going back to my old setup now.",
    "Exceeded expectations in every way. I did extensive research before buying and this was the best choice. The quality, functionality, and value are all exceptional. Already recommended to three friends.",
]

# Generate 50 products with realistic patterns
data = []

for i in range(50):
    # Pick a random review
    review = np.random.choice(reviews)
    
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