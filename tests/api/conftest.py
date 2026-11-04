import pytest
from playwright.sync_api import Playwright, APIRequestContext

BASE_URL = "https://restful-booker.herokuapp.com"


@pytest.fixture(scope="session")
def api(playwright: Playwright):
    context = playwright.request.new_context(base_url=BASE_URL)
    yield context          # the tests run here
    context.dispose()      # always runs afterwards, even if tests failed