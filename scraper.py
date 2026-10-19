import asyncio
import csv
from playwright.async_api import async_playwright

async def scrape_google_maps(search_query: str, max_results: int = 20):
    results = []

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
        )
        page = await context.new_page()

        encoded_query = search_query.replace(" ", "+")
        url = f"https://www.google.com/maps/search/{encoded_query}/"
        print(f"Opening: {url}")

        # Use domcontentloaded to prevent networkidle timeouts
        await page.goto(url, wait_until="domcontentloaded", timeout=60000)
        await asyncio.sleep(5)

        # Handle any initial cookie or consent dialogs if they appear
        try:
            reject_button = await page.query_selector('button[aria-label="Reject all"]')
            if reject_button:
                await reject_button.click()
                await asyncio.sleep(2)
        except Exception:
            pass

        feed_selector = 'div[role="feed"]'
        try:
            await page.wait_for_selector(feed_selector, timeout=20000)
        except Exception:
            print("Listing feed not detected. Make sure the page finished rendering.")
            await browser.close()
            return

        print("Scrolling results panel...")
        for _ in range(5):
            await page.evaluate(f'''
                const el = document.querySelector('{feed_selector}');
                if (el) el.scrollTop += 2500;
            ''')
            await asyncio.sleep(2.5)

        # Retrieve listings
        cards = await page.query_selector_all('div[role="feed"] > div > div[role="article"]')
        if not cards:
            cards = await page.query_selector_all('a.hfpxzc')

        print(f"Found {len(cards)} items. Extracting details...")

        for card in cards[:max_results]:
            try:
                name_elem = await card.query_selector('.qBF1Pd, .fontHeadlineSmall')
                name = await name_elem.inner_text() if name_elem else "N/A"

                rating_elem = await card.query_selector('span.MW4etd')
                rating = await rating_elem.inner_text() if rating_elem else "N/A"

                review_elem = await card.query_selector('span.UY7F9')
                reviews = await review_elem.inner_text() if review_elem else "0"
                reviews = reviews.replace("(", "").replace(")", "").strip()

                info_elem = await card.query_selector('.W4Efsd')
                info = await info_elem.inner_text() if info_elem else "N/A"

                link_elem = await card.query_selector('a.hfpxzc')
                link = await link_elem.get_attribute('href') if link_elem else "N/A"

                if name != "N/A":
                    results.append({
                        "name": name,
                        "rating": rating,
                        "reviews": reviews,
                        "details": info.replace("\n", " | "),
                        "url": link
                    })
            except Exception:
                continue

        await browser.close()

    filename = "hospitals.csv"
    if results:
        with open(filename, mode="w", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=["name", "rating", "reviews", "details", "url"])
            writer.writeheader()
            writer.writerows(results)
        print(f"Success: Saved {len(results)} hospitals to {filename}")
    else:
        print("No items extracted. The page structure might require an adjusted selector.")

if __name__ == "__main__":
    TARGET_QUERY = "Hospitals in Hyderabad"
    asyncio.run(scrape_google_maps(TARGET_QUERY, max_results=20))