from selenium.webdriver.common.by import By
from .base_page import BasePage
import time

class ProductPage(BasePage):
    PAGE_TITLE = (By.CLASS_NAME, "title")
    SORT_LOW_HIGH = (By.CSS_SELECTOR, "#header_container > div.header_secondary_container > div > span > select > option:nth-child(3)")
    TO_CART_ONESIE = (By.ID, "add-to-cart-sauce-labs-onesie")
    TO_CART_BIKE = (By.ID, "add-to-cart-sauce-labs-bike-light")
    CART = (By.CLASS_NAME, "shopping_cart_link")

    def get_pageTitle(self):
        page_title = self.wait_for_element(self.PAGE_TITLE)
        return page_title.text
    
    def sort_price_low_high(self):
        sort_menu = self.wait_for_clickable_element(self.SORT_LOW_HIGH)
        sort_menu.click()
        
    def add_onesie(self):
        to_cart_onesie = self.wait_for_clickable_element(self.TO_CART_ONESIE)
        to_cart_onesie.click()
        
    def add_bike(self):
        to_cart_bike = self.wait_for_clickable_element(self.TO_CART_BIKE)
        to_cart_bike.click()
        
    def go_to_cart(self):
        cart = self.wait_for_clickable_element(self.CART)
        cart.click()
    

