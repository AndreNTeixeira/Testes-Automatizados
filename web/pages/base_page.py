from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

TIMEOUT = 20

class BasePage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, TIMEOUT)

    def find(self, locator):
        return self.wait.until(EC.visibility_of_element_located(locator))

    def click(self, locator):
        element = self.wait.until(EC.presence_of_element_located(locator))
        element.click()




    def type(self, locator, text):
        field = self.wait.until(EC.visibility_of_element_located(locator))
        field.clear()
        field.send_keys(text)

    def get_text(self, locator) -> str:
        return self.find(locator).text
