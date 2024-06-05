# Linked-In Search/Email Scrapper
This scrapper uses Selenium and BS4 to visit a LinkedIn search page and scrape the emails of the profiles that appear in the search results. The scrapper is able to scrape the emails of the profiles that appear in the page of the search results. This scrapper is also able to capture the emails of the scrapped user data.


## Disclaimer
This script is repurposed from the following 2 repositories:

- [LinkedIn-Search-Scraper](https://github.com/info3g/linkedin-scrapper)
- [LinkedIn-Email-Scraper](https://github.com/sercanerhan/Linkedin-Email-Scrapper)

## Installation
1. Clone the repository
2. Install the required packages using the following command:
```bash
pip install -r requirements.txt
```
3. Download the Chrome WebDriver from [here](https://chromedriver.chromium.org/downloads) and place it in the root directory of the project.
4. Create a `.env` file in the root directory of the project and add the following variables:
```bash
EMAIL=<YOUR_EMAIL>
PASSWORD=<YOUR_PASSWORD>

# Change the following variables according to your requirements
SEARCH_QUERY="Backend Developer"
PAGES=2
```
5. Run the script using the following command:
```bash
python3 main.py
```

