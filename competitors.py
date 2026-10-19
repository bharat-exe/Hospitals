import asyncio
import csv
from playwright.async_api import async_playwright

# List of direct hospital chains & digital health competitors
COMPETITORS = [
    {"name": "Practo", "type": "HealthTech Aggregator", "url": "https://www.practo.com"},
    {"name": "Apollo Hospitals", "type": "Hospital Chain", "url": "https://www.apollohospitals.com"},
    {"name": "Yashoda Hospitals", "type": "Hospital Chain (Hyderabad)", "url": "https://www.yashodahospitals.com"},
    {"name": "KIMS Hospitals", "type": "Hospital Chain (Hyderabad)", "url": "https://www.kimshospitals.com"},
    {"name": "CARE Hospitals", "type": "Hospital Chain", "url": "https://www.carehospitals.com"},
    {"name": "Lybrate", "type": "HealthTech Aggregator", "url": "https://www.lybrate.com"},
    {"name": "MediBuddy", "type": "Digital Healthcare Platform", "url": "https://www.medibuddy.in"}
]

async def scrape_competitors():
    results = []

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
        )
        page = await context.new_page()

        for comp in COMPETITORS:
            print(f"Scraping competitor: {comp['name']} ({comp['url']})...")
            try:
                await page.goto(comp["url"], wait_until="domcontentloaded", timeout=45000)
                await asyncio.sleep(3)

                # 1. Extract Page Title
                title = await page.title()

                # 2. Extract Meta Description (Value Proposition)
                meta_desc = await page.query_selector('meta[name="description"]')
                description = await meta_desc.get_attribute("content") if meta_desc else "N/A"

                # 3. Extract Top Headings (H1/H2 - Core Offerings & Messaging)
                headings = await page.eval_on_selector_all(
                    "h1, h2",
                    "elements => elements.map(e => e.innerText.trim()).filter(t => t.length > 3).slice(0, 8)"
                )

                # 4. Detect Key Digital Features on Homepage (Booking, Emergency, Lab, Telehealth, etc.)
                body_text = (await page.inner_text("body")).lower()
                features = []
                feature_keywords = [
                    "book appointment", "online consultation", "video consultation",
                    "health checkup", "lab test", "medicine", "emergency",
                    "insurance", "second opinion", "home care", "find a doctor"
                ]
                for kw in feature_keywords:
                    if kw in body_text:
                        features.append(kw.title())

                results.append({
                    "Competitor Name": comp["name"],
                    "Category": comp["type"],
                    "URL": comp["url"],
                    "Title": title.strip() if title else "N/A",
                    "Value Proposition (Meta)": description.strip() if description else "N/A",
                    "Detected Features": ", ".join(features) if features else "Standard Info",
                    "Key Headings / Sections": " | ".join(headings) if headings else "N/A"
                })

            except Exception as e:
                print(f"  -> Error scraping {comp['name']}: {e}")
                results.append({
                    "Competitor Name": comp["name"],
                    "Category": comp["type"],
                    "URL": comp["url"],
                    "Title": "Error loading",
                    "Value Proposition (Meta)": "N/A",
                    "Detected Features": "N/A",
                    "Key Headings / Sections": "N/A"
                })

        await browser.close()

    # Save to CSV
    filename = "competitors.csv"
    if results:
        fieldnames = [
            "Competitor Name", "Category", "URL", "Title",
            "Value Proposition (Meta)", "Detected Features", "Key Headings / Sections"
        ]
        with open(filename, mode="w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(results)
        print(f"\nSuccess! Saved {len(results)} competitors to {filename}")

if __name__ == "__main__":
    asyncio.run(scrape_competitors())