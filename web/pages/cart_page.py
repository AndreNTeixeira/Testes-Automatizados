from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from .base_page import BasePage

CART_ITEM_NAME = (By.CLASS_NAME, "inventory_item_name")
BTN_CHECKOUT   = (By.ID, "checkout")

class CartPage(BasePage):
    def get_item_name(self) -> str:
        return self.get_text(CART_ITEM_NAME)
    def proceed_to_checkout(self):
        self.wait.until(lambda d: d.execute_script("return document.readyState") == "complete")
        btn = self.wait.until(EC.element_to_be_clickable(BTN_CHECKOUT))
        ActionChains(self.driver).move_to_element(btn).click().perform()
        self.wait.until(EC.url_contains("checkout-step-one"))
