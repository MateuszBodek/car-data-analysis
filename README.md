# Car Data Analysis Project

A Python project for scraping and analyzing car technical specifications and user reviews from autocentrum.pl. The project includes web scraping capabilities, data cleaning, and database integration.

## Project Structure

```bash
├── src/
│ ├── data/					     # Scraped data storage
│    ├── car_technical_data/ 	 # JSON files with car specs
│    ├── car_model_links.txt 	 # URLs to car models
│    ├── car_ratings.txt 		 # User ratings data
│    └── cars.db                 # Cars database
│ ├── data_scripts/ 			 # Data processing scripts
│    ├── database.py			 # Database loading scripts
│    └── preliminary_ed.ipynb 	 # Data exploration notebook
│ └── scraper/ 				     # Web scraping modules
│ 	 ├── links_scraper.py		 # Car model URLs scraper
│ 	 ├── tech_data_scraper.py 	 # Technical specs scraper
│ 	 └── review_data_scraper.py  # User reviews scraper
└── main.py 					 # Main execution script
```

## Features

- Scrapes comprehensive car technical specifications
- Collects user ratings and reviews
- Handles data cleaning and preprocessing
- Stores data in structured JSON and CSV formats
- Database integration for cleaned data

## Usage

1. Install requirements:

```bash
pip install -r requirements.txt
```

2. Run the main script to collect data:

```bash
python main.py
```

python main.py

3. Use Jupyter notebook `preliminary_ed.ipynb` for data exploration and cleaning

## Data Sources

The project scrapes data from autocentrum.pl including:

* Technical specifications for different car models
* User ratings across multiple categories
* Car model information and generations

Clean data is saved into a database located in the folder data.

## Note

This project is for educational purposes. Please respect the website's robots.txt and implement appropriate delays between requests when scraping data.
