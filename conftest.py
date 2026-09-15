import glob
import os

import allure
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager


def _cached_driver(binary_name: str) -> str | None:
    matches = sorted(glob.glob(os.path.expanduser(f"~/.wdm/drivers/*/linux64/*/{binary_name}")),
                     key=os.path.getmtime, reverse=True)
    return matches[0] if matches else None


def pytest_addoption(parser):
    parser.addoption(
        "--browser",
        action="store",
        default="chrome",
        choices=["chrome", "firefox"],
        help="Browser to run tests in: chrome or firefox",
    )
    parser.addoption(
        "--headless",
        action="store_true",
        default=False,
        help="Run browser in headless mode",
    )


@pytest.fixture(scope="function")
def driver(request):
    browser = request.config.getoption("--browser")
    headless = request.config.getoption("--headless")

    if browser == "firefox":
        options = FirefoxOptions()
        if headless:
            options.add_argument("--headless")
        if os.environ.get("FIREFOX_NO_PROXY") == "1":
            options.set_preference("network.proxy.type", 0)
        options.set_capability("pageLoadStrategy", "eager")
        cached = _cached_driver("geckodriver")
        executable_path = cached if cached else GeckoDriverManager().install()
        service = FirefoxService(executable_path=executable_path)
        driver = webdriver.Firefox(service=service, options=options)
    else:
        options = ChromeOptions()
        if headless:
            options.add_argument("--headless=new")
        options.set_capability("pageLoadStrategy", "eager")
        cached = _cached_driver("chromedriver")
        executable_path = cached if cached else ChromeDriverManager().install()
        service = ChromeService(executable_path=executable_path)
        driver = webdriver.Chrome(service=service, options=options)

    driver.maximize_window()
    driver.set_page_load_timeout(60)
    driver.implicitly_wait(5)

    yield driver

    driver.quit()


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()

    if report.when == "call" and report.failed:
        driver_instance = item.funcargs.get("driver")
        if driver_instance is not None:
            screenshot = driver_instance.get_screenshot_as_png()
            allure.attach(
                screenshot,
                name="screenshot_on_failure",
                attachment_type=allure.attachment_type.PNG,
            )