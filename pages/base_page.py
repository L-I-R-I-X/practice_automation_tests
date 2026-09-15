from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class BasePage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    def find_element(self, locator) -> WebElement:
        return self.wait.until(EC.visibility_of_element_located(locator))

    def find_elements(self, locator) -> list[WebElement]:
        return self.wait.until(EC.visibility_of_all_elements_located(locator))

    def click(self, locator) -> None:
        element = self.wait.until(EC.element_to_be_clickable(locator))
        self.driver.execute_script("arguments[0].scrollIntoView(true);", element)
        element.click()

    def type_text(self, locator, text) -> None:
        element = self.wait.until(EC.visibility_of_element_located(locator))
        element.click()
        element.clear()
        element.send_keys(text)

    def get_text(self, locator) -> str:
        return self.find_element(locator).text

    def is_element_available(self, locator) -> bool:
        try:
            return self.wait.until(EC.visibility_of_element_located(locator)).is_displayed()
        except Exception:
            return False

    def is_displayed(self, locator) -> bool:
        for element in self.driver.find_elements(*locator):
            if element.is_displayed():
                return True
        return False

    def wait_for_visible(self, locator, timeout: int = 10) -> bool:
        try:
            WebDriverWait(self.driver, timeout).until(EC.visibility_of_element_located(locator))
            return True
        except Exception:
            return False

    def wait_until_hidden(self, locator, timeout: int = 10) -> bool:
        try:
            WebDriverWait(self.driver, timeout).until(EC.invisibility_of_element_located(locator))
            return True
        except Exception:
            return False

    def press_escape(self) -> None:
        from selenium.webdriver.common.keys import Keys
        from selenium.webdriver.common.action_chains import ActionChains

        ActionChains(self.driver).send_keys(Keys.ESCAPE).perform()