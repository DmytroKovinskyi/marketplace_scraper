from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
import time
from app.db import models
from datetime import datetime

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

def save_rozetka_scraped_data(db, product_id: int, platform_id: int, scraped_list: list):
    saved = []
    for item in scraped_list:
        db_data = models.ScrapedProductData(
            product_id=product_id,
            platform_id=platform_id,
            url_on_platform=item.get("url_on_platform"),
            name_on_platform=item.get("name_on_platform"),
            price=item.get("price"),
            currency=item.get("currency"),
            rating=item.get("rating"),
            reviews_count=item.get("reviews_count"),
            availability_status=item.get("availability_status"),
            scraped_at=datetime.utcnow(),
            search_position=item.get("search_position"),
        )
        db.add(db_data)
        saved.append(db_data)
    db.commit()
    return saved

def scrape_citrus_smartphones(query: str, limit: int = 10):
    results = []
    search_url = f"https://www.citrus.ua/search/?q={query}"
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(search_url)
        time.sleep(2)
        html = page.content()
        soup = BeautifulSoup(html, "html.parser")
        items = soup.select("div.product-card")
        for item in items[:limit]:
            name = item.select_one(".product-card__name").get_text(strip=True) if item.select_one(".product-card__name") else None
            price = item.select_one(".product-card__price-value").get_text(strip=True) if item.select_one(".product-card__price-value") else None
            url = item.select_one("a.product-card__photo")
            url = url["href"] if url and url.has_attr("href") else None
            rating = None  # Citrus не завжди показує рейтинг
            reviews = item.select_one(".product-card__reviews-count")
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

def save_citrus_scraped_data(db, product_id: int, platform_id: int, scraped_list: list):
    saved = []
    for item in scraped_list:
        db_data = models.ScrapedProductData(
            product_id=product_id,
            platform_id=platform_id,
            url_on_platform=item.get("url_on_platform"),
            name_on_platform=item.get("name_on_platform"),
            price=item.get("price"),
            currency=item.get("currency"),
            rating=item.get("rating"),
            reviews_count=item.get("reviews_count"),
            availability_status=item.get("availability_status"),
            scraped_at=datetime.utcnow(),
            search_position=item.get("search_position"),
        )
        db.add(db_data)
        saved.append(db_data)
    db.commit()
    return saved

def scrape_amazon_smartphones(query: str, limit: int = 10):
    results = []
    search_url = f"https://www.amazon.com/s?k={query.replace(' ', '+')}"
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(search_url)
        time.sleep(2)
        html = page.content()
        soup = BeautifulSoup(html, "html.parser")
        items = soup.select("div.s-result-item[data-component-type='s-search-result']")
        for item in items[:limit]:
            name = item.select_one("h2 .a-text-normal").get_text(strip=True) if item.select_one("h2 .a-text-normal") else None
            price_whole = item.select_one(".a-price-whole")
            price_frac = item.select_one(".a-price-fraction")
            price = None
            if price_whole and price_frac:
                price = float(f"{price_whole.get_text(strip=True)}.{price_frac.get_text(strip=True)}")
            url = item.select_one("h2 a.a-link-normal")
            url = f"https://www.amazon.com{url['href']}" if url and url.has_attr("href") else None
            rating = item.select_one(".a-icon-alt")
            rating = float(rating.get_text(strip=True).split()[0].replace(',', '.')) if rating else None
            reviews = item.select_one(".a-size-base.s-underline-text")
            reviews_count = int(reviews.get_text(strip=True).replace(',', '')) if reviews else None
            results.append({
                "name_on_platform": name,
                "price": price,
                "url_on_platform": url,
                "rating": rating,
                "reviews_count": reviews_count,
                "currency": "USD",
                "availability_status": None,
                "search_position": len(results) + 1
            })
        browser.close()
    return results

def save_amazon_scraped_data(db, product_id: int, platform_id: int, scraped_list: list):
    saved = []
    for item in scraped_list:
        db_data = models.ScrapedProductData(
            product_id=product_id,
            platform_id=platform_id,
            url_on_platform=item.get("url_on_platform"),
            name_on_platform=item.get("name_on_platform"),
            price=item.get("price"),
            currency=item.get("currency"),
            rating=item.get("rating"),
            reviews_count=item.get("reviews_count"),
            availability_status=item.get("availability_status"),
            scraped_at=datetime.utcnow(),
            search_position=item.get("search_position"),
        )
        db.add(db_data)
        saved.append(db_data)
    db.commit()
    return saved
