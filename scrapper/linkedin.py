import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from bs4 import BeautifulSoup
import re

class LinkedInScraper:
    def __init__(self, email, password, search_key="data_analyst", pages=2):
        self.email = email
        self.password = password
        self.search_key = search_key
        self.pages = pages
        self.data = []
        self.driver = None

    def setup_driver(self):
        chromedriver_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'chromedriver'))
        options = webdriver.ChromeOptions()
        service = Service(chromedriver_path)
        self.driver = webdriver.Chrome(options=options, service=service)

    def login(self):
        self.driver.get("https://www.linkedin.com/login")
        self.driver.find_element(By.ID, "username").send_keys(self.email)
        self.driver.find_element(By.ID, "password").send_keys(self.password)
        self.driver.find_element(By.XPATH, "//*[@type='submit']").click()
        time.sleep(3)  # Wait for the login process to complete

        # Handle 2FA
        try:
            two_fa_form = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.ID, "two-step-challenge"))
            )
            if two_fa_form:
                print("2FA page loaded. Please enter the 2FA code on the LinkedIn page.")
                while True:
                    input("Press Enter after you have entered the 2FA code and clicked Submit on the LinkedIn page...")
                    if ("challenge" not in self.driver.current_url or
                            "feed" in self.driver.current_url or "search/results" in self.driver.current_url):
                        print("2FA verification successful.")
                        break
                    else:
                        print("2FA verification not completed yet. Please complete the 2FA verification on the LinkedIn page.")
        except:
            print("No 2FA page detected, proceeding with login.")

        # Check if login was successful
        if "feed" in self.driver.current_url:
            return True
        return False

    def get_search_data(self):
        for no in range(1, self.pages + 1):
            start = "&page={}".format(no)
            search_url = f"https://www.linkedin.com/search/results/people/?keywords={self.search_key}&origin=SUGGESTION{start}"
            self.driver.get(search_url)
            self.driver.maximize_window()
            time.sleep(5)  # Ensure the page loads completely

            for scroll in range(2):
                self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(2)

            search = BeautifulSoup(self.driver.page_source, 'html.parser')
            peoples = search.find_all('li', class_='reusable-search__result-container')
            print(f"Going to scrape Page {no} data")

            for people in peoples:
                try:
                    profile_url = people.find('a', class_='app-aware-link')['href'].split('?')[0]
                except Exception as e:
                    print("Profile URL Error:", e)
                    profile_url = None

                try:
                    name = people.find('span', class_='entity-result__title-text').get_text(strip=True)
                    name = name.split('View ')[0].strip()
                except Exception as e:
                    print("Name Error:", e)
                    name = 'None'

                try:
                    connection_degree = people.find('span', class_='entity-result__badge-text').get_text(strip=True)
                    connection_degree = connection_degree.split('• ')[1].strip()[3::]
                except Exception as e:
                    print("Connection Degree Error:", e)
                    connection_degree = 'None'

                try:
                    location = people.find('div', class_='entity-result__secondary-subtitle').get_text(strip=True)
                except Exception as e:
                    print("Location Error:", e)
                    location = 'None'

                try:
                    title = people.find('div', class_='entity-result__primary-subtitle').get_text(strip=True)
                except Exception as e:
                    print("Title Error:", e)
                    title = 'None'

                self.data.append({
                    'profile_url': profile_url,
                    'name': name,
                    'connection_degree': connection_degree,
                    'location': location,
                    'title': title
                })
                print(f"Scraped data: {self.data[-1]}")
            print(f"Data scraped from page {no}")

    def get_email_data(self, profiles):
        email_data = {}
        for profile in profiles:
            profile_url = profile['profile_url'] + "/overlay/contact-info/"
            self.driver.get(profile_url)
            time.sleep(3)  # Allow time for the page to load

            sc = BeautifulSoup(self.driver.page_source, 'lxml')
            emails_found = self.extract_emails(sc)
            email_data[profile['profile_url']] = emails_found[0] if emails_found else 'Not Available'
        return email_data

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

    def run(self):
        self.setup_driver()
        if self.login():
            print("Login successful")
            self.get_search_data()
            email_data = self.get_email_data(self.data)
            self.driver.quit()
            return self.data, email_data
        else:
            print("Login failed")
            self.driver.quit()
            return None, None
