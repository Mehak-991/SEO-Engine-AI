import asyncio
# pyrefly: ignore [missing-import]
from playwright.async_api import async_playwright
import random

# Fallback mock products in case eBay blocks scraping
MOCK_PRODUCTS = [
    {"title": "Apple AirPods Pro (2nd Generation) - Active Noise Cancellation", "price": "$189.99", "url": "https://www.ebay.com/b/Apple-AirPods-Pro/"},
    {"title": "Samsung Galaxy S24 Ultra 256GB Titanium Unlocked Smartphone", "price": "$999.99", "url": "https://www.ebay.com/b/Samsung-Galaxy-S24/"},
    {"title": "Sony WH-1000XM5 Wireless Noise Canceling Headphones", "price": "$279.99", "url": "https://www.ebay.com/b/Sony-WH-1000XM5/"},
    {"title": "DJI Mini 4 Pro Drone Fly More Combo with 4K Camera", "price": "$759.00", "url": "https://www.ebay.com/b/DJI-Mini-4-Pro/"},
    {"title": "Apple Watch Series 9 GPS 45mm Midnight Aluminum Sport Band", "price": "$329.99", "url": "https://www.ebay.com/b/Apple-Watch-Series-9/"},
    {"title": "ASUS ROG Zephyrus G14 Gaming Laptop RTX 4060 AMD Ryzen 9", "price": "$1,149.99", "url": "https://www.ebay.com/b/ASUS-ROG-Gaming-Laptop/"},
    {"title": "GoPro HERO12 Black Action Camera - Waterproof 5.3K60 Ultra HD", "price": "$299.99", "url": "https://www.ebay.com/b/GoPro-HERO12/"},
    {"title": "Dyson V15 Detect Cordless Vacuum Cleaner with Laser Detection", "price": "$599.99", "url": "https://www.ebay.com/b/Dyson-V15/"},
    {"title": "LEGO Star Wars Millenium Falcon 75257 Building Kit 1353 Pieces", "price": "$119.99", "url": "https://www.ebay.com/b/LEGO-Star-Wars/"},
    {"title": 'LG C3 55" OLED evo 4K Smart TV with Dolby Vision & AI ThinQ', "price": "$896.99", "url": "https://www.ebay.com/b/LG-OLED-TV/"},
]

async def scrape_trending_ebay():
    products = []
    try:
        async with async_playwright() as p:
            user_agents = [
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
            ]
            browser = await p.chromium.launch(headless=True)
            context = await browser.new_context(
                user_agent=random.choice(user_agents),
                viewport={"width": 1280, "height": 800}
            )
            page = await context.new_page()

            await page.goto(
                "https://www.ebay.com/globaldeals",
                wait_until="domcontentloaded",
                timeout=30000
            )
            await page.wait_for_timeout(3000)  # let JS render

            # Try multiple selector patterns eBay uses
            selectors = [
                ".ebayui-dls-card",
                ".dne-item",
                ".srp-results .s-item",
                "[data-view='mi:1686']",
                ".deal-item",
            ]

            for selector in selectors:
                items = await page.query_selector_all(selector)
                if items:
                    for item in items[:12]:
                        try:
                            # Try various title and price selectors
                            title = None
                            for t_sel in [".ebayui-ellipsis-2", ".s-item__title", ".item-title", "h3", ".deal-item__title"]:
                                el = await item.query_selector(t_sel)
                                if el:
                                    title = (await el.inner_text()).strip()
                                    break

                            price = None
                            for p_sel in [".first", ".s-item__price", ".item-price", ".deal-item__price", ".realPrice"]:
                                el = await item.query_selector(p_sel)
                                if el:
                                    price = (await el.inner_text()).strip()
                                    break

                            link_el = await item.query_selector("a")
                            link = ""
                            if link_el:
                                link = await link_el.get_attribute("href") or ""
                                if link and not link.startswith("http"):
                                    link = f"https://www.ebay.com{link}"

                            if title and len(title) > 5 and "Shop on eBay" not in title:
                                products.append({
                                    "title": title,
                                    "price": price or "Check Price",
                                    "url": link or "https://www.ebay.com/globaldeals"
                                })
                        except Exception:
                            continue
                    if products:
                        break

            await browser.close()
    except Exception as e:
        print(f"Scrape error: {e}")

    # If scraping failed or blocked, return curated trending products
    if not products:
        print("Using mock trending products (eBay scraping blocked/failed)")
        products = MOCK_PRODUCTS

    return products


if __name__ == "__main__":
    results = asyncio.run(scrape_trending_ebay())
    print(f"Found {len(results)} products:")
    for res in results:
        print(f"  - {res['title']} | {res['price']}")
