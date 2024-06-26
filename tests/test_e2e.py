# tests/test_login_page.py
import pytest
# import os
from selenium import webdriver
from pages.page_object_manager import PageObjectManager
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options


@pytest.fixture(scope="function")
def setup(request):
    options = Options()
    options.add_argument('--headless')
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.get("https://www.saucedemo.com/")
    driver.maximize_window()
    request.cls.page_manager = PageObjectManager(driver)
    request.cls.driver = driver
    yield
    driver.quit()


user_data = [
    ("standard_user", "secret_sauce", "Larry", "David", "1101"),
    # ("locked_out_user", "secret_sauce", "John", "Smith", "2202"),
    # ("problem_user", "secret_sauce", "Emily", "Johnson", "3303"),
    # ("performance_glitch_user", "secret_sauce", "Michael", "Williams", "4404"),
    # ("error_user", "secret_sauce", "Jessica", "Brown", "5505"),
    # ("visual_user", "secret_sauce", "Daniel", "Jones", "6606")
]


@pytest.mark.usefixtures("setup")
class TestE2E:

    @pytest.mark.parametrize("username, password, firstname, lastname, zipcode", user_data)
    def test_checkout_flow(self, username, password, firstname, lastname, zipcode):
        # login
        login_page = self.page_manager.get_login_page()
        login_page.enter_username(username)
        login_page.enter_password(password)
        login_page.click_login_button()

        # pick items, go to cart
        product_page = self.page_manager.get_product_page()
        product_page.sort_price_low_high()
        product_page.add_onesie()
        # >get product name and price
        product_page.add_bike()
        # >get product name and price
        product_page.go_to_cart()

        # verify products in cart
        cart_page = self.page_manager.get_cart_page()
        # >validate products
        cart_page.go_to_checkout()

        # fill-out checkout form
        checkout_form_page = self.page_manager.get_checkout_form_page()
        checkout_form_page.enter_firstname(firstname)
        checkout_form_page.enter_lastname(lastname)
        checkout_form_page.enter_zip(zipcode)
        checkout_form_page.go_continue()

        # verify order details
        checkout_overview_page = self.page_manager.get_checkout_overview_page()
        # >validate prices
        checkout_overview_page.go_finish()

        # verify order complete
        checkout_complete_page = self.page_manager.get_checkout_complete_page()
        assert "Thank you for your order!" == checkout_complete_page.get_thankyou()
