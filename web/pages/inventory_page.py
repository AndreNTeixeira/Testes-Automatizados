from selenium.webdriver.common.by import By
from .base_page import BasePage

ADD_FIRST_ITEM = (By.CSS_SELECTOR, ".inventory_item button")
CART_ICON = (By.CLASS_NAME, "shopping_cart_link")

class InventoryPage(BasePage):
    def add_first_item_to_cart(self):
        self.click(ADD_FIRST_ITEM)
        return self

    def go_to_cart(self):
        self.click(CART_ICON)
