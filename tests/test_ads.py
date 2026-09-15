import time

import allure
import pytest

from pages.ads_page import AdsPage


@allure.feature("Страница Ads")
@allure.story("Рекламный попап")
class TestAdsPage:

    @allure.title("Успешная загрузка страницы Ads")
    def test_page_loads_successfully(self, driver):
        app = AdsPage(driver)

        app.open_page()

        assert app.get_page_heading() == "Ads"
        assert "An ad will appear" in app.get_countdown_text()

    @allure.title("Рекламный попап появляется по истечении таймаута")
    def test_ad_popup_appears_after_timeout(self, driver):
        app = AdsPage(driver)
        app.open_page()

        assert not app.is_ad_popup_visible()

        started = time.monotonic()
        appeared = app.wait_for_ad_popup()
        elapsed = time.monotonic() - started

        assert appeared
        assert elapsed >= 4.0, f"Попап появился слишком рано: {elapsed:.2f}с"

    @allure.title("Текст рекламного попапа соответствует ожидаемому")
    def test_ad_popup_text_matches_expected(self, driver):
        app = AdsPage(driver)
        app.open_page()
        app.wait_for_ad_popup()

        assert app.get_ad_title() == "Hi"
        assert app.get_ad_content() == "I am an ad."

    @allure.title("В попапе присутствует кнопка закрытия")
    def test_close_button_present(self, driver):
        app = AdsPage(driver)
        app.open_page()
        app.wait_for_ad_popup()

        assert app.is_close_button_visible()

    @allure.title("Попап закрывается кликом по крестику")
    def test_popup_closes_via_close_button(self, driver):
        app = AdsPage(driver)
        app.open_page()
        app.wait_for_ad_popup()

        app.close_popup_with_button()

        assert app.wait_for_ad_popup_hidden()

    @allure.title("Клик по оверлею не закрывает попап (конфигурация попапа)")
    def test_overlay_click_blocked(self, driver):
        app = AdsPage(driver)
        app.open_page()
        app.wait_for_ad_popup()

        app.close_popup_with_overlay_click()

        assert app.is_ad_popup_visible()
        app.close_popup_with_button()

    @allure.title("Основной контент страницы доступен после закрытия попапа")
    def test_main_content_available_after_close(self, driver):
        app = AdsPage(driver)
        app.open_page()
        app.wait_for_ad_popup()

        app.close_popup_with_button()
        app.wait_for_ad_popup_hidden()

        assert app.is_main_content_available()

    @allure.title("Пока попап открыт, клики перехватываются оверлеем")
    def test_focus_interception_while_popup_open(self, driver):
        app = AdsPage(driver)
        app.open_page()
        app.wait_for_ad_popup()

        app.try_click_page_heading_under_overlay()

        assert app.is_ad_popup_visible()

    @allure.title("ESC не закрывает рекламный попап (закрытие не настроено)")
    def test_escape_does_not_close_popup(self, driver):
        app = AdsPage(driver)
        app.open_page()
        app.wait_for_ad_popup()

        app.close_popup_with_escape()

        assert app.is_ad_popup_visible()
        app.close_popup_with_button()

    @allure.title("Попап не появляется повторно после закрытия")
    def test_popup_does_not_duplicate_after_close(self, driver):
        app = AdsPage(driver)
        app.open_page()
        app.wait_for_ad_popup()

        app.close_popup_with_button()
        app.wait_for_ad_popup_hidden()

        time.sleep(5.5)
        assert not app.is_ad_popup_visible()