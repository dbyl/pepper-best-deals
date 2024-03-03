from pathlib import Path
import html5lib
from pytest_mock import mocker
import time
import pytest
from bs4 import BeautifulSoup, Tag
from source.pepper_app.scrape import ScrapePage, CheckConditions


@pytest.fixture
def soup():
    """Preparing article for tests."""
    path_to_file = Path("pepper_app/tests/fixtures/to_test_scrape/soup.html")
    with open(path_to_file, "r", encoding="utf-8") as file:
        soup = file.read()
    soup = BeautifulSoup(soup, "html5lib")
    return soup


def test_get_items_details_depending_on_the_function_1(monkeypatch, mocker):
    """Test get items details depending on the function whether the correct function has been started."""
    category_type = "nowe"
    articles_to_retrieve = 50
    scrap_continuously = False
    scrap_choosen_data = True

    def mock_sleep(seconds):
        """Mocking time sleep."""
        pass

    monkeypatch.setattr(time, "sleep", mock_sleep)

    infinite_scroll_handling_mock = mocker.patch("pepper_app.scrape.ScrapePage.infinite_scroll_handling")
    get_items_details_mock = mocker.patch("pepper_app.scrape.ScrapePage.get_items_details")

    ScrapePage(category_type=category_type, articles_to_retrieve=articles_to_retrieve, \
        scrape_continuously=scrape_continuously, scrape_choosen_data=scrape_choosen_data).get_items_details_depending_on_the_function()

    get_items_details_mock.assert_called_once()
    infinite_scroll_handling_mock.assert_called_once()


# write more tests here!


