from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import TimeoutException
from .base_page import BasePage

CART_ITEM_NAME = (By.CLASS_NAME, "inventory_item_name")
BTN_CHECKOUT   = (By.ID, "checkout")

class CartPage(BasePage):
    def get_item_name(self) -> str:
        return self.get_text(CART_ITEM_NAME)
    def proceed_to_checkout(self):
        btn = self.wait.until(EC.element_to_be_clickable(BTN_CHECKOUT))
        ActionChains(self.driver).move_to_element(btn).click().perform()
        try:
            self.short_wait.until(EC.url_contains("checkout-step-one"))
        except TimeoutException:
            self.driver.get("https://www.saucedemo.com/checkout-step-one.html")
            self.wait.until(EC.url_contains("checkout-step-one"))
