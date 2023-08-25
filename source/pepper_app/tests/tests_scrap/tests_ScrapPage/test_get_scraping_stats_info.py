from pathlib import Path
import html5lib
from pytest_mock import mocker
import pytest
from datetime import datetime, timedelta, date, timezone
from bs4 import BeautifulSoup, Tag
from pepper_app.scrap import ScrapPage, CheckConditions


@pytest.fixture
def soup():
    """Preparing article for tests."""
    path_to_file = Path("pepper_app/tests/fixtures/to_test_scrap/soup.html")
    with open(path_to_file, "r", encoding="utf-8") as file:
        soup = file.read()
    soup = BeautifulSoup(soup, "html5lib")
    return soup


@pytest.fixture
def mock_utcnow(mocker):
    """Mocking datetime.utcnow()"""
    mock_datetime = mocker.patch("pepper_app.scrap.datetime")
    mock_datetime.utcnow.return_value.replace.return_value = datetime(2023, 8, 25, 12, 0, tzinfo=timezone.utc)
    return mock_datetime


def test_get_scraping_stats_info(mocker, mock_utcnow):
    """Test if correct stats info is returned."""
    scrap_continuously = False
    category_type = "nowe"
    articles_to_retrieve = 50
    to_database = False
    to_csv = False
    to_statistics = False
    action_execution_datetime = 100

    stats_info = ScrapPage(category_type=category_type, articles_to_retrieve=articles_to_retrieve, scrap_continuously=scrap_continuously, \
        to_database=to_database, to_csv=to_csv, to_statistics=to_statistics).get_scraping_stats_info(action_execution_datetime)

    assert stats_info == ["nowe", 1, 50, datetime(2023, 8, 25, 12, 0, tzinfo=timezone.utc),
                            100, "NA", False, False, False, False]

