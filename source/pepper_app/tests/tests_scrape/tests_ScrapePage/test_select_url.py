from pathlib import Path
import html5lib
import pytest
from bs4 import BeautifulSoup, Tag
from source.pepper_app.scrape import ScrapePage




def test_select_url_1():
    """Test if function returns correct url if scrape_continuously is True (on)."""
    scrape_continuously = True
    category_type = "nowe"
    articles_to_retrieve = 50
    url_to_scrape = ScrapePage(category_type=category_type, articles_to_retrieve=articles_to_retrieve,
                            scrape_continuously=scrape_continuously).select_url()

    assert url_to_scrape == "https://www.pepper.pl/nowe"


def test_select_url_2():
    """Test if function returns correct url if category_type is nowe."""
    scrape_continuously = False
    category_type = "nowe"
    articles_to_retrieve = 50
    url_to_scrape = ScrapePage(category_type=category_type, articles_to_retrieve=articles_to_retrieve,
                            scrape_continuously=scrape_continuously).select_url()

    assert url_to_scrape == "https://www.pepper.pl/nowe?page=1"


def test_select_url_3():
    """Test if function returns correct url if category_type is search."""
    scrape_continuously = False
    category_type = "search"
    articles_to_retrieve = 50
    searched_article = "s21"
    url_to_scrape = ScrapePage(category_type=category_type, articles_to_retrieve=articles_to_retrieve,
                            searched_article=searched_article, scrape_continuously=scrape_continuously).select_url()

    assert url_to_scrape == "https://www.pepper.pl/search?q=s21&page=1"


def test_select_url_4():
    """Test if function returns Exception if category_type is invalid."""
    scrape_continuously = False
    category_type = "other"
    articles_to_retrieve = 50
    searched_article = "s21"

    with pytest.raises(Exception) as exc_info:
        url_to_scrape = ScrapePage(category_type=category_type, articles_to_retrieve=articles_to_retrieve,
                            searched_article=searched_article, scrape_continuously=scrape_continuously).select_url()
    assert "The variables were defined incorrectly." in str(exc_info)


def test_select_url_5():
    """Test if function returns Exception if scrape_continuously is invalid."""
    scrape_continuously = "string instead of bool"
    category_type = "nowe"
    articles_to_retrieve = 50
    searched_article = "s21"

    with pytest.raises(Exception) as exc_info:
        url_to_scrape = ScrapePage(category_type=category_type, articles_to_retrieve=articles_to_retrieve,
                            searched_article=searched_article, scrape_continuously=scrape_continuously).select_url()
    assert "The variables were defined incorrectly." in str(exc_info)








