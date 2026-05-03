import asyncio
import json
import os
from playwright.async_api import async_playwright

async def run_enrichment():
    async with async_playwright() as p:
        # Use the persistent directory to keep your session 'warm'
        user_data_dir = os.path.join(os.getcwd(), "amazon_session")
        context = await p.chromium.launch_persistent_context(
            user_data_dir,
            headless=False,
            slow_mo=500,
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0"
        )
        page = context.pages[0]

        if not os.path.exists("cleaned_dataset.json"):
            print("ERROR: File 'cleaned_dataset.json' not found!")
            return

        with open("cleaned_dataset.json", "r") as f:
            master_data = json.load(f)

        print(f"\n--- STARTING GREEDY AUTO-DETECTION ---")

        for i, product in enumerate(master_data):
            # Safe way to get the name for display
            display_name = product.get('product_title') or product.get('title') or "Product"
            
            if not product.get("reviews") or len(product["reviews"]) == 0:
                print(f"\n[{i+1}/60] TARGET: {display_name[:40]}")
                
                try:
                    await page.goto(product['url'], wait_until="domcontentloaded")

                    print("   [WAITING] Solve Captcha or click 'See all reviews'...")
                    
                    # Wait up to 5 minutes for ANY review-like element to appear
                    # We use a comma-separated list of possible selectors
                    await page.wait_for_selector('div[data-hook="review"], .review, .a-section.review', timeout=300000)
                    
                    print("   [DETECTED] Reviews found! Vacuuming data...")
                    await page.wait_for_timeout(2000) # Let the page finish rendering

                    reviews = []
                    # GREEDY SELECTORS: Try every known Amazon review container
                    elements = await page.query_selector_all('div[data-hook="review"]') or \
                               await page.query_selector_all('.a-section.review') or \
                               await page.query_selector_all('.review')
                    
                    for el in elements:
                        # GREEDY BODY SELECTORS: Try every known Amazon review body tag
                        body = await el.query_selector('[data-hook="review-body"]') or \
                               await el.query_selector('.review-text-content') or \
                               await el.query_selector('.review-body') or \
                               await el.query_selector('.a-expander-content')
                        
                        if body:
                            text = (await body.inner_text()).strip().replace('\n', ' ')
                            if text and len(text) > 5:
                                reviews.append({"text": text})
                    
                    # EMERGENCY BACKUP: If containers were found but text wasn't
                    if not reviews and elements:
                        print("   [!] Logic backup: Searching for raw text blocks...")
                        for el in elements:
                            all_spans = await el.query_selector_all('span')
                            for span in all_spans:
                                t = await span.inner_text()
                                if len(t) > 40: # Only grab significant blocks of text
                                    reviews.append({"text": t.strip()})
                                    break

                    product["reviews"] = reviews
                    
                    # Save progress immediately so you never lose a single product
                    with open("cleaned_dataset.json", "w") as f:
                        json.dump(master_data, f, indent=4)
                    
                    if reviews:
                        print(f"   ✔ SUCCESS: Saved {len(reviews)} reviews.")
                    else:
                        print(f"   ✘ FAILED: Found page but could not extract text.")

                except Exception as e:
                    print(f"   ✘ Skipping: {e}")
            else:
                print(f"[{i+1}] Already done.")

        await context.close()

if __name__ == "__main__":
    asyncio.run(run_enrichment())