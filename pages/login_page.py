# pages/login_page.py
from selenium.webdriver.common.by import By
from .base_page import BasePage

class LoginPage(BasePage):
    USERNAME_FIELD = (By.ID, "username")
    PASSWORD_FIELD = (By.ID, "password")
    LOGIN_BUTTON = (By.ID, "login-btn")
    ERROR_MESSAGE = (By.ID, "error-message")

    def enter_username(self, username):
        username_field = self.wait_for_element(self.USERNAME_FIELD)
        username_field.clear()
        username_field.send_keys(username)

    def enter_password(self, password):
        password_field = self.wait_for_element(self.PASSWORD_FIELD)
        password_field.clear()
        password_field.send_keys(password)

    def click_login_button(self):
        login_button = self.wait_for_clickable_element(self.LOGIN_BUTTON)
        login_button.click()

    def get_error_message(self):
        error_element = self.find_element(self.ERROR_MESSAGE)
        return error_element.text if error_element.is_displayed() else ""
