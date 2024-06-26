from selenium.webdriver.common.by import By
from .base_page import BasePage

class CheckoutOverviewPage(BasePage):
    FINISH_BUTTON = (By.ID, "finish")
        
    def go_finish(self):
        finish_button = self.wait_for_clickable_element(self.FINISH_BUTTON)
        finish_button.click()
        
