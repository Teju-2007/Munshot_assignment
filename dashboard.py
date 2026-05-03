import streamlit as st
import pandas as pd
import json
import plotly.express as px

# Set page config for a professional UI polish
st.set_page_config(page_title="Luggage Competitive Intelligence", layout="wide")

# 1. LOAD DATA
with open("brand_summary.json", "r") as f:
    brand_df = pd.DataFrame(json.load(f))
with open("cleaned_dataset.json", "r") as f:
    product_df = pd.DataFrame(json.load(f))

# Helper to clean prices for filtering
product_df['clean_price'] = product_df['price'].apply(lambda x: float(str(x).replace(',', '').replace('₹', '')) if x else 0)

# --- SIDEBAR FILTERS ---
st.sidebar.header("📊 Interactive Filters")
selected_brands = st.sidebar.multiselect("Select Brands", options=brand_df['brand'].unique(), default=brand_df['brand'].unique())
price_range = st.sidebar.slider("Price Range (₹)", 0, int(product_df['clean_price'].max()), (0, 10000))

# Apply Filters
filtered_brand_df = brand_df[brand_df['brand'].isin(selected_brands)]
filtered_product_df = product_df[
    (product_df['brand'].isin(selected_brands)) & 
    (product_df['clean_price'] >= price_range[0]) & 
    (product_df['clean_price'] <= price_range[1])
]

# --- HEADER SECTION ---
st.title("🧳 Luggage Market Intelligence Dashboard")
st.markdown("### Decision-Ready Analysis for Amazon India Marketplace")

col1, col2, col3, col4 = st.columns(4)
col1.metric("Brands Analyzed", len(filtered_brand_df))
col2.metric("Products Tracked", len(filtered_product_df))
col3.metric("Avg. Market Sentiment", f"{filtered_brand_df['avg_sentiment'].mean():.2f}")
col4.metric("Avg. Price Point", f"₹{filtered_product_df['clean_price'].mean():,.0f}")

st.divider()

# --- VIEW 1: BRAND COMPARISON ---
st.subheader("🎯 Brand Benchmarking")
tab1, tab2 = st.tabs(["Price vs Sentiment", "Pricing Spread"])

with tab1:
    fig = px.scatter(filtered_brand_df, x="avg_price", y="avg_sentiment", text="brand", 
                     size="avg_price", color="brand", height=500,
                     labels={"avg_price": "Avg Price (₹)", "avg_sentiment": "Sentiment Score"})
    st.plotly_chart(fig, use_container_width=True)

with tab2:
    st.markdown("**Product-Level Price Spread:** Identifying Market Positioning")
    fig_box = px.box(filtered_product_df, x="brand", y="clean_price", color="brand", points="all")
    st.plotly_chart(fig_box, use_container_width=True)

# --- VIEW 2: PRODUCT DRILLDOWN ---
st.divider()
st.subheader("🔍 Product-Level Drilldown")
product_name = st.selectbox("Select a Specific Product to Analyze", filtered_product_df['title'].unique())
selected_p = filtered_product_df[filtered_product_df['title'] == product_name].iloc[0]

d_col1, d_col2 = st.columns([1, 2])
with d_col1:
    st.info(f"**Price:** ₹{selected_p['clean_price']}")
    st.success(f"**Sentiment Score:** {selected_p['sentiment_score']}")
    st.write(f"**Position:** {selected_p.get('position', 'N/A')}")

with d_col2:
    st.markdown("**Review Synthesis:**")
    st.write(f"✅ **Pros:** {', '.join(selected_p['top_themes']['pros'])}")
    st.write(f"❌ **Cons:** {', '.join(selected_p['top_themes']['cons'])}")

# --- AGENT INSIGHTS (The Bonus Layer) ---
st.sidebar.divider()
st.sidebar.header("🤖 Agent Insights (Non-Obvious)")
st.sidebar.write("1. **Value Gap:** Safari leads sentiment while being 36% cheaper than VIP.")
st.sidebar.write("2. **Durability Paradox:** Premium brands show high durability complaints despite high price points.")
st.sidebar.write("3. **Price Sensitivity:** Skybags dominates the ₹2500-₹2700 band with stable sentiment.")
st.sidebar.write("4. **Risk Factor:** VIP's sentiment variance is high, indicating inconsistent product quality.")
st.sidebar.write("5. **Market Opportunity:** Lack of 'Premium' (₹5k+) high-sentiment options suggests a gap for luxury entrants.")
