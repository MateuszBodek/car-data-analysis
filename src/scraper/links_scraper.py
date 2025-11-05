"""Functions for scraping all car model links from autocentrum.pl and optionally saings them to a text file."""

import requests
from bs4 import BeautifulSoup
from typing import List
from tqdm import tqdm
import os


def links_scraper(save_to_file: bool = False, filename: str = "car_model_links") -> List:
    base_url = 'https://www.autocentrum.pl'

    headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0 Safari/537.36'
    }
    response = requests.get(base_url + '/oceny/', headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')

    # get all make names
    makes = soup.find_all('a', class_='make')
    models_links = []

    # get all model links
    for make in tqdm(makes):
        response_models = requests.get(base_url + make['href'], headers=headers)
        soup_models = BeautifulSoup(response_models.content, 'html.parser')
        models = soup_models.find_all('a', class_=['photo-loader big-box',
                                                    'photo-loader big-box other-model not-activated'])

        # get all generations for each model
        for model in models:
            try: 
                response_gens = requests.get(base_url + model['href'])
                soup_gens = BeautifulSoup(response_gens.content, 'html.parser')
                generations = soup_gens.find_all('a', class_='car-selector-box')

                for gen in generations:
                    models_links.append(gen['href'])
            except:
                models_links.append(model['href'])
        
    if save_to_file: # Save links to a text file in data directory
        data_dir = "src/data/"
        file_path = os.path.join(data_dir, filename + '.txt')
        
        with open(file_path, 'w', encoding='utf-8') as links_file:
            for link in models_links:
                links_file.write(base_url + link + '\n')

    return models_links
