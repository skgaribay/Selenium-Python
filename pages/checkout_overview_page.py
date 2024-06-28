from selenium.webdriver.common.by import By
from .base_page import BasePage
from utils.num_utils import currency_to_float


class CheckoutOverviewPage(BasePage):
    FINISH_BUTTON = (By.ID, "finish")
    FIRST_ITEM_NAME = (By.ID, "item_2_title_link")
    SECOND_ITEM_NAME = (By.ID, "item_0_title_link")
    FIRST_ITEM_PRICE = (By.CSS_SELECTOR, "body > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > div:nth-child(3) > div:nth-child(2) > div:nth-child(3) > div:nth-child(1)")
    SECOND_ITEM_PRICE = (By.CSS_SELECTOR, "body > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > div:nth-child(4) > div:nth-child(2) > div:nth-child(3) > div:nth-child(1)")
    ITEM_TOTAL = (By.CLASS_NAME, "summary_subtotal_label")
    TAX_VALUE = (By.CLASS_NAME, "summary_tax_label")
    PRICE_TOTAL = (By.CLASS_NAME, "summary_total_label")

    CHECKOUT_COMPLETE_URL = "https://www.saucedemo.com/checkout-complete.html"

    def go_finish(self):
        finish_button = self.wait_for_clickable_element(self.FINISH_BUTTON)

        try:
            finish_button.click()
            self.wait_for_url(self.CHECKOUT_COMPLETE_URL)
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

    def get_prices(self):
        item_total_str = self.find_element(self.ITEM_TOTAL).text
        price_total_str = self.find_element(self.PRICE_TOTAL).text

        item_total = currency_to_float(item_total_str[12:])
        price_total = currency_to_float(price_total_str[7:])

        return [item_total, price_total]
