# pages/page_object_manager.py
from .login_page import LoginPage
# Add imports for other page classes as needed

class PageObjectManager:
    def __init__(self, driver):
        self.driver = driver

    def get_login_page(self):
        return LoginPage(self.driver)
        # Add methods for other page objects as needed
