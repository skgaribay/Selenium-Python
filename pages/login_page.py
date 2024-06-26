from selenium.webdriver.common.by import By
from .base_page import BasePage

class LoginPage(BasePage):
    USERNAME_FIELD = (By.ID, "user-name")
    PASSWORD_FIELD = (By.ID, "password")
    LOGIN_BUTTON = (By.ID, "login-button")

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
