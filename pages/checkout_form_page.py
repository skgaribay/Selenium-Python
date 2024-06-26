from selenium.webdriver.common.by import By
from .base_page import BasePage
import time

class CheckoutFormPage(BasePage):
    FIRSTNAME_FIELD = (By.ID, "first-name")
    LASTNAME_FIELD = (By.ID, "last-name")
    ZIP_FIELD = (By.ID, "postal-code")
    CONTINUE_BUTTON = (By.ID, "continue")

    def enter_firstname(self, firstname):
        firstname_field = self.wait_for_element(self.FIRSTNAME_FIELD)
        firstname_field.clear()
        firstname_field.send_keys(firstname)

    def enter_lastname(self, lastname):
        lastname_field = self.wait_for_element(self.LASTNAME_FIELD)
        lastname_field.clear()
        lastname_field.send_keys(lastname)

    def enter_zip(self, zip):
        zip_field = self.wait_for_element(self.ZIP_FIELD)
        zip_field.clear()
        zip_field.send_keys(zip)
        
    def go_continue(self):
        continue_button = self.wait_for_clickable_element(self.CONTINUE_BUTTON)
        continue_button.click()
        
