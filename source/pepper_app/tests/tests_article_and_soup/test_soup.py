from pathlib import Path
import html5lib
import pytest
from bs4 import BeautifulSoup, Tag
from pepper_app.tests.fixtures.to_test_article_and_soup import get_soup

@pytest.fixture
def soup():
    pass