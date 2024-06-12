# LinkedIn Event Registration Automation

This scraper uses Selenium and BeautifulSoup (BS4) to visit a LinkedIn search page, scrape event links, and data, and then visit those events to attend or register for them. It is capable of navigating through multiple pages of search results, capturing event links, and compiling the event data into an Excel file. Additionally, it supports Two-Factor Authentication (2FA).

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

4. **Create a `.env` file in the root directory and add the following variables:**
   ```bash
   EMAIL=<YOUR_EMAIL>
   PASSWORD=<YOUR_PASSWORD>

   # Change the following variables according to your requirements
   SEARCH_QUERY="Devops"
   PAGES=100
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
   - Support Two-Factor Authentication (2FA) if enabled.
   - Perform a search based on the `SEARCH_QUERY` parameter.
   - Scrape event links and data from the search results pages.
   - Visit each event page to attend or register for the event.
   - Compile the data into an Excel file named `linkedin_events.xlsx`.

## Notes

- Make sure you have the latest version of Chrome installed.
- The script navigates LinkedIn pages and might be subject to LinkedIn's rate limiting or CAPTCHA mechanisms.
- Use this script responsibly and ensure compliance with LinkedIn's terms of service.

## Troubleshooting

If you encounter the following error:

```plaintext
selenium.common.exceptions.SessionNotCreatedException: Message: session not created: This version of ChromeDriver only supports Chrome version 125
Current browser version is 124.0.6367.91 with binary path /opt/google/chrome/chrome
```

This script supports Chrome versions 125. You can download the appropriate ChromeDriver from [here](https://developer.chrome.com/docs/chromedriver/downloads).

Ensure you have the correct version of Chrome and ChromeDriver installed.

If the script fails to click the "Next" button while paginating through search results, ensure that:
- The XPath used for the "Next" button is accurate.
- There is enough wait time for the button to become clickable.
- The page is fully loaded before attempting to click the button.

If issues persist, review the log messages for more details about the error and check the HTML structure of the LinkedIn search results page to ensure the XPath expressions are correct.

If the script encounters issues with attending or registering for events, ensure that:
- The XPath used for the "Register" or "Attend" button is accurate.
- There is enough wait time for the buttons to become clickable.
- The page is fully loaded before attempting to interact with the buttons.