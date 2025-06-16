from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
import time

def scrape_rozetka_smartphones(query: str, limit: int = 10):
    results = []
    search_url = f"https://rozetka.com.ua/search/?text={query}"
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(search_url)
        time.sleep(2)  # Дати сторінці завантажитись
        html = page.content()
        soup = BeautifulSoup(html, "html.parser")
        items = soup.select("div.goods-tile")
        for item in items[:limit]:
            name = item.select_one(".goods-tile__title").get_text(strip=True) if item.select_one(".goods-tile__title") else None
            price = item.select_one(".goods-tile__price-value").get_text(strip=True) if item.select_one(".goods-tile__price-value") else None
            url = item.select_one("a.goods-tile__picture")
            url = url["href"] if url and url.has_attr("href") else None
            rating = item.select_one(".goods-tile__rating")
            rating = float(rating["aria-label"].split()[1].replace(',', '.')) if rating and rating.has_attr("aria-label") else None
            reviews = item.select_one(".goods-tile__reviews-link")
            reviews_count = int(reviews.get_text(strip=True)) if reviews else None
            results.append({
                "name_on_platform": name,
                "price": float(price.replace('₴', '').replace(' ', '').replace(',', '.')) if price else None,
                "url_on_platform": url,
                "rating": rating,
                "reviews_count": reviews_count,
                "currency": "UAH",
                "availability_status": None,
                "search_position": len(results) + 1
            })
        browser.close()
    return results
