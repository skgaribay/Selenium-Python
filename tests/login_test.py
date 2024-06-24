# tests/test_login_page.py
import pytest
from selenium import webdriver
from pages.page_object_manager import PageObjectManager

@pytest.fixture(scope="class")
def setup(request):
    driver = webdriver.Chrome(executable_path='path/to/chromedriver')
    driver.get("http://example.com/login")  # Replace with your actual login page URL
    driver.maximize_window()
    request.cls.page_manager = PageObjectManager(driver)
    request.cls.driver = driver
    yield
    driver.quit()

@pytest.mark.usefixtures("setup")
class TestLoginPage:

    def test_valid_login(self):
        login_page = self.page_manager.get_login_page()
        login_page.enter_username("valid_username")
        login_page.enter_password("valid_password")
        login_page.click_login_button()
        # Add assertions for successful login
        assert "Welcome" in self.driver.title  # Example assertion

    def test_invalid_login(self):
        login_page = self.page_manager.get_login_page()
        login_page.enter_username("invalid_username")
        login_page.enter_password("invalid_password")
        login_page.click_login_button()
        error_message = login_page.get_error_message()
        # Add assertions for invalid login
        assert "Invalid credentials" in error_message  # Example assertion

    def test_email_validation(self):
        login_page = self.page_manager.get_login_page()
        login_page.enter_username("invalid_email")
        login_page.enter_password("password123")
        login_page.click_login_button()
        error_message = login_page.get_error_message()
        # Add assertions for email validation
        assert "Please enter a valid email" in error_message  # Example assertion
