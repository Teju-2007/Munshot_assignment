import json

def aggregate_brand_data():
    with open("cleaned_dataset.json", "r") as f:
        data = json.load(f)

    brands = {}

    for p in data:
        # Normalize brand name (e.g., Safari, Skybags)
        # Assuming your scraper saved a 'brand' key, or we extract from title
        brand_name = p.get('brand') or (p.get('product_title') or p.get('title') or "Other").split()[0]
        
        if brand_name not in brands:
            brands[brand_name] = {
                "product_count": 0,
                "total_price": 0,
                "total_discount": 0,
                "total_sentiment": 0,
                "all_pros": [],
                "all_cons": []
            }
        
        b = brands[brand_name]
        b["product_count"] += 1
        
        # Handle pricing (ensure they are numbers, not strings with ₹)
        try:
            price = float(str(p.get('price', 0)).replace(',', '').replace('₹', ''))
            list_price = float(str(p.get('list_price', 0)).replace(',', '').replace('₹', ''))
            discount = ((list_price - price) / list_price * 100) if list_price > 0 else 0
        except:
            price, discount = 0, 0

        b["total_price"] += price
        b["total_discount"] += discount
        b["total_sentiment"] += p.get('sentiment_score', 0)
        b["all_pros"].extend(p.get('top_themes', {}).get('pros', []))
        b["all_cons"].extend(p.get('top_themes', {}).get('cons', []))

    # Calculate final averages
    summary = []
    for name, stats in brands.items():
        avg_price = stats["total_price"] / stats["product_count"]
        avg_sentiment = stats["total_sentiment"] / stats["product_count"]
        
        summary.append({
            "brand": name,
            "avg_price": round(avg_price, 2),
            "avg_discount": round(stats["total_discount"] / stats["product_count"], 1),
            "avg_sentiment": round(avg_sentiment, 2),
            "top_pros": list(set(stats["all_pros"]))[:3],
            "top_cons": list(set(stats["all_cons"]))[:3],
            "position": "Premium" if avg_price > 5000 else "Mass-Market" # Simple logic for the 'Product Thinking' requirement
        })

    with open("brand_summary.json", "w") as f:
        json.dump(summary, f, indent=4)
    
    print("✔ SUCCESS: brand_summary.json created for your dashboard overview!")

if __name__ == "__main__":
    aggregate_brand_data()