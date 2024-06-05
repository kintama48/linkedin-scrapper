import os

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
import time
import re
from bs4 import BeautifulSoup


class LinkedIn:

    def __init__(self, email, password):
        self.email = email
        self.password = password
        self.driver = None

    def setup_driver(self):
        # Get the absolute path of chromedriver
        chromedriver_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'chromedriver'))
        options = webdriver.ChromeOptions()
        # options.add_argument("--headless")  # Uncomment to run in headless mode
        service = Service(chromedriver_path)
        self.driver = webdriver.Chrome(options=options, service=service)

    def login(self):
        self.driver.get("https://www.linkedin.com/login")
        self.driver.find_element(By.ID, "username").send_keys(self.email)
        self.driver.find_element(By.ID, "password").send_keys(self.password)
        self.driver.find_element(By.XPATH, "//*[@type='submit']").click()
        time.sleep(3)  # Wait for the login process to complete

        # Check if login was successful
        if "feed" in self.driver.current_url:
            return True
        return False

    def bulk_scan(self, profiles):
        all_emails = []
        for profile in profiles:
            profile = profile + "/overlay/contact-info/"
            self.driver.get(profile)
            time.sleep(3)  # Allow time for the page to load

            sc = BeautifulSoup(self.driver.page_source, 'lxml')
            emails_found = self.extract_emails(sc)
            all_emails.extend(emails_found)
        return all_emails

    def single_scan(self, profile):
        profile = profile + "/overlay/contact-info/"
        self.driver.get(profile)
        time.sleep(3)  # Allow time for the page to load

        sc = BeautifulSoup(self.driver.page_source, 'lxml')
        emails_found = self.extract_emails(sc)
        return emails_found

    @staticmethod
    def extract_emails(soup):
        emails = []
        contact_info_section = soup.find('div', class_='artdeco-modal__content')
        if contact_info_section:
            email_section = contact_info_section.find('a', href=True, text=re.compile(r'@'))
            if email_section:
                email = email_section.get('href').replace('mailto:', '')
                emails.append(email)
        return emails

    def quit_driver(self):
        if self.driver:
            self.driver.quit()
