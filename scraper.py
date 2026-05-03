import asyncio
import json
import os
from playwright.async_api import async_playwright

BRANDS = ["Safari", "Skybags", "American Tourister", "VIP"]
PRODUCTS_PER_BRAND = 15 

async def auto_scroll(page):
    for _ in range(3):
        await page.mouse.wheel(0, 1000)
        await page.wait_for_timeout(1000)

async def run_full_scraper():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context(user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/124.0.0.0")
        page = await context.new_page()
        
        # Reset file for a clean test
        with open("cleaned_dataset.json", "w") as f:
            json.dump([], f)

        for brand in BRANDS:
            print(f"\n--- SCRAPING: {brand} ---")
            try:
                await page.goto(f"https://www.amazon.in/s?k={brand}+luggage", wait_until="load")
                await auto_scroll(page)
                
                # Broadest possible selector for the product containers
                items = await page.query_selector_all('div[data-component-type="s-search-result"]')
                
                success_count = 0
                for item in items:
                    if success_count >= PRODUCTS_PER_BRAND: break
                    
                    # EXTRACTOR: Tries multiple tag patterns
                    data = await item.evaluate('''el => {
                        // Look for any H2, or any link with a specific size class
                        const titleEl = el.querySelector('h2') || el.querySelector('.a-size-medium') || el.querySelector('.a-size-base-plus');
                        const linkEl = el.querySelector('a[href*="/dp/"]');
                        const priceEl = el.querySelector('.a-price-whole');
                        
                        return {
                            title: titleEl ? titleEl.innerText.trim() : null,
                            url: linkEl ? linkEl.href : null,
                            price: priceEl ? priceEl.innerText.replace(/[^0-9]/g, '') : "0"
                        }
                    }''')

                    if data['title'] and data['url']:
                        print(f"   [+] Saved: {data['title'][:40]}")
                        
                        # Save to file immediately
                        with open("cleaned_dataset.json", "r+") as f:
                            curr = json.load(f)
                            curr.append({"brand": brand, **data, "reviews": []})
                            f.seek(0)
                            json.dump(curr, f, indent=4)
                            f.truncate()
                        success_count += 1
                    else:
                        # This helps us see if it's finding titles but missing links (or vice-versa)
                        pass

            except Exception as e:
                print(f"   ! Error: {e}")

        await browser.close()

if __name__ == "__main__":
    asyncio.run(run_full_scraper())
    print(f"\nCheck 'cleaned_dataset.json' now!")