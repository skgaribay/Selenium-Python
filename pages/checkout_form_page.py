from selenium.webdriver.common.by import By
from .base_page import BasePage


class CheckoutFormPage(BasePage):
    FIRSTNAME_FIELD = (By.ID, "first-name")
    LASTNAME_FIELD = (By.ID, "last-name")
    ZIP_FIELD = (By.ID, "postal-code")
    CONTINUE_BUTTON = (By.ID, "continue")
    ERROR_CONTAINER = (By.CLASS_NAME, "error-message-container")

    CHECKOUT_OVERVIEW_URL = "https://www.saucedemo.com/checkout-step-two.html"

    def enter_firstname(self, firstname):
        firstname_field = self.wait_for_element(self.FIRSTNAME_FIELD)
        firstname_field.clear()
        firstname_field.send_keys(firstname)

    def enter_lastname(self, lastname):
        lastname_field = self.wait_for_element(self.LASTNAME_FIELD)
        lastname_field.clear()
        lastname_field.send_keys(lastname)

    def enter_zip(self, zipcode):
        zip_field = self.wait_for_element(self.ZIP_FIELD)
        zip_field.clear()
        zip_field.send_keys(zipcode)

    def go_continue(self):
        continue_button = self.wait_for_clickable_element(self.CONTINUE_BUTTON)

        try:
            continue_button.click()
            self.wait_for_url(self.CHECKOUT_OVERVIEW_URL)
            return True
        except Exception as e:
            print(e)
            return False

    def check_for_error(self):
        error_container = self.find_element(self.ERROR_CONTAINER)
        return error_container

    def get_error(self):
        error_message = self.check_for_error()
        return error_message.text

    def complete_form(self, firstname, lastname, zipcode):
        self.enter_firstname(firstname)
        self.enter_lastname(lastname)
        self.enter_zip(zipcode)
