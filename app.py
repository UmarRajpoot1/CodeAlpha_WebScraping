"""
CodeAlpha Data Analytics Internship - Task 1: Web Scraping
Flask app: a small local web UI to WATCH the scraper work live,
page by page, in the browser. Great for recording your demo video.

Run with: python app.py
Then open: http://127.0.0.1:5000 in your browser.
"""

from flask import Flask, jsonify, render_template, request
import requests
from bs4 import BeautifulSoup
import pandas as pd
from urllib.parse import urljoin

app = Flask(__name__)

BASE_URL = "https://books.toscrape.com/catalogue/page-{}.html"

RATING_MAP = {"One": 1, "Two": 2, "Three": 3, "Four": 4, "Five": 5}

DATASET_PATH = "books_dataset.csv"


def parse_books_from_html(html: str, page_url: str) -> list[dict]:
    soup = BeautifulSoup(html, "html.parser")
    books = []

    for article in soup.select("article.product_pod"):
        title = article.h3.a["title"]

        price_text = article.select_one("p.price_color").get_text(strip=True)
        price = float(price_text.replace("£", "").replace("Â", ""))

        rating_word = article.select_one("p.star-rating")["class"][1]
        rating = RATING_MAP.get(rating_word, None)

        availability = article.select_one("p.instock.availability").get_text(strip=True)
        image_src = article.select_one("img")["src"]
        image = urljoin(page_url, image_src)

        books.append(
            {
                "title": title,
                "price_gbp": price,
                "rating_out_of_5": rating,
                "availability": availability,
                "image": image,
            }
        )

    return books


def load_dataset() -> pd.DataFrame:
    """Load the scraped catalog from CSV if available, otherwise scrape a small sample."""
    try:
        df = pd.read_csv(DATASET_PATH)
        if not df.empty:
            return df
    except FileNotFoundError:
        pass

    sample = []
    for page in range(1, 4):
        url = BASE_URL.format(page)
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        sample.extend(parse_books_from_html(response.text, url))

    df = pd.DataFrame(sample)
    df.to_csv(DATASET_PATH, index=False)
    return df


BOOKS_DATA = load_dataset()


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/scrape/<int:page_number>")
def scrape_page(page_number):
    """
    Scrapes ONE page and returns it as JSON.
    The frontend calls this endpoint once per page, in a loop,
    so you can watch the table fill up live in the browser.
    """
    url = BASE_URL.format(page_number)
    response = requests.get(url, timeout=10)

    if response.status_code == 404:
        return jsonify({"done": True, "books": []})

    books = parse_books_from_html(response.text, url)
    return jsonify({"done": False, "books": books, "page": page_number})


@app.route("/api/stats")
def stats():
    total_books = len(BOOKS_DATA)
    avg_price = round(float(BOOKS_DATA["price_gbp"].mean()), 2)
    min_price = round(float(BOOKS_DATA["price_gbp"].min()), 2)
    max_price = round(float(BOOKS_DATA["price_gbp"].max()), 2)
    return jsonify(
        {
            "total_books": total_books,
            "avg_price": avg_price,
            "min_price": min_price,
            "max_price": max_price,
        }
    )


@app.route("/api/search")
def search():
    query = (request.args.get("q", "") or "").strip().lower()
    data = BOOKS_DATA.copy()

    if query:
        filtered = data[
            data["title"].str.lower().str.contains(query, na=False)
            | data["availability"].str.lower().str.contains(query, na=False)
        ]
        data = filtered

    if data.empty:
        return jsonify({"count": 0, "results": []})

    results = data.head(24).to_dict(orient="records")
    return jsonify({"count": len(results), "results": results})


if __name__ == "__main__":
    app.run(debug=True)
