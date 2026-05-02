from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from .base_page import BasePage

CART_ITEM_NAME = (By.CLASS_NAME, "inventory_item_name")
BTN_CHECKOUT   = (By.ID, "checkout")

class CartPage(BasePage):
    def get_item_name(self) -> str:
        return self.get_text(CART_ITEM_NAME)
    def proceed_to_checkout(self):
        self.click(BTN_CHECKOUT)
        self.wait.until(EC.url_contains("checkout-step-one"))
