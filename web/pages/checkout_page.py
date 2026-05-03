from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from .base_page import BasePage

FIRST_NAME   = (By.ID, "first-name")
LAST_NAME    = (By.ID, "last-name")
POSTAL_CODE  = (By.ID, "postal-code")
BTN_CONTINUE = (By.ID, "continue")

class CheckoutPage(BasePage):
    def fill_info(self, first: str, last: str, postal: str):
        self.type(FIRST_NAME, first)
        self.type(LAST_NAME, last)
        self.type(POSTAL_CODE, postal)
        return self
    def continue_to_overview(self):
        self.click(BTN_CONTINUE)
        self.wait.until(EC.url_contains("checkout-step-two"))
