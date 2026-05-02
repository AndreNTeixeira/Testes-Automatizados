from selenium.webdriver.common.by import By
from .base_page import BasePage

COMPLETE_HEADER = (By.CSS_SELECTOR, "[data-test='complete-header']")

class CheckoutCompletePage(BasePage):
    def get_confirmation_message(self) -> str:
        return self.get_text(COMPLETE_HEADER)
