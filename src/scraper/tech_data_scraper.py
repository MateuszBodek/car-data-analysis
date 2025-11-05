"""Functions for scraping technical car data from autocentrum.pl and saving it to JSON files."""

import re
import os
import requests
import json
from bs4 import BeautifulSoup
from tqdm import tqdm


def modify_url(old, new):
    """Modifies URLs by replacing a specified substring with a new substring."""
    def modify_url(func):
        def inner(file_path: str) -> list:
            links_old = func(file_path)
            links_new = [link.replace(old, new) for link in links_old]
            return links_new
        return inner
    return modify_url


def scrape_car_tech_specs(url: str) -> list:
    """Scrapes technical specifications of every variant of a car from the provided URL."""

    headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0 Safari/537.36'
    }

    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')

    versions_listed = soup.find_all('a', class_='car-selector-box') # find all versions of the car

    versions = ['https://www.autocentrum.pl/' + ver['href'] for ver in versions_listed]

    # If no versions found, use the original URL
    if not versions:
        versions.append(url)
    
    # Scrape engine links from each version
    for ver in versions:
        response = requests.get(ver, headers=headers)
        soup = BeautifulSoup(response.content, 'html.parser')
        engines_listed = soup.find_all('a', class_=['engine-link pb', 'engine-link on', 'engine-link el', 'engine-link hyb', 'engine-link plugin'])
        engines = ['https://www.autocentrum.pl/' + eng['href'] for eng in engines_listed]

    technical_data = []

    # Scrape technical specs from each engine link
    for engine in engines:
        response = requests.get(engine, headers=headers)
        soup = BeautifulSoup(response.content, 'html.parser')
        numbers = [engine.split('dane-techniczne/')[1].replace('/', ' ').strip()]

        tech_numbers_listed = soup.find_all('span', class_='dt-param-value') # Find all technical data
        tech_descr_listed = soup.find_all('div', class_='dt-row__text__content') # Find all technical data labels

        descr_list = ['Model']
        for descr in tech_descr_listed:
            descr_list.append(descr.get_text(strip=True))

        # Clean numerical data from unit names
        for num in tech_numbers_listed:
            cleaned = re.sub(r'(?:\xa0mm| mm|\xa0l|\xa0cm³|\xa0km/h|\xa0s|\xa0l/100km|\xa0km|\xa0kg)$', '', num.get_text(strip=True))
            numbers.append(cleaned)

        # Create a dictionary mapping descriptions to their corresponding values, clean None or empty entries
        result = dict(zip(descr_list, numbers))
        result_cleaned = {k: v for k, v in result.items() if v not in ("", None)} 
        
        technical_data.append(result_cleaned)

    return technical_data


def scrape_and_save_tech_data(path: str, filename: str, links: list, limit: int | None = None) -> None:
    """
    Scrapes technical car data from the provided links and saves it to a valid JSON file.
    The file is updated after each link, so progress is never lost.
    """

    full_path = os.path.join(path, filename + '.json')
    counter = 0
    file_number = 1

    # Try to load existing data (if file exists and is valid JSON)
    if os.path.exists(full_path):
        try:
            with open(full_path, "r", encoding="utf-8") as f:
                all_rows = json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            print("Existing file is invalid or empty, starting fresh.")
            all_rows = []
    else:
        all_rows = []

    # Scrape and save after each link, log errors and links for later review
    for link in tqdm(links[:limit] if limit else links):
        file_lenght = len(all_rows)
        if file_lenght > 1500:
            all_rows = []
            print("File exceeded 500 entries, starting fresh")
            file_number += 1
            full_path = os.path.join(path, filename + f'_{file_number}.json')

        try:
            for row in scrape_car_tech_specs(link):
                all_rows.append(row)
                counter += 1
        except Exception as e:
            print(f" Error scraping {link}: {e}")
            with open(path + "scraping_errors_log.txt", "a", encoding="utf-8") as log_file:
                log_file.write(f"Error scraping {link}: {e}\n")
            continue

        with open(full_path, "w", encoding="utf-8") as f:
            json.dump(all_rows, f, indent=4, ensure_ascii=False)

    print(f"Scraped and saved {counter} car specs to {file_number} files")
