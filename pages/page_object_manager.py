# pages/page_object_manager.py
from .login_page import LoginPage
from .product_page import ProductPage
from .cart_page import CartPage
from .checkout_form_page import CheckoutFormPage
from .checkout_overview_page import CheckoutOverviewPage
from .checkout_complete_page import CheckoutCompletePage


class PageObjectManager:
    def __init__(self, driver):
        self.driver = driver

    def get_login_page(self):
        return LoginPage(self.driver)

    def get_product_page(self):
        return ProductPage(self.driver)

    def get_cart_page(self):
        return CartPage(self.driver)

    def get_checkout_form_page(self):
        return CheckoutFormPage(self.driver)

    def get_checkout_overview_page(self):
        return CheckoutOverviewPage(self.driver)

    def get_checkout_complete_page(self):
        return CheckoutCompletePage(self.driver)
