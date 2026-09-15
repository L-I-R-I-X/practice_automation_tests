import allure
from selenium.webdriver.common.by import By
from selenium.common.exceptions import ElementClickInterceptedException, ElementNotInteractableException

from pages.base_page import BasePage


class AdsPage(BasePage):
    URL = "https://practice-automation.com/ads/"

    PAGE_HEADING = (By.CSS_SELECTOR, "h1[itemprop='headline']")
    COUNTDOWN_TEXT = (By.XPATH, "//p[contains(text(),'An ad will appear')]")
    AD_OVERLAY = (By.ID, "pum-1272")
    AD_CONTAINER = (By.ID, "popmake-1272")
    AD_TITLE = (By.ID, "pum_popup_title_1272")
    AD_CONTENT = (By.CSS_SELECTOR, "#popmake-1272 .pum-content p")
    AD_CLOSE_BTN = (By.CSS_SELECTOR, "#popmake-1272 button.pum-close")
    ENTRY_CONTENT = (By.CSS_SELECTOR, "div.entry-content")

    @allure.step("Открыть страницу Ads")
    def open_page(self) -> None:
        self.driver.get(self.URL)

    @allure.step("Проверить заголовок страницы Ads")
    def get_page_heading(self) -> str:
        return self.get_text(self.PAGE_HEADING)

    @allure.step("Проверить текст обратного отсчёта рекламы")
    def get_countdown_text(self) -> str:
        return self.get_text(self.COUNTDOWN_TEXT)

    @allure.step("Проверить, что рекламный попап появился")
    def is_ad_popup_visible(self) -> bool:
        return self.is_displayed(self.AD_CONTAINER)

    @allure.step("Дождаться появления рекламного попапа")
    def wait_for_ad_popup(self) -> bool:
        return self.wait_for_visible(self.AD_CONTAINER)

    @allure.step("Дождаться скрытия рекламного попапа")
    def wait_for_ad_popup_hidden(self) -> bool:
        return self.wait_until_hidden(self.AD_CONTAINER)

    @allure.step("Получить заголовок рекламного попапа")
    def get_ad_title(self) -> str:
        return self.get_text(self.AD_TITLE)

    @allure.step("Получить текст рекламного предложения")
    def get_ad_content(self) -> str:
        return self.get_text(self.AD_CONTENT)

    @allure.step("Проверить наличие кнопки закрытия попапа")
    def is_close_button_visible(self) -> bool:
        return self.is_element_available(self.AD_CLOSE_BTN)

    @allure.step("Закрыть попап кликом по крестику")
    def close_popup_with_button(self) -> None:
        self.click(self.AD_CLOSE_BTN)

    @allure.step("Закрыть попап кликом по оверлею")
    def close_popup_with_overlay_click(self) -> None:
        self.click(self.AD_OVERLAY)

    @allure.step("Проверить доступность основного контента страницы")
    def is_main_content_available(self) -> bool:
        return self.is_element_available(self.ENTRY_CONTENT)

    @allure.step("Попытаться кликнуть по заголовку страницы под оверлеем")
    def try_click_page_heading_under_overlay(self) -> None:
        try:
            self.click(self.PAGE_HEADING)
        except (ElementClickInterceptedException, ElementNotInteractableException):
            pass

    @allure.step("Закрыть попап нажатием ESC")
    def close_popup_with_escape(self) -> None:
        self.press_escape()