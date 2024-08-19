import json
import requests

from bs4 import BeautifulSoup
from tqdm import tqdm


def fetch_quotes(page_number):
    """Fetches quotes from a specific page number on the quotes.toscrape website."""
    url = f"http://quotes.toscrape.com/page/{page_number}/"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    quotes = []
    quotes_elements = soup.find_all('div', class_="quote")

    for quote_element in quotes_elements:
        quote = quote_element.find('span', class_="text").text
        author = quote_element.find('small', class_="author").text
        tags = quote_element.find('meta', class_="keywords")['content']

        tag_element = quote_element.find('a', class_="tag")
        tag_link = f"http://quotes.toscrape.com/{tag_element['href']}" if tag_element else None
        
        quotes.append({
            'quote': quote,
            'author': author,
            'tags': tags,
            'tag_links': tag_link
        })

    return quotes


def main():
    all_quotes = []
    max_page = 10
    current_page = 1

    # Initialize progress bar for page scraping
    with tqdm(total=max_page, desc="Quotes Scraping", unit="page", ncols=100) as progress_bar:
        while current_page <= max_page:
            quotes_on_page = fetch_quotes(current_page)
            all_quotes.extend(quotes_on_page)

            with open('quotes.json', 'w') as f:
                json.dump(all_quotes, f, indent=4)
            
            current_page += 1

            progress_bar.update(1)
    
    print("Data has been saved to quotes.json")


if __name__ == "__main__":
    main()
