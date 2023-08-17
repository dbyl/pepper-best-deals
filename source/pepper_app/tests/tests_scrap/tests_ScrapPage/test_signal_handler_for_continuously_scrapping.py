from pathlib import Path
import html5lib
from pytest_mock import mocker
import time
import pytest
import signal
from bs4 import BeautifulSoup, Tag
from pepper_app.scrap import ScrapPage, CheckConditions


"""
    def signal_handler_for_continuously_scrapping(signal, frame):
        global interrupted
        interrupted = True
"""

def test_signal_handler_for_continuously_scrapping_1(monkeypatch, mocker):
    """Test signal handler for continuously scrapping if interruptor is global variable set on True."""
    category_type = "nowe"
    articles_to_retrieve = 50

    #signal_handler_for_continuously_scrapping_mock = mocker.patch("pepper_app.scrap.ScrapPage.signal_handler_for_continuously_scrapping")

    interrupted = False
    ScrapPage(category_type=category_type, articles_to_retrieve=articles_to_retrieve).signal_handler_for_continuously_scrapping()

    assert interrupted == True