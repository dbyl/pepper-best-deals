from pathlib import Path
import html5lib
import pytest
import datetime
from pytest_mock import mocker
from datetime import datetime, timedelta, date, timezone
import pandas as pd
from pepper_app.models import ScrapingStatistic
from pepper_app.populate_database import LoadScrapingStatisticsToDatabase


@pytest.fixture
def loadscrapingstatisticstodatabase():
    stats_info = ["nowe", 1, 50, datetime(2023, 8, 25, 12, 0, tzinfo=timezone.utc),
                100, "NA", False, False, False, False]
    return LoadScrapingStatisticsToDatabase(stats_info)

@pytest.fixture
def loadscrapingstatisticstodatabasesearch():
    stats_info = ["search", 1, 50, "2021-07-05",
                100, "Samsung S22", False, False, False, False]
    return LoadScrapingStatisticsToDatabase(stats_info)


def test_if_no_search_item_1(loadscrapingstatisticstodatabase):
    """Test if the function returns None if there was no article search and scrapping was in the "nowe" category."""
    row = pd.Series(data={'category_type': 'nowe'}, index=['category_type'])
    output = loadscrapingstatisticstodatabase.if_no_search_item(row)

    assert output == None


def test_if_no_search_item_2(loadscrapingstatisticstodatabasesearch):
    """Test whether the function returns the name of the searched article if the scrapping involved the search."""
    row = pd.Series(data={'category_type': 'search', 'searched_article': 'Samsung S22'}, index=['category_type','searched_article'])
    output = loadscrapingstatisticstodatabasesearch.if_no_search_item(row)

    assert output == "Samsung S22"
