from selenium.webdriver.common.by import By
from .base_page import BasePage


class CheckoutCompletePage(BasePage):
    THANK_YOU_TEXT = (By.CLASS_NAME, "complete-header")

    def get_thankyou(self):
        thank_you_text = self.wait_for_element(self.THANK_YOU_TEXT)
        return thank_you_text.text
