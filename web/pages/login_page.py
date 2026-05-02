from selenium.webdriver.common.by import By
from .base_page import BasePage

URL = "https://www.saucedemo.com/"

USERNAME = (By.ID, "user-name")
PASSWORD = (By.ID, "password")
BTN_LOGIN = (By.ID, "login-button")
ERROR_MSG = (By.CSS_SELECTOR, "[data-test='error']")

class LoginPage(BasePage):
    def open(self):
        self.driver.get(URL)
        return self

    def login(self, username: str, password: str):
        self.type(USERNAME, username)
        self.type(PASSWORD, password)
        self.click(BTN_LOGIN)

    def get_error(self) -> str:
        return self.get_text(ERROR_MSG)
