# pages/base_page.py
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.common.exceptions import TimeoutException, NoSuchElementException


class BasePage:
    def __init__(self, driver):
        self.driver = driver

    def find_element(self, locator):
        try:
            return self.driver.find_element(*locator)
        except NoSuchElementException:
            return None

    def wait_for_element(self, locator, timeout=10):
        try:
            element = WebDriverWait(self.driver, timeout).until(
                ec.visibility_of_element_located(locator)
            )
            return element
        except TimeoutException:
            raise AssertionError(f"Element {locator} not found within {timeout} seconds")

    def wait_for_clickable_element(self, locator, timeout=10):
        try:
            element = WebDriverWait(self.driver, timeout).until(
                ec.element_to_be_clickable(locator)
            )
            return element
        except TimeoutException:
            raise AssertionError(f"Clickable element {locator} not found within {timeout} seconds")
