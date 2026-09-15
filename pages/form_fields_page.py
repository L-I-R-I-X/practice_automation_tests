import allure
from selenium.webdriver.common.by import By

from pages.base_page import BasePage


class FormFieldsPage(BasePage):
    URL = "https://practice-automation.com/form-fields/"

    AUTOMATION_TOOLS_LIST = (By.XPATH, "//label[normalize-space(text())='Automation tools']/following-sibling::ul[1]")
    AUTOMATION_TOOLS_ITEMS = (By.XPATH, "//label[normalize-space(text())='Automation tools']/following-sibling::ul[1]/li")

    @allure.step("Открыть страницу Form Fields")
    def open_page(self) -> None:
        self.driver.get(self.URL)

    @allure.step("Получить полный текст списка инструментов")
    def get_tools_list_text(self) -> str:
        return self.get_text(self.AUTOMATION_TOOLS_LIST)

    @allure.step("Получить отдельные пункты списка инструментов")
    def get_tools_items(self) -> list[str]:
        return [item.text for item in self.find_elements(self.AUTOMATION_TOOLS_ITEMS)]

    @allure.step("Собрать пункты списка инструментов в одну строку")
    def get_joined_tools_text(self) -> str:
        return "\n".join(self.get_tools_items())