# CodeAlpha Data Analytics Internship — Task 1: Web Scraping

## Overview
This project scrapes book data (title, price, star rating, availability) from
[books.toscrape.com](https://books.toscrape.com), a website built specifically
for scraping practice. It handles pagination across multiple pages and saves
the collected data into a clean CSV file.

## Objectives (as required by CodeAlpha)
- Use Python libraries (BeautifulSoup) to extract data from websites
- Identify and collect relevant datasets from public web pages
- Handle HTML structure and web navigation to gather accurate data
- Create a custom dataset tailored to specific analysis needs

## Tech Stack
- Python 3
- `requests` — to fetch web pages
- `BeautifulSoup` (`bs4`) — to parse HTML
- `pandas` — to structure and export the data

## How to Run
1. Clone this repo:
   ```
   git clone https://github.com/<your-username>/CodeAlpha_WebScraping.git
   cd CodeAlpha_WebScraping
   ```
2. (Optional but recommended) Create a virtual environment:
   ```
   python -m venv venv
   venv\Scripts\activate      # Windows
   source venv/bin/activate   # Mac/Linux
   ```
3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
4. Run the scraper:
   ```
   python scraper.py
   ```
5. Output: a `books_dataset.csv` file will be generated in the project folder.

## Output
The scraper produces a CSV with the following columns:

| Column | Description |
|---|---|
| title | Book title |
| price_gbp | Price in GBP |
| rating_out_of_5 | Star rating (1–5) |
| availability | Stock status |

## Author
Internship: CodeAlpha Data Analytics Internship
Task: Task 1 — Web Scraping
