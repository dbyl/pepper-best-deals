from pathlib import Path
import html5lib
from pytest_mock import mocker
import time
from collections import Counter
from datetime import date, datetime, timezone
import pytest
import logging
from bs4 import BeautifulSoup, Tag
from source.pepper_app.scrape import (ScrapePage,
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
def retrived_articles_all():
    """Preparing article for tests."""
    path_to_file = Path("source/pepper_app/tests/fixtures/to_test_get_info/soup.html")
    with open(path_to_file, "r", encoding="utf-8") as file:
        soup = file.read()
    soup = BeautifulSoup(soup, "html5lib")
    articles = soup.find_all('article')
    retrived_articles = articles
    return retrived_articles


@pytest.fixture
def retrived_articles_with_duplicates():
    """Preparing article for tests."""
    path_to_file = Path("source/pepper_app/tests/fixtures/to_test_get_info/soup_with_duplicates.html")
    with open(path_to_file, "r", encoding="utf-8") as file:
        soup = file.read()
    soup = BeautifulSoup(soup, "html5lib")
    articles = soup.find_all('article')
    retrived_articles = articles
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


def test_get_items_details_1(retrived_articles_all):
    """Test if correct list filled with all items detailes is returned."""
    scrape_continuously = False
    category_type = "nowe"
    articles_to_retrieve = 50
    to_database=False
    to_csv=False
    to_statistics=False

    all_items = ScrapePage(category_type=category_type, articles_to_retrieve=articles_to_retrieve, scrape_continuously=scrape_continuously, \
        to_database=to_database, to_csv=to_csv, to_statistics=to_statistics).get_items_details(retrived_articles_all)

    date_1 = "2024-03-01"

    assert isinstance(all_items, list)
    assert len(all_items) == 30
    assert all_items[0] == [803602, "słuchawki soundcore p40i // 49 eur", 211.72,
                            -30.0, 302.41, date_1, "https://www.pepper.pl/promocje/soundcore-p40i-49-eur-803602"]


def test_get_items_details_2(retrived_articles_with_duplicates):
    """Test if no duplicates are returned."""
    scrape_continuously = False
    category_type = "nowe"
    articles_to_retrieve = 50
    to_database=False
    to_csv=False
    to_statistics=False


    all_items = ScrapePage(category_type=category_type, articles_to_retrieve=articles_to_retrieve, scrape_continuously=scrape_continuously, \
        to_database=to_database, to_csv=to_csv, to_statistics=to_statistics).get_items_details(retrived_articles_with_duplicates)

    count_duplicates = Counter(tuple(article) for article in all_items)

    assert len(retrived_articles_with_duplicates) == 31
    assert len(all_items) == 30
    assert any(val > 1 for val in count_duplicates.values()) == False


def test_get_items_details_3(caplog, retrived_articles_with_none_values):
    """Test if functions is broken if none values is in retrived articles."""
    scrape_continuously = False
    category_type = "nowe"
    articles_to_retrieve = 50
    to_database=False
    to_csv=False
    to_statistics=False

    caplog.set_level(logging.WARNING)
    logging.getLogger()

    ScrapePage(category_type=category_type, articles_to_retrieve=articles_to_retrieve, scrape_continuously=scrape_continuously, \
        to_database=to_database, to_csv=to_csv, to_statistics=to_statistics).get_items_details(retrived_articles_with_none_values)

    expected_message = "Data retrieving failed. None values detected"
    assert any(record.levelname == 'WARNING' and expected_message in record.message for record in caplog.records)

def test_get_items_details_4(mocker, retrived_articles_all):
    """Test if the correct function has been started when to csv is on."""
    scrape_continuously = False
    category_type = "nowe"
    articles_to_retrieve = 50
    to_database=False
    to_csv=True
    to_statistics=False

    save_data_to_csv_mock = mocker.patch("source.pepper_app.scrape.ScrapePage.save_data_to_csv")

    ScrapePage(category_type=category_type, articles_to_retrieve=articles_to_retrieve, scrape_continuously=scrape_continuously, \
        to_database=to_database, to_csv=to_csv, to_statistics=to_statistics).get_items_details(retrived_articles_all)

    save_data_to_csv_mock.assert_called()

def test_get_items_details_5(mocker, retrived_articles_all):
    """Test if the correct function has been started when saving data to database is on."""
    scrape_continuously = False
    category_type = "nowe"
    articles_to_retrieve = 50
    to_database=True
    to_csv=False
    to_statistics=False

    load_to_db_mock = mocker.patch("pepper_app.populate_database.LoadItemDetailsToDatabase.load_to_db")

    ScrapePage(category_type=category_type, articles_to_retrieve=articles_to_retrieve, scrape_continuously=scrape_continuously, \
        to_database=to_database, to_csv=to_csv, to_statistics=to_statistics).get_items_details(retrived_articles_all)

    load_to_db_mock.assert_called()

def test_get_items_details_6(mocker, retrived_articles_all):
    """Test if the correct function has been started when saving data to statistics is on."""
    scrape_continuously = False
    category_type = "nowe"
    articles_to_retrieve = 50
    to_database=False
    to_csv=False
    to_statistics=True

    load_statistics_to_db_mock = mocker.patch("pepper_app.populate_database.LoadScrapingStatisticsToDatabase.load_to_db")


    ScrapePage(category_type=category_type, articles_to_retrieve=articles_to_retrieve, scrape_continuously=scrape_continuously, \
        to_database=to_database, to_csv=to_csv, to_statistics=to_statistics).get_items_details(retrived_articles_all)

    load_statistics_to_db_mock.assert_called()

