from pathlib import Path
import html5lib
from pytest_mock import mocker
import pytest
from bs4 import BeautifulSoup, Tag
import time
import source.pepper_app.scrape
from source.pepper_app.scrape import ScrapePage, CheckConditions


@pytest.fixture
def soup():
    """Preparing article for tests."""
    path_to_file = Path("source/pepper_app/tests/fixtures/to_test_scrape/soup.html")
    with open(path_to_file, "r", encoding="utf-8") as file:
        soup = file.read()
    soup = BeautifulSoup(soup, "html5lib")
    return soup

def test_scrape_continuously_by_refreshing_page_1(monkeypatch, mocker, soup):
    """Test scrape continuously by refreshing page if correct list filled with articles is returned."""

    def mock_sleep(seconds):
        pass

    monkeypatch.setattr(time, "sleep", mock_sleep)

    category_type = "nowe"
    articles_to_retrieve = 50

    scrape_page_mock = mocker.patch("source.pepper_app.scrap.ScrapPage.scrape_page")

    scrape_page_mock.return_value = soup

    retrived_articles = ScrapePage(category_type=category_type, articles_to_retrieve=articles_to_retrieve).scrape_continuously_by_refreshing_page()

    assert isinstance(retrived_articles, list)
    assert len(retrived_articles) > 0

