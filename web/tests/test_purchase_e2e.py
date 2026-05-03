import pytest
from web.pages.login_page import LoginPage
from web.pages.inventory_page import InventoryPage
from web.pages.cart_page import CartPage
from web.pages.checkout_page import CheckoutPage
from web.pages.checkout_complete_page import CheckoutCompletePage

@pytest.mark.web
class TestLogin:
    def test_login_success(self, logged_in):
        assert "inventory" in logged_in.current_url

    def test_login_invalid(self, driver):
        login = LoginPage(driver).open()
        login.login("wrong_user", "wrong_pass")
        assert "Epic sadface" in login.get_error()


@pytest.mark.web
class TestCart:
    def test_item_in_cart(self, cart_ready):
        assert CartPage(cart_ready).get_item_name() == "Sauce Labs Backpack"


@pytest.mark.web
class TestCheckout:
    def test_fill_checkout_form(self, checkout_ready):
        CheckoutPage(checkout_ready).fill_info("Andre", "Tester", "12345").continue_to_overview()
        assert "checkout-step-two" in checkout_ready.current_url

    def test_complete_purchase(self, checkout_ready):
        CheckoutPage(checkout_ready).fill_info("Andre", "Tester", "12345").continue_to_overview()
        page = CheckoutCompletePage(checkout_ready).finish_purchase()
        assert page.get_confirmation_message() == "Thank you for your order!"
