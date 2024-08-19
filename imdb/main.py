import json

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from tqdm import tqdm


def initialize_driver(chrome_driver_path):
    """Initialize and return a headless Chrome WebDriver."""
    service = Service(executable_path=chrome_driver_path)
    options = Options()
    options.add_argument('--headless')
    user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.6533.120 Safari/537.36"
    options.add_argument(f"user-agent={user_agent}")
    service.start()
    driver = webdriver.Chrome(service=service, options=options)
    return driver


def fetch_data(url, driver):
    """Fetch and parse data from the given URL using the provided driver."""
    driver.get(url)
    driver.implicitly_wait(10)  # Wait for the page to load
    soup = BeautifulSoup(driver.page_source, "html.parser")
    driver.quit()
    return soup


def parse_movies_or_tv_shows(soup):
    """Parse the movies or TV shows from the BeautifulSoup object."""
    items = []
    item_elements = soup.find_all("li", class_="ipc-metadata-list-summary-item")
    
    with tqdm(total=len(item_elements), desc="IMDB Scraping", unit="item", ncols=100) as progress_bar:
        for item_element in item_elements:
            try:
                poster = item_element.find("img", class_="ipc-image")['src']
                title = item_element.find('a', class_="ipc-title-link-wrapper").text.split(". ", 1)[-1]

                meta_data_div = item_element.find('div', class_="sc-b189961a-7 btCcOY cli-title-metadata")
                meta_data = [span.text for span in meta_data_div.find_all('span', class_="sc-b189961a-8 hCbzGp cli-title-metadata-item")][:-1] if meta_data_div else []

                year = meta_data[0] if len(meta_data) > 0 else None
                duration = meta_data[1] if len(meta_data) > 1 else None

                rating = item_element.find("span", class_="ipc-rating-star--rating").text
                vote = item_element.find("span", class_="ipc-rating-star--voteCount").text.replace("(", "").replace(")", "").strip()

                items.append({
                    'poster': poster,
                    'title': title,
                    'year': year,
                    'duration': duration,
                    'rating': rating,
                    'vote': vote
                })
            except AttributeError as e:
                print(f"Error parsing item: {e}")
            
            progress_bar.update(1)
    
    return items


def save_to_file(filename, data):
    """Save the data to a JSON file."""
    with open(filename, "w") as file:
        json.dump(data, file, indent=4)


def main():
    chrome_driver_path = r"path/to/chromedriver"
    movie_url = 'https://www.imdb.com/chart/top/?ref_=nv_mv_250'
    tv_show_url = 'https://www.imdb.com/chart/toptv/?ref_=nv_tvv_250'

    driver = initialize_driver(chrome_driver_path)
    
    movie_soup = fetch_data(movie_url, driver)
    tv_show_soup = fetch_data(tv_show_url, driver)

    top_250_movies = parse_movies_or_tv_shows(movie_soup)
    top_250_tv_shows = parse_movies_or_tv_shows(tv_show_soup)

    save_to_file("top_250_movies.json", top_250_movies)
    save_to_file("top_250_tv_shows.json", top_250_tv_shows)

    print("Data has been saved to top_250_movies.json")
    print("Data has been saved to top_250_tv_shows.json")


if __name__ == "__main__":
    main()
