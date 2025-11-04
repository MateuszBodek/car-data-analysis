from src.scraper.links_scraper import links_scraper
from src.scraper.data_scraper import scrape_and_save_ratings, load_links
from src.scraper.tech_data_scraper import scrape_and_save_tech_data, modify_url

def main():
    links = links_scraper(save_to_file=True, filename="car_model_links")
    print(f"Total links scraped: {len(links)}")

    links = load_links('src/data/car_model_links.txt')
    scrape_and_save_ratings('src/data/','car_ratings.txt', links[1794:1974])

    modify_tech_specs_url = modify_url('oceny', 'dane-techniczne')(load_links)
    tech_specs_urls = modify_tech_specs_url('src/data/car_model_links.txt')
    scrape_and_save_tech_data('src/data/car_technical_data/', 'car_technical_data', tech_specs_urls[1155:])



if __name__ == "__main__":
    main()