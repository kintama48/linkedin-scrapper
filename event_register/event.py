import time

from selenium.webdriver.common.by import By


class Event:
    def __init__(self, name, meeting_url="", organizer="", date="", time=""):
        self.meeting_url = meeting_url
        self.name = name
        self.organizer = organizer
        self.date = date
        self.time = time

    def __str__(self):
        return (f"Event: {self.name}, Organizer: {self.organizer}, Date: {self.date}, Time: {self.time},"
                f" Meeting URL: {self.meeting_url}")

    def get_event_details(self):
        return {
            'meeting_url': self.meeting_url,
            'name': self.name,
            'organizer': self.organizer,
            'date': self.date,
            'time': self.time
        }

    def set_event_details(self, meeting_url, name, organizer, date, time):
        self.meeting_url = meeting_url
        self.name = name
        self.organizer = organizer
        self.date = date
        self.time = time

    @classmethod
    def from_webpage(cls, driver):
        try:
            event_name = driver.find_element(By.XPATH, "//h1").text
            event_datetime = driver.find_element(By.XPATH,
                                                 "//div[@class='events-live-top-card__status-feedback--bold "
                                                 "artdeco-inline-feedback artdeco-inline-feedback--yield "
                                                 "ember-view']//span").text
            event_organizer = driver.find_element(By.XPATH, "//span[@class='t-16 t-black t-normal pr1']//a").text
            event_joining_link = driver.current_url

            date, time = event_datetime.split(',')[1].strip(), event_datetime.split(',')[2].strip()

            return cls(
                name=event_name,
                meeting_url=event_joining_link,
                organizer=event_organizer,
                date=date,
                time=time
            )
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
                time.sleep(3)  # Wait to see the feedback
                print(f"Clicked 'Attend' button for event: {self.name}")
            except:
                print("No 'Register' or 'Attend' button found for event: {self.name}")

    def complete_registration(self, driver):
        try:
            submit_button = driver.find_element(By.XPATH, "//button[contains(text(), 'Submit')]")
            submit_button.click()
            time.sleep(3)  # Wait to see the feedback
            print(f"Clicked 'Submit' button to complete registration for event: {self.name}")
        except:
            print("No 'Submit' button found to complete registration for event: {self.name}")
