import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

from pages.base_page import BasePage


class CalendarsPage(BasePage):
    URL = "https://practice-automation.com/calendars/"

    DATE_FIELD = (By.ID, "g1065-1-selectorenteradate")
    DATE_FIELD_LABEL = (By.CSS_SELECTOR, "label[for='g1065-1-selectorenteradate']")
    DATE_FORMAT_HINT = (By.ID, "g1065-1-selectorenteradate-text-format")
    DATE_FIELD_ERROR = (By.ID, "g1065-1-selectorenteradate-text-error-message")
    SUBMIT_BTN = (By.XPATH,
                  "//form[.//input[@id='g1065-1-selectorenteradate']]"
                  "//button[contains(@class,'pushbutton-wide')]")
    SUCCESS_MESSAGE = (By.CSS_SELECTOR, ".contact-form-submission, .jetpack-form-success")

    @allure.step("Открыть страницу Calendars")
    def open_page(self) -> None:
        self.driver.get(self.URL)

    @allure.step("Ввести дату вручную в формате YYYY-MM-DD")
    def enter_date_manually(self, date: str) -> None:
        self.type_text(self.DATE_FIELD, date)

    @allure.step("Получить текущее значение поля даты")
    def get_date_value(self) -> str:
        return self.find_element(self.DATE_FIELD).get_attribute("value")

    @allure.step("Получить подсказку формата даты")
    def get_format_hint(self) -> str:
        return self.get_text(self.DATE_FORMAT_HINT)

    @allure.step("Получить текст ошибки валидации даты")
    def get_date_field_error(self) -> str:
        return self.get_text(self.DATE_FIELD_ERROR)

    @allure.step("Отправить форму с датой")
    def submit_form(self) -> None:
        self.click(self.SUBMIT_BTN)

    @allure.step("Проверить сообщение об успешной отправке")
    def is_success_message_visible(self, timeout: int = 20) -> bool:
        return self.wait_for_visible(self.SUCCESS_MESSAGE, timeout)

    @allure.step("Дождаться и получить текст сообщения об успешной отправке")
    def wait_for_success_message(self, timeout: int = 20) -> str:
        def _has_response_text(driver) -> str | None:
            for element in driver.find_elements(*self.SUCCESS_MESSAGE):
                if element.is_displayed() and "Thank you" in element.text:
                    return element.text
            return None

        return WebDriverWait(self.driver, timeout).until(_has_response_text)