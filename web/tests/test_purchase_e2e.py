import pytest
from selenium.webdriver.common.by import By
from web.pages.login_page import LoginPage
from web.pages.inventory_page import InventoryPage
from web.pages.cart_page import CartPage
from web.pages.checkout_page import CheckoutPage
from web.pages.checkout_complete_page import CheckoutCompletePage
from web.pages.base_page import BasePage

VALID_USER     = "standard_user"
VALID_PASSWORD = "secret_sauce"

@pytest.mark.web
class TestE2EPurchase:
    def test_complete_purchase(self, driver):
        LoginPage(driver).open().login(VALID_USER, VALID_PASSWORD)

        InventoryPage(driver).add_first_item_to_cart().go_to_cart()

        cart = CartPage(driver)
        assert cart.get_item_name() == "Sauce Labs Backpack"

        cart.proceed_to_checkout()

        CheckoutPage(driver).fill_info("Andre", "Tester", "12345").continue_to_overview()

        BasePage(driver).click((By.ID, "finish"))

        msg = CheckoutCompletePage(driver).get_confirmation_message()
        assert msg == "Thank you for your order!"

    def test_login_with_invalid_credentials(self, driver):
        login = LoginPage(driver).open()
        login.login("wrong_user", "wrong_pass")
        assert "Epic sadface" in login.get_error()
