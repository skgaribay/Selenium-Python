from selenium.webdriver.common.by import By
from .base_page import BasePage
import time

class CartPage(BasePage):
    CHECKOUT_BUTTON = (By.ID, "checkout")

    def go_to_checkout(self):
        checkout_button = self.wait_for_clickable_element(self.CHECKOUT_BUTTON)
        checkout_button.click()
        
