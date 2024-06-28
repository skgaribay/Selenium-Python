# import time

import pytest
import math

from selenium.common import UnexpectedAlertPresentException, NoAlertPresentException

from utils.num_utils import currency_to_float

user_data = [
    ("standard_user", "secret_sauce", "Larry", "David", "1101"),
    ("performance_glitch_user", "secret_sauce", "Michael", "Williams", "4404"),
    ("visual_user", "secret_sauce", "Daniel", "Jones", "6606"),
    # ("error_user", "secret_sauce", "Jessica", "Brown", "5505"),
    # ("locked_out_user", "secret_sauce", "John", "Smith", "2202"),
    # ("problem_user", "secret_sauce", "Emily", "Johnson", "3303")
]

master_pass = "secret_sauce"
locked_out_user = "locked_out_user"
problem_user = "problem_user"
error_user = "error_user"


@pytest.fixture(scope="function")
def initialize_pages(request):
    # Ensure the WebDriver is set up
    if not hasattr(request.cls, 'page_manager'):
        raise AttributeError("PageManager not initialized. Make sure the 'setup' fixture is used.")

    # Initialize page objects
    request.cls.login_page = request.cls.page_manager.get_login_page()
    request.cls.product_page = request.cls.page_manager.get_product_page()
    request.cls.cart_page = request.cls.page_manager.get_cart_page()
    request.cls.checkout_form_page = request.cls.page_manager.get_checkout_form_page()
    request.cls.checkout_overview_page = request.cls.page_manager.get_checkout_overview_page()
    request.cls.checkout_complete_page = request.cls.page_manager.get_checkout_complete_page()


