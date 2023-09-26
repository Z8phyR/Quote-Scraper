"""
This script scrapes quotes from the website "http://quotes.toscrape.com" and saves them to a JSON file.
It uses the requests and BeautifulSoup libraries to scrape the website and extract the quotes and authors.
The scraped data is stored in a list of dictionaries, where each dictionary contains the quote and author.
The script then saves the list of dictionaries to a JSON file named "quotes.json".
"""
import requests
from bs4 import BeautifulSoup
import time
import json

BASE_URL = "http://quotes.toscrape.com"
URL = BASE_URL
pages_scraped = 0
MAX_PAGES = 3

all_quotes = []

while URL and pages_scraped < MAX_PAGES:
    response = requests.get(URL)

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        quotes_divs = soup.find_all('div', class_='quote')

        for quote_div in quotes_divs:
            quote_text = quote_div.find('span', class_='text').text
            author_name = quote_div.find('small', class_='author').text
            all_quotes.append({
                'quote': quote_text,
                'author': author_name
            })

        # Check for the next page
        next_link = soup.find('li', class_='next')

        if next_link:
            next_page = next_link.find('a')['href']
            # Construct the full URL
            URL = BASE_URL + next_page
        else:
            URL = None

        # Increase the pages_scraped counter
        pages_scraped += 1

        # Politeness delay
        time.sleep(2)

    else:
        print("Failed to retrieve the webpage.")
        URL = None

# Save the quotes to a JSON file
with open('quotes.json', 'w') as file:
    json.dump(all_quotes, file, indent=4)
