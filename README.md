# 🧳 Luggage Competitive Intelligence Dashboard
### Amazon India Market Analysis & Sentiment Synthesis

## 📌 Project Overview
This project is a decision-ready competitive intelligence dashboard built to analyze the luggage market on Amazon India. It transforms raw marketplace data—product listings and customer reviews—into structured insights regarding pricing strategy, customer sentiment, and brand positioning.

## 🚀 Core Features
* **Automated Data Collection**: Reproducible scraping workflow using **Playwright** to extract product details and reviews.
* **Sentiment Synthesis**: Multi-threaded sentiment analysis using the **NLTK VADER** lexicon to generate compound scores (-1 to 1).
* **Aspect-Level Theme Extraction**: Automated detection of recurring praise and complaints regarding **Wheels, Zippers, and Durability**.
* **Interactive Dashboard**: A **Streamlit** interface featuring Brand Benchmarking, Pricing Spread (Box Plots), and Product Drilldowns.
* **Agent Insights**: A dedicated layer surfacing 5 non-obvious conclusions from data trends.

## 🛠️ Tech Stack
* **Scraping**: Python, Playwright.
* **Analysis**: Pandas, NLTK.
* **UI/UX**: Streamlit, Plotly.

## 📊 Methodology
1. **Extraction**: Scraped 4+ brands (Safari, Skybags, American Tourister, VIP).
2. **Enrichment**: Analyzed reviews to extract sentiment and themes.
3. **Synthesis**: Aggregated data into competitive benchmarks.
4. **Presentation**: Visualized findings for business decision-making.

## ⚠️ Limitations & Trade-offs
* **Review Availability**: Product #28 (Skybags) was identified with 0 reviews; the system documents this as a data limitation.
* **Sample Size**: Limited to the first page of reviews (8 per product) to maintain a low scraping footprint and avoid detection.

## 🏃 How to Run
1. Install dependencies: `pip install -r requirements.txt`
2. Setup Playwright: `playwright install chromium`
3. Run the Dashboard: `streamlit run dashboard.py`
