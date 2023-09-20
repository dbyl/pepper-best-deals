from pathlib import Path
import html5lib
from pytest_mock import mocker
import pytest
from bs4 import BeautifulSoup, Tag
import pandas as pd
import os
import time
import source.pepper_app.scrap
import csv
from source.pepper_app.scrap import ScrapPage, CheckConditions




class MockDataFrame:
    def __init__(self, data, columns):
        self.data = data
        self.columns = columns

    def to_csv(self, *args, **kwargs):
        pass

    @property
    def iloc(self):
        return lambda idx: self.data[idx]

    @property
    def tolist(self):
        return self.data.tolist()

def mock_exists(filepath):
    return filepath == 'scraped.csv'

def mock_read_csv(filepath):
    if filepath == 'scraped.csv':
        return MockDataFrame([], columns=['item_id'])
    else:
        raise ValueError(f"Unexpected file: {filepath}")

@pytest.fixture
def mocking_class_instance(monkeypatch):
    """Patching methods for the instance of ScrapPage"""
    monkeypatch.setattr(os.path, 'exists', mock_exists)
    monkeypatch.setattr(pd, 'read_csv', mock_read_csv)

    category_type = "nowe"
    articles_to_retrieve = 50

    return ScrapPage(category_type=category_type, articles_to_retrieve=articles_to_retrieve)

def test_save_data_to_csv_new_item(mocking_class_instance, monkeypatch):
    """Test if csv file is created."""
    item = {'item_id': 123, 'name': 'Test Item'}
    mocking_class_instance.save_data_to_csv(item)

    assert os.path.exists("scraped.csv") == True


# write more tests here!
