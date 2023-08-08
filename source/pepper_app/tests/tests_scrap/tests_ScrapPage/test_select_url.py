from pathlib import Path
import html5lib
import pytest
from bs4 import BeautifulSoup, Tag
from pepper_app.scrap import ScrapPage




def test_select_url_1(scrap_continuously_true):
    """Test if function returns correct url if scrap_continuously is True (on)."""
    scrap_continuously = True
    category_type = "nowe"
    articles_to_retrieve = 50
    url_to_scrap = ScrapPage(category_type=category_type, articles_to_retrieve=articles_to_retrieve,
                            scrap_continuously=scrap_continuously).select_url()

    assert url_to_scrap == "https://www.pepper.pl/nowe"

def test_select_url_2(scrap_continuously_true):
    """Test if function returns correct url if scrap_continuously is True (on)."""
    scrap_continuously = True
    category_type = "nowe"
    articles_to_retrieve = 50
    url_to_scrap = ScrapPage(category_type=category_type, articles_to_retrieve=articles_to_retrieve,
                            scrap_continuously=scrap_continuously).select_url()

    assert url_to_scrap == "https://www.pepper.pl/nowe"

def test_select_url_3(scrap_continuously_true):
    """Test if function returns correct url if scrap_continuously is True (on)."""
    scrap_continuously = True
    category_type = "nowe"
    articles_to_retrieve = 50
    url_to_scrap = ScrapPage(category_type=category_type, articles_to_retrieve=articles_to_retrieve,
                            scrap_continuously=scrap_continuously).select_url()

    assert url_to_scrap == "https://www.pepper.pl/nowe"






