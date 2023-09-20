from pathlib import Path
import html5lib
import pytest
import time
from bs4 import BeautifulSoup, Tag
from source.pepper_app.tests.fixtures.to_test_article_and_soup import get_soup


get_soup.get_current_soup() #Collecting current soup.


@pytest.fixture
def current_list_of_articles():
    """Setting environment up."""
    time.sleep(0.7)
    path_to_file = Path("pepper_app/tests/fixtures/to_test_article_and_soup/soup_to_check.html")
    with open(path_to_file, "r", encoding="utf-8") as file:
        current_soup = file.read()
    current_soup = BeautifulSoup(current_soup, "html5lib")
    current_list_of_articles = current_soup.find_all('article')
    return current_list_of_articles


def test_if_valid_class_with_name_exists(current_list_of_articles):
    """Test if valid class with item name exists."""
    bad, ok = 0, 0

    for article in current_list_of_articles:
        if article.find_all(attrs={'class': "cept-tt thread-link linkPlain thread-title--list js-thread-title"}):
            ok += 1
        else:
            bad += 1

    assert bad == 0
    assert ok > 0


def test_if_valid_class_with_id_exists(current_list_of_articles):
    """Test if valid class with item id exists."""
    bad, ok = 0, 0

    for article in current_list_of_articles:
        if article.get("id"):
            ok += 1
        else:
            bad += 1

    assert bad == 0
    assert ok > 0


def test_if_valid_class_with_discount_price_exists(current_list_of_articles):
    """Test if valid class with item discount price exists."""
    bad, ok = 0, 0

    for article in current_list_of_articles:
        if article.find_all(attrs={'class': "thread-price text--b cept-tp size--all-l size--fromW3-xl"}):
            ok += 1
        else:
            bad += 1

    assert bad >= 0
    assert ok > 0


def test_if_valid_class_with_regular_price_exists(current_list_of_articles):
    """Test if valid class with item regular price exists."""
    bad, ok = 0, 0

    for article in current_list_of_articles:
        if article.find_all(attrs={'class': "mute--text text--lineThrough size--all-l size--fromW3-xl"}):
            ok += 1
        else:
            bad += 1

    assert bad >= 0
    assert ok > 0


def test_if_valid_class_with_percentage_discount_exists(current_list_of_articles):
    """Test if valid class with item percentage discount exists."""
    bad, ok = 0, 0

    for article in current_list_of_articles:
        if article.find_all(attrs={'class': "space--ml-1 size--all-l size--fromW3-xl"}):
            ok += 1
        else:
            bad += 1

    assert bad >= 0
    assert ok > 0


def test_if_valid_class_with_url_exists(current_list_of_articles):
    """Test if valid class with item url exists."""
    bad, ok = 0, 0

    for article in current_list_of_articles:
        if article.find_all("a", {"class":"cept-tt thread-link linkPlain thread-title--list js-thread-title"}):
            ok += 1
        else:
            bad += 1

    assert bad == 0
    assert ok > 0


def test_if_valid_class_with_added_date_exists(current_list_of_articles):
    """Test if valid class with item added date exists."""
    bad, ok = 0, 0

    for article in current_list_of_articles:
        if article.find_all('div', {"class":"size--all-s flex boxAlign-jc--all-fe boxAlign-ai--all-c flex--grow-1 overflow--hidden"}):
            ok += 1
        else:
            bad += 1

    assert bad >= 0
    assert ok > 0