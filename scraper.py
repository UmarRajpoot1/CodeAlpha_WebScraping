"""
CodeAlpha Data Analytics Internship - Task 1: Web Scraping
Author: <your name here>

What this script does:
- Scrapes book data (title, price, rating, availability) from
  https://books.toscrape.com — a website built specifically for
  scraping practice.
- Handles pagination (navigates across multiple pages automatically).
- Cleans and structures the data.
- Saves the final dataset to a CSV file (books_dataset.csv).

Libraries used: requests, BeautifulSoup (bs4), pandas
"""

import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

BASE_URL = "https://books.toscrape.com/catalogue/page-{}.html"

# Star ratings on the site are written as words in the CSS class name
RATING_MAP = {
    "One": 1,
    "Two": 2,
    "Three": 3,
    "Four": 4,
    "Five": 5,
}


def get_page_html(page_number: int) -> str:
    """Download the raw HTML for a given catalogue page number."""
    url = BASE_URL.format(page_number)
    response = requests.get(url, timeout=10)
    response.raise_for_status()  # stop early if the request failed
    return response.text


def parse_books_from_html(html: str) -> list[dict]:
    """Extract book details from one page's HTML."""
    soup = BeautifulSoup(html, "html.parser")
    books = []

    for article in soup.select("article.product_pod"):
        title = article.h3.a["title"]

        price_text = article.select_one("p.price_color").get_text(strip=True)
        price = float(price_text.replace("£", "").replace("Â", ""))

        rating_word = article.select_one("p.star-rating")["class"][1]
        rating = RATING_MAP.get(rating_word, None)

        availability = article.select_one("p.instock.availability").get_text(strip=True)

        books.append(
            {
                "title": title,
                "price_gbp": price,
                "rating_out_of_5": rating,
                "availability": availability,
            }
        )

    return books


def scrape_all_pages(max_pages: int = 5) -> pd.DataFrame:
    """
    Loop through multiple catalogue pages and combine the results
    into a single pandas DataFrame.
    """
    all_books = []

    for page in range(1, max_pages + 1):
        print(f"Scraping page {page}...")
        try:
            html = get_page_html(page)
        except requests.HTTPError:
            print(f"Page {page} not found — stopping (reached the last page).")
            break

        page_books = parse_books_from_html(html)
        all_books.extend(page_books)

        time.sleep(1)  # be a polite scraper, don't hammer the server

    return pd.DataFrame(all_books)


if __name__ == "__main__":
    df = scrape_all_pages(max_pages=5)  # change max_pages to scrape more/less
    print(f"\nScraped {len(df)} books total.")
    print(df.head())

    df.to_csv("books_dataset.csv", index=False)
    print("\nSaved dataset to books_dataset.csv")
