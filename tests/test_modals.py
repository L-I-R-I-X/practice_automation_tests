import allure
import pytest

from pages.form_fields_page import FormFieldsPage
from pages.modals_page import ModalsPage


@allure.feature("Страница Modals")
class TestModals:

    @allure.story("Simple Modal")
    class TestSimpleModal:

        @allure.title("Клик по кнопке Simple Modal открывает окно")
        def test_open_simple_modal(self, driver):
            app = ModalsPage(driver)
            app.open_page()

            app.open_simple_modal()

            assert app.is_simple_modal_visible()

        @allure.title("Simple Modal содержит ожидаемый текст приветствия")
        def test_simple_modal_greeting(self, driver):
            app = ModalsPage(driver)
            app.open_page()
            app.open_simple_modal()

            assert app.get_simple_modal_content().replace("\u2019", "'") == "Hi, I'm a simple modal."

        @allure.title("Simple Modal закрывается крестиком")
        def test_close_simple_modal(self, driver):
            app = ModalsPage(driver)
            app.open_page()
            app.open_simple_modal()

            app.close_simple_modal()

            assert app.wait_for_simple_modal_hidden()

        @allure.title("Клик по оверлею не закрывает Simple Modal")
        def test_simple_modal_not_closed_by_overlay(self, driver):
            app = ModalsPage(driver)
            app.open_page()
            app.open_simple_modal()

            app.close_popup_with_overlay_click()

            assert app.is_simple_modal_visible()

    @allure.story("Form Modal")
    class TestFormModal:

        @allure.title("Клик по кнопке Form Modal открывает окно с формой")
        def test_open_form_modal(self, driver):
            app = ModalsPage(driver)
            app.open_page()

            app.open_form_modal()

            assert app.is_form_modal_visible()

        @allure.title("Поле Name принимает ввод")
        def test_fill_name_field(self, driver):
            app = ModalsPage(driver)
            app.open_page()
            app.open_form_modal()

            app.type_text(app.NAME_FIELD, "John Doe")

            assert app.find_element(app.NAME_FIELD).get_attribute("value") == "John Doe"

        @allure.title("Поле Email принимает ввод")
        def test_fill_email_field(self, driver):
            app = ModalsPage(driver)
            app.open_page()
            app.open_form_modal()

            app.type_text(app.EMAIL_FIELD, "john.doe@example.com")

            assert app.find_element(app.EMAIL_FIELD).get_attribute("value") == "john.doe@example.com"

        @allure.title("Отправка формы с валидными данными завершается успехом")
        def test_submit_valid_form(self, driver):
            app = ModalsPage(driver)
            app.open_page()
            app.open_form_modal()

            app.fill_contact_form(name="John Doe", email="john.doe@example.com", message="Hello!")
            app.submit_form()

            assert app.is_success_message_visible()
            assert "Thank you for your response" in app.get_success_message()

    @allure.story("Валидация формы")
    class TestFormValidation:

        @pytest.mark.parametrize("name", ["", "   ", "\t\n"])
        @allure.title("Отправка формы с пустым именем name='{name}' отклоняется")
        def test_required_name(self, driver, name):
            app = ModalsPage(driver)
            app.open_page()
            app.open_form_modal()

            app.fill_contact_form(name=name, email="john.doe@example.com", message="Hello")
            app.submit_form()

            assert "required" in app.get_name_error_text().lower()

        @pytest.mark.parametrize("email", ["invalid", "test@", "@domain.com", "john doe@example.com", "john@.com"])
        @allure.title("Отправка формы с некорректным email='{email}' отклоняется")
        def test_invalid_email(self, driver, email):
            app = ModalsPage(driver)
            app.open_page()
            app.open_form_modal()

            app.fill_contact_form(name="John Doe", email=email, message="Hello")
            app.submit_form()

            assert app.get_email_error_text() == "Please enter a valid email address"


@allure.feature("Сквозной сценарий")
@allure.story("Спецзадание: текст из Form Fields в форму Modals")
class TestCrossPage:

    @allure.title("Текст списка инструментов отправляется через Form Modal")
    def test_tools_text_sent_via_form_modal(self, driver):
        form_fields = FormFieldsPage(driver)
        form_fields.open_page()

        tools_text = form_fields.get_joined_tools_text()
        assert "Selenium" in tools_text

        app = ModalsPage(driver)
        app.open_page()
        app.open_form_modal()

        app.type_text(app.NAME_FIELD, "QA Tester")
        app.type_text(app.MESSAGE_FIELD, tools_text)
        app.submit_form()

        assert "Thank you for your response" in app.get_success_message()