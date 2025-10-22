"""
Examples page - Sample datasets and use cases
"""

import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Examples",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Example Datasets & Use Cases")

st.markdown("""
Here are some example datasets you can use to test the platform.
""")

# Example 1: Customer Reviews
st.markdown("## 🛍️ Customer Product Reviews")

example1_data = {
    'product': ['Laptop', 'Phone', 'Tablet', 'Monitor', 'Keyboard'],
    'rating': [4.5, 3.8, 4.2, 4.7, 3.5],
    'price': [1200, 800, 600, 400, 150],
    'review': [
        'Great laptop! Fast performance and excellent build quality. Highly recommend for professionals.',
        'Good phone but battery life could be better. Camera is excellent though.',
        'Nice tablet for media consumption. Screen is beautiful but a bit heavy.',
        'Amazing monitor! Colors are vibrant and the 144Hz refresh rate is perfect for gaming.',
        'Keyboard is okay but keys feel a bit cheap. Not bad for the price.'
    ]
}

df1 = pd.DataFrame(example1_data)

st.dataframe(df1, use_container_width=True)

csv1 = df1.to_csv(index=False)
st.download_button(
    "⬇️ Download Customer Reviews CSV",
    csv1,
    "customer_reviews.csv",
    "text/csv"
)

# Example 2: Survey Responses
st.markdown("## 📝 Survey Responses")

example2_data = {
    'respondent_id': [1, 2, 3, 4, 5],
    'age_group': ['25-34', '35-44', '18-24', '45-54', '25-34'],
    'satisfaction': [8, 6, 9, 5, 7],
    'feedback': [
        'The service was excellent! Staff were very helpful and knowledgeable.',
        'Average experience. Nothing special but nothing bad either.',
        'Absolutely loved it! Will definitely come back and recommend to friends.',
        'Disappointed with the wait time. Service was okay once we got seated.',
        'Good overall but prices are a bit high for what you get.'
    ]
}

df2 = pd.DataFrame(example2_data)

st.dataframe(df2, use_container_width=True)

csv2 = df2.to_csv(index=False)
st.download_button(
    "⬇️ Download Survey Responses CSV",
    csv2,
    "survey_responses.csv",
    "text/csv"
)

# Example 3: Social Media Posts
st.markdown("## 📱 Social Media Posts")

example3_data = {
    'post_id': [1, 2, 3, 4, 5],
    'platform': ['Twitter', 'Instagram', 'Facebook', 'Twitter', 'Instagram'],
    'likes': [120, 450, 89, 234, 567],
    'post_text': [
        'Just tried the new @TechCorp phone! Camera quality is mind-blowing 📸 #tech #smartphone',
        'Beautiful sunset at Santa Monica Beach today 🌅 Perfect weather in Los Angeles!',
        'Excited to announce our new partnership with Amazon! Big things coming soon.',
        'Anyone else having issues with the latest software update? System keeps crashing 😤',
        'Delicious meal at The Italian Kitchen in NYC! Chef Mario really outdid himself 🍝'
    ]
}

df3 = pd.DataFrame(example3_data)

st.dataframe(df3, use_container_width=True)

csv3 = df3.to_csv(index=False)
st.download_button(
    "⬇️ Download Social Media Posts CSV",
    csv3,
    "social_media_posts.csv",
    "text/csv"
)

# Use Cases
st.markdown("---")
st.markdown("## 💡 Use Cases")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    ### 🛍️ E-commerce
    - Analyze product reviews
    - Track customer sentiment
    - Identify common complaints
    - Find trending products
    """)

with col2:
    st.markdown("""
    ### 📋 Market Research
    - Process survey responses
    - Identify themes
    - Sentiment tracking
    - Demographic analysis
    """)

with col3:
    st.markdown("""
    ### 📱 Social Media
    - Monitor brand mentions
    - Track engagement
    - Identify influencers
    - Sentiment analysis
    """)