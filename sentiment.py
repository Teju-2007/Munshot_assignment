import json
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer

# Download the required lexicon for sentiment analysis
nltk.download('vader_lexicon')

def analyze_sentiment():
    sia = SentimentIntensityAnalyzer()
    
    with open("cleaned_dataset.json", "r") as f:
        data = json.load(f)

    print("--- STARTING SENTIMENT SYNTHESIS ---")

    for product in data:
        reviews = product.get("reviews", [])
        
        if not reviews:
            product["sentiment_score"] = 0.0
            product["top_themes"] = {"pros": [], "cons": []}
            continue

        all_text = " ".join([r["text"] for r in reviews])
        
        # Calculate Sentiment Score (Compound ranges from -1 to 1)
        score = sia.polarity_scores(all_text)
        product["sentiment_score"] = round(score['compound'], 2)

        # Simple Theme Extraction based on common luggage keywords
        pros = []
        cons = []
        keywords = {
            "Wheels": ["wheels", "sturdy", "smooth", "movability"],
            "Zippers": ["zipper", "chain", "lock"],
            "Durability": ["strong", "sturdy", "unbreakable", "broken"],
            "Weight": ["light", "heavy", "weight"],
            "Space": ["roomy", "space", "compartment"]
        }

        # Logic to identify if keywords appear in positive or negative contexts
        for category, words in keywords.items():
            for word in words:
                if word in all_text.lower():
                    # If product score is high, assume keyword is a 'pro'
                    if product["sentiment_score"] > 0.1 and category not in pros:
                        pros.append(category)
                    elif product["sentiment_score"] < -0.1 and category not in cons:
                        cons.append(category)

        product["top_themes"] = {
            "pros": pros[:3], 
            "cons": cons[:3]
        }
        
        display_name = product.get('product_title') or product.get('title') or "Product"
        print(f"✔ Analyzed: {display_name[:30]} | Score: {product['sentiment_score']}")

    # Save the enriched data
    with open("cleaned_dataset.json", "w") as f:
        json.dump(data, f, indent=4)
    
    print("\nSUCCESS: Sentiment and Themes added to cleaned_dataset.json!")

if __name__ == "__main__":
    analyze_sentiment()