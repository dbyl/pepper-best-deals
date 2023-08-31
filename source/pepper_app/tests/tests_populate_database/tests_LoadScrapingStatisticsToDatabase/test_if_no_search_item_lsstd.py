from pathlib import Path
import html5lib
import pytest
import datetime
import pandas as pd
from pepper_app.models import ScrapingStatistic
from pepper_app.populate_database import LoadScrapingStatisticsToDatabase



@pytest.fixture
def loadscrapingstatisticstodatabase():
    stats_info = ["nowe", 1, 50, datetime(2023, 8, 25, 12, 0, tzinfo=timezone.utc),
                100, "NA", False, False, False, False]
    return LoadScrapingStatisticsToDatabase(stats_info)


def test_if_no_search_item_1(loadscrapingstatisticstodatabase):
    """Test if the function returns None if there was no article search and scrapping was in the "nowe" category."""
    row = pd.Series(data={'category_type': 'nowe'}, index=['category_type'])
    output = loadscrapingstatisticstodatabase.if_no_search_item(row)

    assert output == None


def test_if_no_search_item_2(loadscrapingstatisticstodatabase):
    """Test whether the function returns the name of the searched article if the scrapping involved the search."""
    row = pd.Series(data={'searched_article': 'Samsung S22'}, index=['searched_article'])
    output = loadscrapingstatisticstodatabase.if_no_search_item(row)

    assert output == "Samsung S22"
