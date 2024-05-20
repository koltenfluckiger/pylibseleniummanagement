import time

from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.common.by import By


class CachedElement:
    def __init__(self, driver_client, locator, max_retries=3, retry_delay=1):
        self.driver_client = driver_client
        self.locator = locator
        self.max_retries = max_retries
        self.retry_delay = retry_delay
        self.element = None

    def locate(self):
        self.element = self.driver_client.get_element(self.locator)

    def get_element(self):
        if not self.element:
            self.locate()
        return self.element

    def perform_action(self, action, *args, **kwargs):
        retries = 0
        while retries < self.max_retries:
            try:
                element = self.get_element()
                action(element, *args, **kwargs)
                return
            except StaleElementReferenceException:
                retries += 1
                self.element = None  # Clear the cached element
                time.sleep(self.retry_delay)
        raise StaleElementReferenceException(
            f"Element located by {self.locator} is stale after {self.max_retries} retries")

    def click(self):
        self.perform_action(lambda elem: elem.click())

    def send_keys(self, keys):
        self.perform_action(lambda elem, keys: elem.send_keys(keys), keys)
