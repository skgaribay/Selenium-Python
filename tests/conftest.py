import pytest
from selenium import webdriver
from pages.page_object_manager import PageObjectManager
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options


@pytest.fixture(scope="function")
def setup(request):
    options = Options()
    options.add_argument('--headless')
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.get("https://www.saucedemo.com/")
    driver.maximize_window()
    request.cls.page_manager = PageObjectManager(driver)
    request.cls.driver = driver
    yield
    driver.quit()
