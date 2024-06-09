from event_register.linkedin import LinkedInScraper
import xlsxwriter
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Get environment variables
email = os.getenv('EMAIL')
password = os.getenv('PASSWORD')
search_query = os.getenv('SEARCH_QUERY')
pages = int(os.getenv('PAGES'))

# Example usage:
if __name__ == "__main__":
    scraper = LinkedInScraper(email, password, search_query, pages)
    scraper.run()
    print("Data compiled successfully")
