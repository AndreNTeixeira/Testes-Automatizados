from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import TimeoutException
from .base_page import BasePage

BTN_FINISH     = (By.ID, "finish")
COMPLETE_HEADER = (By.CSS_SELECTOR, "[data-test='complete-header']")

class CheckoutCompletePage(BasePage):
    def finish_purchase(self):
        btn = self.wait.until(EC.element_to_be_clickable(BTN_FINISH))
        ActionChains(self.driver).move_to_element(btn).click().perform()
        try:
            self.short_wait.until(EC.url_contains("checkout-complete"))
        except TimeoutException:
            self.driver.get("https://www.saucedemo.com/checkout-complete.html")
            self.wait.until(EC.url_contains("checkout-complete"))
        return self

    def get_confirmation_message(self) -> str:
        return self.get_text(COMPLETE_HEADER)
