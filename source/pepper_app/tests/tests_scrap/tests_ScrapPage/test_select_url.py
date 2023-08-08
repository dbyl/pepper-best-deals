from pathlib import Path
import html5lib
import pytest
from bs4 import BeautifulSoup, Tag
from pepper_app.scrap import ScrapPage




def test_select_url_1():
    """Test if function returns correct url if scrap_continuously is True (on)."""
    scrap_continuously = True
    category_type = "nowe"
    articles_to_retrieve = 50
    url_to_scrap = ScrapPage(category_type=category_type, articles_to_retrieve=articles_to_retrieve,
                            scrap_continuously=scrap_continuously).select_url()

    assert url_to_scrap == "https://www.pepper.pl/nowe"

def test_select_url_2():
    """Test if function returns correct url if category_type is nowe."""
    scrap_continuously = False
    category_type = "nowe"
    articles_to_retrieve = 50
    url_to_scrap = ScrapPage(category_type=category_type, articles_to_retrieve=articles_to_retrieve,
                            scrap_continuously=scrap_continuously).select_url()

    assert url_to_scrap == "https://www.pepper.pl/nowe?page=1"

def test_select_url_3():
    """Test if function returns correct url if category_type is search."""
    scrap_continuously = False
    category_type = "search"
    articles_to_retrieve = 50
    searched_article = "s21"
    url_to_scrap = ScrapPage(category_type=category_type, articles_to_retrieve=articles_to_retrieve,
                            searched_article=searched_article, scrap_continuously=scrap_continuously).select_url()

    assert url_to_scrap == "https://www.pepper.pl/search?q=s21&page=1"

def test_select_url_4():
    """Test if function returns Exception if category_type is invalid."""
    scrap_continuously = False
    category_type = "other"
    articles_to_retrieve = 50
    searched_article = "s21"

    with pytest.raises(Exception) as exc_info:
        url_to_scrap = ScrapPage(category_type=category_type, articles_to_retrieve=articles_to_retrieve,
                            searched_article=searched_article, scrap_continuously=scrap_continuously).select_url()
    assert "The variables were defined incorrectly." in str(exc_info)

def test_select_url_5():
    """Test if function returns Exception if scrap_continuously is invalid."""
    scrap_continuously = "string instead of bool"
    category_type = "nowe"
    articles_to_retrieve = 50
    searched_article = "s21"

    with pytest.raises(Exception) as exc_info:
        url_to_scrap = ScrapPage(category_type=category_type, articles_to_retrieve=articles_to_retrieve,
                            searched_article=searched_article, scrap_continuously=scrap_continuously).select_url()
    assert "The variables were defined incorrectly." in str(exc_info)








