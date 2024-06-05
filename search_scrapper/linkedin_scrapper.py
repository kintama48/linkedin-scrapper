import os

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import time
from bs4 import BeautifulSoup
import xlsxwriter


class Linkedin():
    def __init__(self, email, password, search_key="data_analyst",
                 pages=2):
        self.search_key = search_key  # Enter your Search key here to find people
        self.email = email
        self.password = password
        self.pages = pages
        self.data = []

    def get_data(self):
        # Set up Chrome options
        options = webdriver.ChromeOptions()
        chromedriver_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'chromedriver'))
        service = Service(chromedriver_path)
        driver = webdriver.Chrome(options=options, service=service)

        driver.get('https://www.linkedin.com/login')
        driver.find_element(By.ID, 'username').send_keys(self.email)  # Enter username of LinkedIn account here
        driver.find_element(By.ID, 'password').send_keys(self.password)  # Enter Password of LinkedIn account here
        driver.find_element(By.XPATH, "//*[@type='submit']").click()


        for no in range(1, self.pages + 1):
            start = "&page={}".format(no)
            search_url = "https://www.linkedin.com/search/results/people/?keywords={}&origin=SUGGESTION{}".format(
                self.search_key, start)
            driver.get(search_url)
            driver.maximize_window()
            time.sleep(5)  # Ensure the page loads completely

            for scroll in range(2):
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(2)

            search = BeautifulSoup(driver.page_source, 'html.parser')
            peoples = search.find_all('li', class_='reusable-search__result-container')
            print("Going to scrape Page {} data".format(no))

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
            print("data: ", self.data)
            print(f"!!!!!! Data scraped from page {no} !!!!!!")
        driver.quit()

    def write_data(self):
        workbook = xlsxwriter.Workbook("linkedin-search-data.xlsx")
        worksheet = workbook.add_worksheet('Peoples')
        bold = workbook.add_format({'bold': True})
        worksheet.write(0, 0, 'profile_url', bold)
        worksheet.write(0, 1, 'name', bold)
        worksheet.write(0, 2, 'connection_degree', bold)
        worksheet.write(0, 3, 'location', bold)
        worksheet.write(0, 4, 'title', bold)

        for i in range(1, len(self.data) + 1):
            worksheet.write(i, 0, self.data[i - 1]['profile_url'])
            worksheet.write(i, 1, self.data[i - 1]['name'])
            worksheet.write(i, 2, self.data[i - 1]['connection_degree'])
            worksheet.write(i, 3, self.data[i - 1]['location'])
            worksheet.write(i, 4, self.data[i - 1]['title'])

        workbook.close()

    def start(self):
        self.get_data()
        self.write_data()
