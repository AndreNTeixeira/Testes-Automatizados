import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from web.pages.login_page import LoginPage
from web.pages.inventory_page import InventoryPage
from web.pages.cart_page import CartPage

VALID_USER     = "standard_user"
VALID_PASSWORD = "secret_sauce"

@pytest.fixture
def driver():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1920,1080")
    browser = webdriver.Chrome(options=options)
    yield browser
    browser.quit()

@pytest.fixture
def logged_in(driver):
    LoginPage(driver).open().login(VALID_USER, VALID_PASSWORD)
    return driver

@pytest.fixture
def cart_ready(logged_in):
    InventoryPage(logged_in).add_first_item_to_cart().go_to_cart()
    return logged_in

@pytest.fixture
def checkout_ready(cart_ready):
    CartPage(cart_ready).proceed_to_checkout()
    return cart_ready
