from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from .base_page import BasePage

ADD_FIRST_ITEM = (By.CSS_SELECTOR, ".inventory_item button")
CART_ICON = (By.CLASS_NAME, "shopping_cart_link")

class InventoryPage(BasePage):
    def add_first_item_to_cart(self):
        self.click(ADD_FIRST_ITEM)
        return self
    def go_to_cart(self):
        self.click(CART_ICON)
        try:
            self.short_wait.until(EC.url_contains("cart.html"))
        except TimeoutException:
            self.driver.get("https://www.saucedemo.com/cart.html")
            self.wait.until(EC.url_contains("cart.html"))
