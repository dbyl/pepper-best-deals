from pathlib import Path
import html5lib
from pytest_mock import mocker
import pytest
from datetime import datetime, timedelta, date, timezone
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


@pytest.fixture
def mock_utcnow(mocker):
    """Mocking datetime.utcnow()"""
    mock_datetime = mocker.patch("source.pepper_app.scrape.datetime")
    mock_datetime.utcnow.return_value.replace.return_value = datetime(2023, 8, 25, 12, 0, tzinfo=timezone.utc)
    return mock_datetime


def test_get_scraping_stats_info(mocker, mock_utcnow):
    """Test if correct stats info is returned."""
    category_type = "nowe"
    articles_to_retrieve = 50
    scrape_continuously = False
    to_database = False 
    to_csv = False
    to_statistics = False
    scrap_choosen_data = True
    action_execution_datetime = 100

    stats_info = ScrapePage(category_type=category_type, articles_to_retrieve=articles_to_retrieve, scrape_continuously=scrape_continuously, \
        to_database=to_database, to_csv=to_csv, to_statistics=to_statistics).get_scraping_stats_info(action_execution_datetime)
    
    assert stats_info == ["nowe", 50, datetime(2023, 8, 25, 12, 0, tzinfo=timezone.utc),
                            100, "NA", False, False, False, True]

