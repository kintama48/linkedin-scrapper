from event_register.linkedin import LinkedInScraper
import xlsxwriter
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Get environment variables
email = os.getenv('EMAIL')
password = os.getenv('PASSWORD')
pages = int(os.getenv('PAGES'))
auto_restart_time = os.getenv('AUTO_RESTART_TIME')

if __name__ == "__main__":
    scraper = LinkedInScraper(email, password, pages=pages, auto_restart_time=auto_restart_time)
    scraper.autostart()
    print("Data compiled successfully")
