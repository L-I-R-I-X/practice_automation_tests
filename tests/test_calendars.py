import re

import allure
import pytest

from pages.calendars_page import CalendarsPage


@allure.feature("Страница Calendars")
@allure.story("Поле выбора даты")
class TestCalendars:

    @allure.title("Успешная загрузка страницы Calendars")
    def test_page_loads_successfully(self, driver):
        app = CalendarsPage(driver)
        app.open_page()

        assert "Select or enter a date" in app.get_text(app.DATE_FIELD_LABEL)
        assert app.get_format_hint() == "YYYY-MM-DD"

    @allure.title("Поле даты принимает ручной ввод в формате YYYY-MM-DD")
    def test_manual_date_entry(self, driver):
        app = CalendarsPage(driver)
        app.open_page()

        app.enter_date_manually("2025-03-15")

        assert app.get_date_value() == "2025-03-15"

    @allure.title("Отправка формы с корректной датой завершается успехом")
    def test_submit_valid_date(self, driver):
        app = CalendarsPage(driver)
        app.open_page()

        app.enter_date_manually("2025-03-15")
        app.submit_form()

        assert "Thank you for your response" in app.wait_for_success_message()

    @pytest.mark.parametrize("invalid_date", ["15-03-2025", "03/15/2025", "2025-03",
                                              "2025.03.15", "invalid", "2025-13-45"])
    @allure.title("Некорректный формат даты '{invalid_date}' отклоняется")
    def test_invalid_date_rejected(self, driver, invalid_date):
        app = CalendarsPage(driver)
        app.open_page()

        app.enter_date_manually(invalid_date)
        app.submit_form()

        assert app.get_date_field_error() != ""
        assert "date" in app.get_date_field_error().lower()