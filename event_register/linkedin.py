import os
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import pandas as pd


class Event:
    def __init__(self, name):
        self.name = name

    @staticmethod
    def from_webpage(driver):
        try:
            event_name = driver.find_element(By.XPATH, "//h1").text
            return Event(event_name)
        except Exception as e:
            print(f"Error extracting event details: {e}")
            return None

    def register_or_attend(self, driver):
        try:
            register_button = driver.find_element(By.XPATH, "//button/span[text()='Register']/..")
            register_button.click()
            print(f"Clicked 'Register' button for event: {self.name}")
            self.complete_registration(driver)
        except:
            try:
                attend_button = driver.find_element(By.XPATH, "//button/span[text()='Attend']/..")
                attend_button.click()
                print(f"Clicked 'Attend' button for event: {self.name}")
                time.sleep(3)  # Wait to see the feedback
            except Exception as e:
                print(f"No 'Register' or 'Attend' button found for event: {self.name}, error: {e}")

    def complete_registration(self, driver):
        try:
            submit_button = driver.find_element(By.XPATH, "//button[contains(text(), 'Submit')]")
            submit_button.click()
            time.sleep(3)  # Wait to see the feedback
            print(f"Clicked 'Submit' button to complete registration for event: {self.name}")
        except:
            print(f"No 'Submit' button found to complete registration for event: {self.name}")

    def get_event_details(self):
        return {'Event Name': self.name}


class LinkedInScraper:
    def __init__(self, email, password, search_key="Devops", pages=100):
        self.email = email
        self.password = password
        self.search_key = search_key
        self.pages = pages
        self.driver = None
        self.event_links = []
        self.event_data = []

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
        self.handle_2fa()

        # Check if login was successful
        if "feed" in self.driver.current_url:
            return True
        return False

    def handle_2fa(self):
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
                        print(
                            "2FA verification not completed yet. Please complete the 2FA verification on the LinkedIn page.")
        except:
            print("No 2FA page detected, proceeding with login.")

    def get_event_data(self):
        search_url = f"https://www.linkedin.com/search/results/events/?keywords={self.search_key}&origin=SWITCH_SEARCH_VERTICAL"
        self.driver.get(search_url)
        self.driver.maximize_window()
        time.sleep(5)  # Ensure the page loads completely

        for no in range(1, self.pages + 1):
            print(f"Going to scrape Page {no} data")
            for scroll in range(2):
                self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(2)

            search = BeautifulSoup(self.driver.page_source, 'html.parser')
            events = search.find_all('li', class_='reusable-search__result-container')

            for event in events:
                self.collect_event_link(event)

            if not self.go_to_next_page(no):
                break

    def collect_event_link(self, event):
        try:
            event_link = event.find('a', class_='app-aware-link')['href']
            self.event_links.append(event_link)
        except Exception as e:
            print(f"Error collecting event link: {e}")

    def go_to_next_page(self, current_page):
        try:
            next_button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, '//button[contains(@aria-label, "Next")]'))
            )
            if next_button:
                print(f"Clicking next button for page {current_page + 1}")
                next_button.click()
                WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, f'//span[text()="{current_page + 1}"]'))
                )
                time.sleep(3)  # Ensure the page loads completely
                return True
            else:
                print("No more pages to scrape.")
                return False
        except Exception as e:
            print(f"Error clicking next button: {e}")
            return False

    def process_event_links(self):
        for event_link in self.event_links:
            self.driver.get(event_link)
            time.sleep(3)
            event = Event.from_webpage(self.driver)
            if event:
                event.register_or_attend(self.driver)
                self.event_data.append(event)

    def save_to_excel(self):
        event_details_list = [event.get_event_details() for event in self.event_data]
        df = pd.DataFrame(event_details_list)
        df.to_excel('linkedin_events.xlsx', index=False)
        print("Event data saved to 'linkedin_events.xlsx'")

    def run(self):
        self.setup_driver()
        if self.login():
            print("Login successful")
            self.get_event_data()
            self.process_event_links()
            self.save_to_excel()
            print("Registered events:", [event.name for event in self.event_data])
        else:
            print("Login failed")
        self.driver.quit()
