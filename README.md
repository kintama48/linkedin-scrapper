# LinkedIn Search/Email Scraper

This scraper uses Selenium and BeautifulSoup (BS4) to visit a LinkedIn search page and scrape the emails of the profiles that appear in the search results. It is capable of capturing the emails of the profiles displayed in the search results and compiling the user data, including emails, into a single file.

## Disclaimer

This script is repurposed from the following repositories:

- [LinkedIn-Search-Scraper](https://github.com/info3g/linkedin-scrapper)
- [LinkedIn-Email-Scraper](https://github.com/sercanerhan/Linkedin-Email-Scrapper)

## Installation

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd <repository-directory>
   ```

2. **Install the required packages:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Download the Chrome WebDriver:**
   - Download from [here](https://chromedriver.chromium.org/downloads)
   - Place it in the root directory of the project.

5. **Create a `.env` file in the root directory and add the following variables:**
   ```bash
   EMAIL=<YOUR_EMAIL>
   PASSWORD=<YOUR_PASSWORD>

   # Change the following variables according to your requirements
   SEARCH_QUERY="Backend Developer"
   PAGES=2
   ```

5. **Run the script:**
   ```bash
   python3 main.py
   ```

## Usage

1. **Ensure that the `.env` file is correctly set up with your LinkedIn credentials and desired search parameters.**

2. **Execute the script using the command provided above.**

3. **The script will:**
   - Log in to LinkedIn using the provided credentials.
   - Perform a search based on the `SEARCH_QUERY` parameter.
   - Scrape profile information and emails from the search results pages.
   - Compile the data into an Excel file named `linkedin-compiled-data.xlsx`.

## Notes

- Make sure you have the latest version of Chrome installed.
- The script navigates LinkedIn pages and might be subject to LinkedIn's rate limiting or CAPTCHA mechanisms.
- Use this script responsibly and ensure compliance with LinkedIn's terms of service.
