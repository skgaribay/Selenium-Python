from selenium.webdriver.common.by import By
from .base_page import BasePage


class LoginPage(BasePage):
    USERNAME_FIELD = (By.ID, "user-name")
    PASSWORD_FIELD = (By.ID, "password")
    LOGIN_BUTTON = (By.ID, "login-button")
    ERROR_CONTAINER = (By.CLASS_NAME, "error-message-container")

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

    def check_for_error(self):
        error_container = self.find_element(self.ERROR_CONTAINER)
        return error_container

    def get_error(self):
        error_message = self.check_for_error()
        return error_message.text

    def login(self, username, password):
        self.enter_username(username)
        self.enter_password(password)
        self.click_login_button()
