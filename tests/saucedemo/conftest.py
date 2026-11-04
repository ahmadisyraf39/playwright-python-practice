import pytest
from playwright.sync_api import Playwright


@pytest.fixture(scope="session", autouse=True)
def use_data_test_attribute(playwright: Playwright):
    playwright.selectors.set_test_id_attribute("data-test")