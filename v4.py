import requests
from bs4 import BeautifulSoup
from textblob import TextBlob
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from jinja2 import Template

# --- Step 1: Data Collection (Scraping Reviews) ---
def get_reviews(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Extract reviews and ratings (Modify this part based on actual website structure)
    reviews = soup.find_all('div', class_='review-class')
    review_data = []
    for review in reviews:
        review_text = review.find('p').text
        review_rating = review.find('span', class_='rating').text
        review_data.append({
            'review': review_text,
            'rating': review_rating
        })

    return pd.DataFrame(review_data)

# Example URL for reviews (change this to actual brand URL)
brand_reviews_url = "https://example.com/reviews"
df_reviews = get_reviews(brand_reviews_url)

# --- Step 2: Sentiment Analysis ---
def analyze_sentiment(reviews):
    sentiments = []
    for review in reviews['review']:
        blob = TextBlob(review)
        sentiment = blob.sentiment.polarity  # Range from -1 (negative) to 1 (positive)
        sentiments.append(sentiment)
    return sentiments

df_reviews['sentiment'] = analyze_sentiment(df_reviews)
df_reviews['sentiment_label'] = df_reviews['sentiment'].apply(lambda x: 'Positive' if x > 0 else ('Negative' if x < 0 else 'Neutral'))

# --- Step 3: Visualize Sentiment Distribution ---
def visualize_sentiment(df_reviews):
    sns.countplot(data=df_reviews, x='sentiment_label', palette='coolwarm')
    plt.title('Sentiment Distribution of Reviews')
    plt.show()

visualize_sentiment(df_reviews)

# --- Step 4: Brand Legitimacy Data (Manual or Scraped Data) ---
brand_data = {
    'brand_name': 'Brand X',
    'moral_legitimacy': 'Ethical labor practices and environmental sustainability.',
    'environmental_impact': 'Has a good track record for reducing carbon footprint.',
    'brand_recognition': 'Highly recognized in the tech industry.',
    'consumer_perceptions': 'Mostly positive consumer feedback, though some complaints about pricing.',
    'product_quality': 'Generally good, with some issues in consistency.',
    'pricing_strategy': 'Competitive pricing with occasional discounts.',
    'positive_reviews': 'Many reviews praise the quality and customer service.',
    'negative_reviews': 'Some reviews cite issues with shipping delays.',
    'brand_response': 'Quick and transparent responses to complaints.',
    'final_verdict': 'Overall legitimate with minor issues to address.',
    'recommendations': 'Continue improving customer service and transparency.',
    'cognitive_legitimacy': 'Strong presence in market, but minor awareness issues in certain regions.',
    'pragmatic_legitimacy': 'Delivers on product promises, but occasional shipping issues.',
    'psychological_distance': 'Close connection with customers due to responsive support.',
    'brand_trust': 'Generally trusted, but has occasional trust issues related to product quality.',
    'brand_loyalty': 'High customer retention, especially among repeat buyers.',
}

# --- Step 5: Jinja2 Template for Full Report ---
report_template = """
# Brand Legitimacy Report: {{ brand_name }}

## Introduction
The increasing importance of brand legitimacy has led us to evaluate the credibility and trustworthiness of **{{ brand_name }}**. This report evaluates the brand's legitimacy across various key dimensions, including consumer reviews, product quality, and industry comparison.

## Section 1: Brand Legitimacy Dimensions

### 1. Moral Legitimacy
- **Labor Practices**: {{ moral_legitimacy }}
- **Environmental Impact**: {{ environmental_impact }}

### 2. Cognitive Legitimacy
- **Brand Recognition**: {{ brand_recognition }}
- **Consumer Perceptions**: {{ consumer_perceptions }}

### 3. Pragmatic Legitimacy
- **Product Quality**: {{ product_quality }}
- **Pricing Strategy**: {{ pricing_strategy }}

## Section 2: Customer Feedback

### Positive Reviews
- **Sentiment**: {{ positive_reviews }}

### Negative Reviews
- **Issues Identified**: {{ negative_reviews }}

### Response to Feedback
- **Brand Response**: {{ brand_response }}

## Section 3: Sentiment Analysis and Insights

### Review Sentiment Distribution
- **Overall Sentiment Analysis**:
  - **Positive**: {{ positive_reviews_count }}
  - **Negative**: {{ negative_reviews_count }}
  - **Neutral**: {{ neutral_reviews_count }}

## Section 4: Consumer-Brand Relationship

### Psychological Distance
- **Emotional Connection**: {{ psychological_distance }}

### Brand Trust
- **Customer Trust**: {{ brand_trust }}

### Brand Loyalty
- **Customer Loyalty**: {{ brand_loyalty }}

## Conclusion
- **Final Verdict**: {{ final_verdict }}

- **Recommendations**: {{ recommendations }}

"""

# --- Step 6: Prepare Data for Report ---
positive_reviews_count = len(df_reviews[df_reviews['sentiment_label'] == 'Positive'])
negative_reviews_count = len(df_reviews[df_reviews['sentiment_label'] == 'Negative'])
neutral_reviews_count = len(df_reviews[df_reviews['sentiment_label'] == 'Neutral'])

# Data to pass into the template
report_data = {**brand_data, 
               'positive_reviews_count': positive_reviews_count,
               'negative_reviews_count': negative_reviews_count,
               'neutral_reviews_count': neutral_reviews_count}

# --- Step 7: Generate the Full Report ---
template = Template(report_template)
report = template.render(report_data)

# Save the report to a file
with open("brand_legitimacy_report.md", "w") as file:
    file.write(report)

# --- Step 8: Display Report File Path ---
print("The brand legitimacy report has been generated and saved as 'brand_legitimacy_report.md'")
