import allure
from selenium.webdriver.common.by import By

from pages.base_page import BasePage


class ModalsPage(BasePage):
    URL = "https://practice-automation.com/modals/"

    SIMPLE_MODAL_BTN = (By.ID, "simpleModal")
    FORM_MODAL_BTN = (By.ID, "formModal")

    MODAL_OVERLAY = (By.CSS_SELECTOR, "div.pum.pum-overlay.pum-active")

    SIMPLE_MODAL_CONTAINER = (By.ID, "popmake-1318")
    SIMPLE_MODAL_TITLE = (By.ID, "pum_popup_title_1318")
    SIMPLE_MODAL_CONTENT = (By.CSS_SELECTOR, "#popmake-1318 .pum-content p")
    SIMPLE_MODAL_CLOSE_BTN = (By.CSS_SELECTOR, "#popmake-1318 button.pum-close")

    FORM_MODAL_CONTAINER = (By.ID, "popmake-674")
    FORM_MODAL_TITLE = (By.ID, "pum_popup_title_674")
    FORM_MODAL_CLOSE_BTN = (By.CSS_SELECTOR, "#popmake-674 button.pum-close")

    NAME_FIELD = (By.ID, "g1051-name")
    EMAIL_FIELD = (By.ID, "g1051-email")
    MESSAGE_FIELD = (By.ID, "contact-form-comment-g1051-message")
    SUBMIT_BTN = (By.CSS_SELECTOR, "#popmake-674 button.pushbutton-wide")

    FORM_ERROR = (By.CSS_SELECTOR, ".jetpack-contact-form .contact-form__error")
    NAME_ERROR = (By.ID, "g1051-name-text-error-message")
    EMAIL_ERROR = (By.ID, "g1051-email-email-error-message")

    SUCCESS_MESSAGE = (By.CSS_SELECTOR, "#popmake-674 .contact-form-submission, #popmake-674 .jetpack-form-success")

    @allure.step("Проверить сообщение об успешной отправке формы")
    def is_success_message_visible(self) -> bool:
        return self.is_element_available(self.SUCCESS_MESSAGE)

    @allure.step("Получить текст сообщения об успешной отправке формы")
    def get_success_message(self) -> str:
        return self.get_text(self.SUCCESS_MESSAGE)

    @allure.step("Открыть страницу Modals")
    def open_page(self) -> None:
        self.driver.get(self.URL)

    @allure.step("Клик по кнопке Simple Modal")
    def open_simple_modal(self) -> None:
        self.click(self.SIMPLE_MODAL_BTN)
        self.wait_for_simple_modal()

    @allure.step("Клик по кнопке Form Modal")
    def open_form_modal(self) -> None:
        self.click(self.FORM_MODAL_BTN)
        self.wait_for_form_modal()

    @allure.step("Проверить, что Simple Modal открыт")
    def is_simple_modal_visible(self) -> bool:
        return self.is_displayed(self.SIMPLE_MODAL_CONTAINER)

    @allure.step("Проверить, что Form Modal открыт")
    def is_form_modal_visible(self) -> bool:
        return self.is_displayed(self.FORM_MODAL_CONTAINER)

    @allure.step("Дождаться скрытия Simple Modal")
    def wait_for_simple_modal_hidden(self) -> bool:
        return self.wait_until_hidden(self.SIMPLE_MODAL_CONTAINER)

    @allure.step("Дождаться появления Simple Modal")
    def wait_for_simple_modal(self) -> bool:
        return self.wait_for_visible(self.SIMPLE_MODAL_CONTAINER)

    @allure.step("Дождаться появления Form Modal")
    def wait_for_form_modal(self) -> bool:
        return self.wait_for_visible(self.FORM_MODAL_CONTAINER)

    @allure.step("Клик по оверлею модального окна")
    def close_popup_with_overlay_click(self) -> None:
        self.click(self.MODAL_OVERLAY)

    @allure.step("Получить заголовок Simple Modal")
    def get_simple_modal_title(self) -> str:
        return self.get_text(self.SIMPLE_MODAL_TITLE)

    @allure.step("Получить текст контента Simple Modal")
    def get_simple_modal_content(self) -> str:
        return self.get_text(self.SIMPLE_MODAL_CONTENT)

    @allure.step("Закрыть Simple Modal крестиком")
    def close_simple_modal(self) -> None:
        self.click(self.SIMPLE_MODAL_CLOSE_BTN)

    @allure.step("Заполнить форму в Form Modal")
    def fill_contact_form(self, name: str = "", email: str = "", message: str = "") -> None:
        self.type_text(self.NAME_FIELD, name)
        self.type_text(self.EMAIL_FIELD, email)
        self.type_text(self.MESSAGE_FIELD, message)

    @allure.step("Отправить форму")
    def submit_form(self) -> None:
        self.click(self.SUBMIT_BTN)

    @allure.step("Получить сообщение об ошибке валидации формы")
    def get_form_validation_error(self) -> str:
        return self.get_text(self.FORM_ERROR)

    @allure.step("Получить текст ошибки поля Name")
    def get_name_error_text(self) -> str:
        return self.get_text(self.NAME_ERROR)

    @allure.step("Получить текст ошибки поля Email")
    def get_email_error_text(self) -> str:
        return self.get_text(self.EMAIL_ERROR)