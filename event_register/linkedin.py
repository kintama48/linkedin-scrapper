import os
import random
import schedule
import pickle
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import pandas as pd
from dotenv import load_dotenv
from .event import Event
from .keywords import Keywords

# Load environment variables from .env file
load_dotenv()


class LinkedInScraper:
    def __init__(self, email, password, pages=100, auto_restart_time="08:00"):
        self.email = email
        self.password = password
        self.keywords = Keywords()
        self.pages = pages
        self.driver = None
        self.event_links = []
        self.event_data = []
        self.current_keyword = None
        self.cookies_file = 'cookies.pkl'
        self.auto_restart_time = auto_restart_time
        self.invited_users = set()

    def setup_driver(self):
        chromedriver_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'chromedriver' if os.getenv(
            'PLATFORM') == 'linux' else 'chromedriver.exe'))
        options = webdriver.ChromeOptions()
        service = Service(chromedriver_path)
        self.driver = webdriver.Chrome(options=options, service=service)

    def login(self):
        if os.path.exists(self.cookies_file):
            self.load_cookies()
            self.driver.get("https://www.linkedin.com/feed/")
            if "feed" in self.driver.current_url:
                print("Login successful using cookies")
                return True
            else:
                print("Cookies invalid, logging in again")
                os.remove(self.cookies_file)

        self.driver.get("https://www.linkedin.com/login")
        self.driver.find_element(By.ID, "username").send_keys(self.email)
        self.driver.find_element(By.ID, "password").send_keys(self.password)
        self.driver.find_element(By.XPATH, "//*[@type='submit']").click()
        time.sleep(3)  # Wait for the login process to complete

        # Handle 2FA
        self.handle_2fa()

        # Check if login was successful
        if "feed" in self.driver.current_url:
            self.save_cookies()
            return True
        return False

    def handle_2fa(self):
        try:
            print("2FA page loaded. Please perform 2FA.")
            while True:
                input("Press Enter after you have performed 2FA...")
                if ("challenge" not in self.driver.current_url or
                        "feed" in self.driver.current_url or "search/results" in self.driver.current_url):
                    print("2FA verification successful.")
                    break
                else:
                    print(
                        "2FA verification not completed yet. Please complete the 2FA verification on the LinkedIn page.")
        except:
            print("No 2FA page detected, proceeding with login.")

    def save_cookies(self):
        with open(self.cookies_file, 'wb') as file:
            pickle.dump(self.driver.get_cookies(), file)
        print("Cookies saved to 'cookies.pkl'")

    def load_cookies(self):
        self.driver.get("https://www.linkedin.com")
        with open(self.cookies_file, 'rb') as file:
            cookies = pickle.load(file)
            for cookie in cookies:
                self.driver.add_cookie(cookie)
        print("Cookies loaded from 'cookies.pkl'")

    def get_event_data(self):
        search_url = f"https://www.linkedin.com/search/results/events/?keywords={self.current_keyword}&origin=SWITCH_SEARCH_VERTICAL"
        self.driver.get(search_url)
        self.driver.maximize_window()
        time.sleep(5)  # Ensure the page loads completely

        for no in range(1, self.pages + 1):
            print(f"Going to scrape Page {no} data")
            for scroll in range(1):  # Scroll more times to ensure full page load
                self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(2)

            search = BeautifulSoup(self.driver.page_source, 'html.parser')
            events = search.find_all('li', class_='reusable-search__result-container')

            for event in events:
                self.collect_event_link(event)

            if not self.go_to_next_page(no):
                break

            if no % 50 == 0:
                self.random_pause()

    def collect_event_link(self, event):
        try:
            event_link = event.find('a', class_='app-aware-link')['href']
            self.event_links.append(event_link)
        except Exception as e:
            print(f"Error collecting event link: {e}")

    def go_to_next_page(self, current_page):
        try:
            # Scroll to the bottom of the page to ensure the "Next" button is visible
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)  # Wait for the scroll to complete and the elements to load

            next_button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, '//button[contains(@aria-label, "Next")]'))
            )
            print(f"Clicking next button for page {current_page + 1}")
            next_button.click()
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            return True
        except Exception as e:
            print(f"Error in WebDriverWait: {e}")
            return False

    def process_event_links(self):
        for event_link in self.event_links:
            self.driver.get(event_link)
            time.sleep(3)
            event = Event.from_webpage(self.driver)
            if event:
                # event.register_or_attend(self.driver)
                # event.follow_event_organizer(self.driver)
                event.share_event(self.driver)
                event.invite_users(self.driver, self.invited_users)
                # event.scrape_attendees(self.driver)
                self.event_data.append(event)
            if len(self.event_data) % 50 == 0:
                self.random_pause()

    def save_to_excel(self):
        event_details_list = [event.get_event_details() for event in self.event_data]
        df = pd.DataFrame(event_details_list)
        df.to_excel('linkedin_events.xlsx', index=False)
        print("Event data saved to 'linkedin_events.xlsx'")

    def random_pause(self):
        delay = random.randint(300, 600)  # Random delay between 5 to 10 minutes
        print(f"Pausing for {delay // 60} minutes")
        time.sleep(delay)

    def run(self):
        self.keywords.load_state()
        while True:
            self.current_keyword = self.keywords.get_next_keyword()
            if not self.current_keyword:
                break
            print(f"Processing keyword: {self.current_keyword}")
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
            self.keywords.save_state()

    def autostart(self):
        schedule.every().day.at(self.auto_restart_time).do(self.run)
        self.run()  # Start immediately
        while True:
            schedule.run_pending()
            time.sleep(60)
