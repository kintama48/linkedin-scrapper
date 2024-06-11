import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class Event:
    def __init__(self, name, datetime=None, organizer=None, meeting_url=None, no_of_attendees=None):
        self.name = name
        self.datetime = datetime
        self.organizer = organizer
        self.meeting_url = meeting_url
        self.no_of_attendees = no_of_attendees

    @staticmethod
    def from_webpage(driver):
        try:
            event_name = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//h1"))).text
            event_datetime = driver.find_element(By.XPATH,
                                                 '//*[@id="events-top-card"]/div[1]/div[2]/div/div[1]/div[1]/div[2]/div/span').text
            event_organizer = driver.find_element(By.XPATH,
                                                  '//*[@id="events-top-card"]/div[1]/div[2]/div/div[1]/div[1]/div[1]/span/a').text
            try:
                meeting_url = (driver.find_element(By.XPATH,
                                                   '//*[@id="events-top-card"]/div[1]/div[2]/div/div[1]/div[1]/div[4]')
                               .get_attribute("href"))
            except:
                meeting_url = None
            try:
                no_of_attendees = driver.find_element(By.XPATH,
                                                      '//*[@id="events-top-card"]/div[1]/div[2]/div/div[1]/div[1]/div[5]/div/div/div').text
            except:
                no_of_attendees = None
            return Event(event_name, event_datetime, event_organizer, meeting_url, no_of_attendees)
        except Exception as e:
            print(f"Error extracting event details: {e}")
            return None

    def register_or_attend(self, driver):
        try:
            # Try to click the Register button if present
            register_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, '//*[@id="ember1768"]'))
            )
            register_button.click()
            print(f"Clicked 'Register' button for event: {self.name}")
            self.complete_registration(driver)
        except Exception as e:
            print(f"Register button not found for event: {self.name}. Trying 'Attend' button. Error: {e}")
            try:
                # If Register button is not found, try to click the Attend button
                attend_button = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, '//*[@id="ember1607"]'))
                )
                attend_button.click()
                print(f"Clicked 'Attend' button for event: {self.name}")
                time.sleep(5)  # Wait to see the feedback
            except Exception as e:
                print(f"No 'Register' or 'Attend' button found for event: {self.name}, error: {e}")

    def complete_registration(self, driver):
        try:
            submit_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, '//*[@id="ember1826"]/button'))
            )
            submit_button.click()
            time.sleep(5)  # Wait to see the feedback
            print(f"Clicked 'Submit' button to complete registration for event: {self.name}")
        except Exception as e:
            print(f"No 'Submit' button found to complete registration for event: {self.name}. Error: {e}")

    def get_event_details(self):
        return {
            'Event Name': self.name,
            'Event Date': self.datetime,
            'Organizer': self.organizer,
            'Meeting URL': self.meeting_url,
            'Number of Attendees': self.no_of_attendees
        }
