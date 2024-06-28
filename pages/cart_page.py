from selenium.webdriver.common.by import By
from .base_page import BasePage


class CartPage(BasePage):
    CHECKOUT_BUTTON = (By.ID, "checkout")
    FIRST_ITEM_NAME = (By.ID, "item_2_title_link")
    SECOND_ITEM_NAME = (By.ID, "item_0_title_link")
    FIRST_ITEM_PRICE = (By.CSS_SELECTOR, "body > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > div:nth-child(3) > div:nth-child(2) > div:nth-child(3) > div:nth-child(1)")
    SECOND_ITEM_PRICE = (By.CSS_SELECTOR, "body > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > div:nth-child(4) > div:nth-child(2) > div:nth-child(3) > div:nth-child(1)")

    CHECKOUT_FORM_URL = "https://www.saucedemo.com/checkout-step-one.html"

    def go_to_checkout(self):
        checkout_button = self.wait_for_clickable_element(self.CHECKOUT_BUTTON)

        try:
            checkout_button.click()
            self.wait_for_url(self.CHECKOUT_FORM_URL)
            return True
        except Exception as e:
            print(e)
            return False

    def get_items(self):
        name1 = self.find_element(self.FIRST_ITEM_NAME).text
        name2 = self.find_element(self.SECOND_ITEM_NAME).text
        price1 = self.find_element(self.FIRST_ITEM_PRICE).text
        price2 = self.find_element(self.SECOND_ITEM_PRICE).text

        return [(name1, price1), (name2, price2)]