@pytest.mark.usefixtures("setup", "initialize_pages")
class TestE2E:

    def test_error(self):
        login_page = self.login_page
        product_page = self.product_page

        login_page.login(error_user, master_pass)
        assert login_page.check_for_error() is None, "Login failed."

        product_page.sort_price_low_high()
        try:
            product_page.go_to_cart()
        except UnexpectedAlertPresentException as err:
            assert "Sorting is broken! This error has been reported to Backtrace." in err.msg

    def test_error_checkout(self):
        login_page = self.login_page
        product_page = self.product_page
        cart_page = self.cart_page
        checkout_form_page = self.checkout_form_page
        checkout_overview_page = self.checkout_overview_page

        # login
        login_page.login(error_user, master_pass)
        assert login_page.check_for_error() is None, "Login failed."

        # pick items, go to cart
        # catch the alert if present
        product_page.sort_price_low_high()
        try:
            product_page.add_onesie()
        except UnexpectedAlertPresentException as err:
            try:
                print(f"Caught Error: {err.msg}")
                alert = self.driver.switch_to.alert
                alert.accept()
            except NoAlertPresentException:
                print("No alert present.")
                product_page.add_onesie()

        product_page.add_bike()
        if not product_page.go_to_cart():
            assert False, "Navigation to cart page failed"

        if not cart_page.go_to_checkout():
            assert False, "Navigation to checkout form page failed"

        # fill-out checkout form
        checkout_form_page.complete_form("Jessica", "Brown", "5505")

        if not checkout_form_page.go_continue():
            assert False, "Navigation to checkout overview page failed"

        assert checkout_form_page.check_for_error() is None, "Form validation error."

        if checkout_overview_page.go_finish():
            assert False, "Unexpected error. Navigation should have failed."

    def test_locked_out(self):
        login_page = self.login_page
        login_page.login(locked_out_user, master_pass)
        login_error = login_page.get_error()
        assert login_error == "Epic sadface: Sorry, this user has been locked out.", "Unexpected error message"

    def test_problem(self):
        login_page = self.login_page
        product_page = self.product_page
        cart_page = self.cart_page
        checkout_form_page = self.checkout_form_page

        login_page.login(problem_user, master_pass)
        assert login_page.check_for_error() is None, "Login failed."

        # pick items, go to cart
        product_page.sort_price_low_high()
        product_page.add_onesie()
        product_page.add_bike()
        product_page.go_to_cart()

        # verify items not expected, negative test
        cart_page.go_to_checkout()

        # fill out the form and try to continue
        checkout_form_page.complete_form("Emily", "Johnson", "3303")
        checkout_form_page.go_continue()
        form_error = checkout_form_page.get_error()
        assert form_error == "Error: Last Name is required", "Unexpected error message"

    @pytest.mark.parametrize("username, password, firstname, lastname, zipcode", user_data)
    def test_full_checkout(self, username, password, firstname, lastname, zipcode):
        # Simplify object calling
        login_page = self.login_page
        product_page = self.product_page
        cart_page = self.cart_page
        checkout_form_page = self.checkout_form_page
        checkout_overview_page = self.checkout_overview_page
        checkout_complete_page = self.checkout_complete_page

        # collecting errors for soft assertions
        errors = []

        # login
        login_page.login(username, password)
        assert login_page.check_for_error() is None, "Login failed."

        # pick items, go to cart
        # catch the alert if present
        product_page.sort_price_low_high()
        try:
            product_page.add_onesie()
        except UnexpectedAlertPresentException as err:
            print(f"Caught Error: {err.msg}")
            try:
                alert = self.driver.switch_to.alert
                alert.accept()
            except NoAlertPresentException:
                print("No alert present.")
                product_page.add_onesie()

        product_page.add_bike()
        # products = product_page.get_items() # used in verifying checkout, disabled
        if not product_page.go_to_cart():
            assert False, "Navigation to cart page failed"

        # verify products in cart (used to catch visual_user errors, but will fail the test)
        cart_items = cart_page.get_items()
        # verify that the items and prices are correct (relative to products page)
        # for product, item in zip(products, cart_items):
        #     if product[0] != item[0]:
        #         errors.append(f"Product {product[0]} != cart item: {item[0]} ")
        #     if product[1] != item[1]:
        #         errors.append(f"Product price {product[1]} != cart item price: {item[1]} ")
        if not cart_page.go_to_checkout():
            assert False, "Navigation to checkout form page failed"

        # fill-out checkout form
        checkout_form_page.complete_form(firstname, lastname, zipcode)

        if not checkout_form_page.go_continue():
            assert False, "Navigation to checkout overview page failed"

        assert checkout_form_page.check_for_error() is None, "Form validation error."

        # verify order details
        overview_items = checkout_overview_page.get_items()
        # verify that the items and prices are correct (relative to cart page)
        for c_item, o_item in zip(cart_items, overview_items):
            if c_item[0] != o_item[0]:
                errors.append(f"cart item {c_item[0]} != overview item {o_item[0]} ")
            if c_item[1] != o_item[1]:
                errors.append(f"cart item price {c_item[1]} != overview item price {o_item[1]} ")

        # calculate actual prices and tax
        prices = checkout_overview_page.get_prices()
        item_price1 = currency_to_float(overview_items[0][1])
        item_price2 = currency_to_float(overview_items[1][1])
        actual_item_total = item_price1 + item_price2
        actual_tax_value = int(actual_item_total * 8.01) / 100.00
        actual_price_total = actual_item_total + actual_tax_value

        # verify actual and expected values
        if actual_item_total != prices[0]:
            errors.append(f"Item Total: {actual_item_total} != {prices[0]} ")
        if not math.isclose(actual_price_total, prices[1]):
            errors.append(f"Price Total: {actual_price_total} != {prices[1]} ")

        if not checkout_overview_page.go_finish():
            assert False, "Navigation to checkout complete page failed"

        # verify order complete
        if "Thank you for your order!" != checkout_complete_page.get_thankyou():
            errors.append("Order not completed")
        print("end")
        assert not errors, f"Errors: {errors}"
