import os
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class Event:
    def __init__(self, name, datetime=None, organizer=None, meeting_url=None, no_of_attendees=None, id=None):
        self.id = None
        self.name = name
        self.datetime = datetime
        self.organizer = organizer
        self.meeting_url = meeting_url
        self.no_of_attendees = no_of_attendees


    @staticmethod
    def from_webpage(driver):
        try:
            event_name = WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.XPATH, "//h1"))).text
            try:
                event_datetime = driver.find_element(By.XPATH,
                                                     '//*[@id="events-top-card"]/div[1]/div[2]/div/div[1]/div[1]/div['
                                                     '2]/div/span').text
            except Exception as e:
                event_datetime = None
                print(e.__str__())

            try:
                event_organizer = driver.find_element(By.XPATH,
                                                      '//*[@id="events-top-card"]/div[1]/div[2]/div/div[1]/div['
                                                      '1]/div[1]/span/a').text
            except Exception as e:
                event_organizer = None
                print(e.__str__())
            try:
                meeting_url = (driver.find_element(By.XPATH,
                                                   '//a[contains(@class, "events-live-top-card__external-url")]')
                               .get_attribute("href"))
            except Exception as e:
                meeting_url = None
                print(e.__str__())
            try:
                no_of_attendees = driver.find_element(By.XPATH,
                                                      '//*[@id="events-top-card"]/div[1]/div[2]/div/div[1]/div['
                                                      '1]/div[5]/div/div/div').text
            except Exception as e:
                no_of_attendees = None
                print(e.__str__())
            return Event(event_name, event_datetime, event_organizer, meeting_url, no_of_attendees)
        except Exception as e:
            print(f"Error extracting event details: {e}")
            return None

    def register_or_attend(self, driver):
        try:
            self.get_event_details()
            # Try to click the Register button if present
            register_button = WebDriverWait(driver, 2).until(
                EC.element_to_be_clickable((By.XPATH, "//button//span[text()='Register']/.."))
            )
            register_button.click()
            print(f"Clicked 'Register' button for event: {self.name}")
            self.complete_registration(driver)
        except Exception as e:
            print(f"Register button not found for event: {self.name}. Trying 'Attend' button.")
            try:
                # If Register button is not found, try to click the Attend button
                attend_button = WebDriverWait(driver, 2).until(
                    EC.element_to_be_clickable((By.XPATH, "//button//span[text()='Attend']/.."))
                )
                attend_button.click()
                print(f"Clicked 'Attend' button for event: {self.name}")
                time.sleep(5)  # Wait to see the feedback
            except Exception as e:
                print(f"No 'Register' or 'Attend' button found for event: {self.name}")

    def complete_registration(self, driver):
        try:
            # Use a more precise and generalized XPath to locate the submit button
            submit_button = WebDriverWait(driver, 4).until(
                EC.element_to_be_clickable(
                    (By.XPATH, "//button[@class='lead-gen-modal__submit-button artdeco-button artdeco-button--2']"))
            )
            submit_button.click()
            time.sleep(5)  # Wait to see the feedback
            print(f"Clicked 'Submit' button to complete registration for event: {self.name}")
        except Exception as e:
            print(f"No 'Submit' button found to complete registration for event: {self.name}")

    def get_event_details(self):
        return {
            'Event Name': self.name,
            'Event Date': self.datetime,
            'Organizer': self.organizer,
            'Meeting URL': self.meeting_url,
            'Number of Attendees': self.no_of_attendees
        }

    def follow_event_organizer(self, driver):
        try:
            follow_button = WebDriverWait(driver, 2).until(
                EC.element_to_be_clickable(
                    (By.XPATH, "//button[contains(@class, 'update-components-actor__follow-button')]"))
            )
            follow_button.click()
            print(f"Clicked 'Follow' button for event: {self.name}")
        except Exception as e:
            print(f"No 'Follow' button found for event: {self.name} - {e}")

    def share_event(self, driver):
        try:
            share_button = WebDriverWait(driver, 2).until(
                EC.element_to_be_clickable(
                    (By.XPATH, "//button[contains(@class, 'events-components-shared-support-share__share-button')]"))
            )
            share_button.click()
            time.sleep(1)  # Wait for the dropdown to appear

            repost_button = WebDriverWait(driver, 2).until(
                EC.element_to_be_clickable((By.XPATH,
                                            "//div[@class='artdeco-dropdown__content-inner']//li[contains(@class, 'social-share__item--share-box-btn') and .//text()='Repost to Feed']")
                                           )
            )
            repost_button.click()

            time.sleep(2)  # Wait for the dropdown to appear

            post_button = WebDriverWait(driver, 2).until(
                EC.element_to_be_clickable((By.XPATH, "//button//span[text()='Post']/.."))
            )
            post_button.click()
            print(f"Shared event: {self.name}")
        except Exception as e:
            print(f"Error sharing event: {self.name} - {e}")

    @staticmethod
    def invite_users(driver, invited_users):
        try:
            # Click the share button
            share_button = WebDriverWait(driver, 2).until(
                EC.element_to_be_clickable(
                    (By.XPATH, "//button[contains(@class, 'events-components-shared-support-share__share-button')]"))
            )
            share_button.click()
            time.sleep(1)  # Wait for the dropdown to appear

            # Click the invite button
            invite_button = WebDriverWait(driver, 2).until(
                EC.element_to_be_clickable((By.XPATH,
                                            "//div[@class='artdeco-dropdown__content-inner']//li[contains(@class, 'artdeco-dropdown__item') and .//text()='Invite']")
                                           )
            )
            invite_button.click()

            while True:
                users = driver.find_elements(By.XPATH, "//li[contains(@class, 'artdeco-typeahead__result')]")
                new_users_found = False

                for user in users:
                    user_id = user.get_attribute("id")
                    if user_id not in invited_users:
                        invited_users.add(user_id)
                        user.click()
                        new_users_found = True

                if not new_users_found:
                    break

                # Scroll down to load more users
                driver.execute_script("arguments[0].scrollIntoView();", users[-1])
                time.sleep(1)  # Wait for new users to load

            # Click the send invite button
            send_invite_button = WebDriverWait(driver, 2).until(
                EC.element_to_be_clickable(
                    (By.XPATH, "//div[contains(@class, 'text-align-right')]//button[.//span[text()='Invite']]"))
            )
            # send_invite_button.click()
            print("Invited users to event")
        except Exception as e:
            print(f"Error inviting users to event - {e}")

    def scrape_attendees(self, driver):
        try:
            attendees_button = WebDriverWait(driver, 2).until(
                EC.element_to_be_clickable((By.XPATH, "ATTENDEES_BUTTON_XPATH"))
            )
            attendees_button.click()
            time.sleep(2)
            attendees = driver.find_elements(By.XPATH, "ATTENDEE_LIST_XPATH")
            self.attendees = []
            for attendee in attendees:
                name = attendee.find_element(By.XPATH, "ATTENDEE_NAME_XPATH").text
                profile_url = attendee.find_element(By.XPATH, "ATTENDEE_PROFILE_URL_XPATH").get_attribute("href")
                self.attendees.append((name, profile_url))
            self.save_attendees_to_file()
        except Exception as e:
            print(f"Error scraping attendees for event: {self.name} - {e}")

    def save_attendees_to_file(self):
        directory = "./attendees"
        if not os.path.exists(directory):
            os.makedirs(directory)
        filename = os.path.join(directory, f"{self.name}.txt")
        with open(filename, "w") as file:
            for attendee in self.attendees:
                file.write(f"Name: {attendee[0]}, Profile URL: {attendee[1]}\n")
        print(f"Saved attendees to {filename}")
