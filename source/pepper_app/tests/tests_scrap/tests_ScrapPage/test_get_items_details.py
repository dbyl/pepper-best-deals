from pathlib import Path
import html5lib
from pytest_mock import mocker
import time
from collections import Counter
from datetime import date, datetime, timezone
import pytest
import logging
from bs4 import BeautifulSoup, Tag
from pepper_app.scrap import (ScrapPage,
                            CheckConditions)
from pepper_app.populate_database import (LoadItemDetailsToDatabase,
                                        LoadScrapingStatisticsToDatabase)
from pepper_app.get_info import (GetItemAddedDate,
                                GetItemDiscountPrice,
                                GetItemId,
                                GetItemName,
                                GetItemPercentageDiscount,
                                GetItemRegularPrice,
                                GetItemUrl)

@pytest.fixture
def retrived_articles():
    """Preparing article for tests."""
    path_to_file = Path("source/pepper_app/tests/fixtures/to_test_get_info/soup.html")
    with open(path_to_file, "r", encoding="utf-8") as file:
        soup = file.read()
    soup = BeautifulSoup(soup, "html5lib")
    articles = soup.find_all('article')
    retrived_articles = articles[1:]
    return retrived_articles


@pytest.fixture
def retrived_articles_with_duplicates():
    """Preparing article for tests."""
    path_to_file = Path("source/pepper_app/tests/fixtures/to_test_get_info/soup_with_duplicates.html")
    with open(path_to_file, "r", encoding="utf-8") as file:
        soup = file.read()
    soup = BeautifulSoup(soup, "html5lib")
    articles = soup.find_all('article')
    retrived_articles = articles[1:]
    return retrived_articles


@pytest.fixture
def retrived_articles_with_none_values():
    """Preparing article for tests."""
    path_to_file = Path("source/pepper_app/tests/fixtures/to_test_get_info/soup_with_none.html")
    with open(path_to_file, "r", encoding="utf-8") as file:
        soup = file.read()
    soup = BeautifulSoup(soup, "html5lib")
    articles = soup.find_all('article')
    retrived_articles = articles[1:]
    return retrived_articles


def test_get_items_details_1(retrived_articles):
    """Test if correct list filled with all items detailes is returned."""
    scrap_continuously = False
    category_type = "nowe"
    articles_to_retrieve = 50
    to_database=False
    to_csv=False
    to_statistics=False

    all_items = ScrapPage(category_type=category_type, articles_to_retrieve=articles_to_retrieve, scrap_continuously=scrap_continuously, \
        to_database=to_database, to_csv=to_csv, to_statistics=to_statistics).get_items_details(retrived_articles)

    date_1 = str(date.today().strftime("%Y-%m-%d"))

    assert isinstance(all_items, list)
    assert len(all_items) == 29
    assert all_items[0] == [704487, "Zegarek sportowy Garmin Instinct 2 Solar", 1149.0,
                            -17.0, 1386.0, date_1, "https://www.pepper.pl/promocje/garmin-instinct-2-solar-704487"]


def test_get_items_details_2(retrived_articles_with_duplicates):
    """Test if no duplicates are returned."""
    scrap_continuously = False
    category_type = "nowe"
    articles_to_retrieve = 50
    to_database=False
    to_csv=False
    to_statistics=False


    all_items = ScrapPage(category_type=category_type, articles_to_retrieve=articles_to_retrieve, scrap_continuously=scrap_continuously, \
        to_database=to_database, to_csv=to_csv, to_statistics=to_statistics).get_items_details(retrived_articles_with_duplicates)

    count_duplicates = Counter(tuple(article) for article in all_items)

    assert len(all_items) == 29
    assert any(val > 1 for val in count_duplicates.values()) == False


def test_get_items_details_3(caplog, retrived_articles_with_none_values):
    """Test if functions is broken if none values is in retrived articles."""
    scrap_continuously = False
    category_type = "nowe"
    articles_to_retrieve = 50
    to_database=False
    to_csv=False
    to_statistics=False

    caplog.set_level(logging.WARNING)
    logging.getLogger()

    all_items = ScrapPage(category_type=category_type, articles_to_retrieve=articles_to_retrieve, scrap_continuously=scrap_continuously, \
        to_database=to_database, to_csv=to_csv, to_statistics=to_statistics).get_items_details(retrived_articles_with_none_values)

    expected_message = "Data retrieving failed. None values detected"
    assert any(record.levelname == 'WARNING' and expected_message in record.message for record in caplog.records)


def test_get_items_details_4(mocker, retrived_articles):
    """Test if the correct function has been started when to csv is on."""
    scrap_continuously = False
    category_type = "nowe"
    articles_to_retrieve = 50
    to_database=False
    to_csv=True
    to_statistics=False

    save_data_to_csv_mock = mocker.patch("pepper_app.scrap.ScrapPage.save_data_to_csv")

    all_items = ScrapPage(category_type=category_type, articles_to_retrieve=articles_to_retrieve, scrap_continuously=scrap_continuously, \
        to_database=to_database, to_csv=to_csv, to_statistics=to_statistics).get_items_details(retrived_articles)

    save_data_to_csv_mock.assert_called()


def test_get_items_details_5(mocker, retrived_articles):
    """Test if the correct function has been started when saving data to database is on."""
    scrap_continuously = False
    category_type = "nowe"
    articles_to_retrieve = 50
    to_database=True
    to_csv=False
    to_statistics=False

    load_to_db_mock = mocker.patch("pepper_app.populate_database.LoadItemDetailsToDatabase.load_to_db")

    all_items = ScrapPage(category_type=category_type, articles_to_retrieve=articles_to_retrieve, scrap_continuously=scrap_continuously, \
        to_database=to_database, to_csv=to_csv, to_statistics=to_statistics).get_items_details(retrived_articles)

    load_to_db_mock.assert_called()

@pytest.mark.django_db
def test_get_items_details_6(mocker, retrived_articles):
    """Test if the correct function has been started when saving data to statistics is on."""
    scrap_continuously = False
    category_type = "nowe"
    articles_to_retrieve = 50
    to_database=False
    to_csv=False
    to_statistics=True

    load_statistics_to_db_mock = mocker.patch("pepper_app.populate_database.LoadScrapingStatisticsToDatabase.load_to_db")
    get_scraping_stats_info_mock = mocker.patch("pepper_app.scrap.ScrapPage.get_scraping_stats_info")


    all_items = ScrapPage(category_type=category_type, articles_to_retrieve=articles_to_retrieve, scrap_continuously=scrap_continuously, \
        to_database=to_database, to_csv=to_csv, to_statistics=to_statistics).get_items_details(retrived_articles)

    load_statistics_to_db_mock.assert_called_once()

