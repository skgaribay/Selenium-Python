import pytest
from selenium import webdriver
from pages.page_object_manager import PageObjectManager
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions


def pytest_addoption(parser):
    parser.addoption(
        "--browser", action="store", default="chrome", help="Browser type: chrome or firefox"
    )


@pytest.fixture(scope="function")
def setup(request):
    browser = request.config.getoption("--browser").lower()

    if browser == "chrome":
        options = ChromeOptions()
        # options.add_argument('--headless')  # Optional: Run Chrome in headless mode
        driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)
    elif browser == "firefox":
        options = FirefoxOptions()
        # options.add_argument('--headless')  # Optional: Run Firefox in headless mode
        driver = webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install()), options=options)
    else:
        raise ValueError(f"Browser '{browser}' is not supported")

    driver.get("https://www.saucedemo.com/")
    driver.maximize_window()
    request.cls.page_manager = PageObjectManager(driver)
    request.cls.driver = driver
    yield
    driver.quit()
