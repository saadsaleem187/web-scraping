import json
import requests

from bs4 import BeautifulSoup
from tqdm import tqdm


def fetch_books(page_number):
    url = f"https://books.toscrape.com/catalogue/page-{page_number}.html"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    books = []
    book_elements = soup.find_all('article', class_="product_pod")

    for book in book_elements:
        title = book.find('h3').find('a')['title']
        price = book.find('p', class_="price_color").text
        stock = 'In stock' if 'In stock' in book.find('p', class_="instock availability").text else 'Out Of Stock'
        rating = book.find('p', class_='star-rating')['class'][1]
        link = book.find('h3').find('a')['href']

        books.append({
            'title': title,
            'price': price,
            'stock': stock,
            'rating': rating,
            'link': f"https://books.toscrape.com/catalogue/{link}"
        })

    return books


def main():
    all_books = []
    max_pages = 10
    current_page = 1

    # Initialize progress bar for page scraping
    with tqdm(total=max_pages, desc="Books Scraping", unit="page", ncols=100) as progress_bar:
        while (current_page <= max_pages):
            books_on_page = fetch_books(current_page)
            all_books.extend(books_on_page)

            with open('books.json', 'w') as f:
                json.dump(all_books, f, indent=4)
            
            current_page += 1

            progress_bar.update(1)

    print('Data is saved to books.json')


if __name__ == "__main__":
    main()
