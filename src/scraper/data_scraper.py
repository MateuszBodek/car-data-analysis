import requests
from bs4 import BeautifulSoup
import re
import csv
from tqdm import tqdm

def scrape_car_data(url: str) -> list:
    '''Scrapes car data from the given URL and returns a list of user rating metrics.'''

    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    car = soup.find_all('div', class_=['value', 'rate-box-container', 'other-offers__text__price'])

    sigma = []
    for val in car:
        sigma.append(val.text)

    done = []
    found = []
    weird_bug_check = True

    for k in sigma:
        found.append(re.findall(r"(\d,\d{1,2}|\d\d%)", k))
        price_match = re.findall(r"(\d+)(?:\xa0|\s)(\d+)", k)
        if price_match:
            done.append(int(''.join(*price_match)))

    if len(done) == 0:
        done.append(None)

    for val in found:
        if val:
            val = val[0]
            if val[-1] == '%':
                val = float(val[:-1])
                val = val / 100
                done.append(val)
                weird_bug_check = False
            else:
                done.append(float(val.replace(',', '.')))

    done = done[:17]
    if weird_bug_check:
        done.insert(2, None)

    done.insert(0, url.split('oceny/')[1].replace('/', ' ').strip())
    return done


def load_links(file_path: str) -> list:
    '''Loads car model links from a text file and returns them as a list.'''

    with open (file_path, 'r', encoding='utf-8') as file:
        return [line.strip() for line in file.readlines()]


def scrape_and_save_ratings(path: str, filename: str, links: list, limit: int|None = None) -> None:
    ''''Scrapes car data from the provided links and saves it to a CSV file.'''
    with open(path + filename, 'a', newline='') as myfile:
        wr = csv.writer(myfile, delimiter=';')
        i = 0
        for link in tqdm(links[:limit] if limit else links):
            wr.writerow(scrape_car_data(link))
            i += 1
        print(f'Scraped data for {i} cars and saved to {filename}.txt')

