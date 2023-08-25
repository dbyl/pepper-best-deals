from pathlib import Path
import html5lib
from pytest_mock import mocker
import pytest
from bs4 import BeautifulSoup, Tag
import time
import pepper_app.scrap
from pepper_app.scrap import ScrapPage, CheckConditions



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

# Pytest fixtures
@pytest.fixture
def your_class_instance(monkeypatch):
    # Patching methods for the instance of YourClass
    monkeypatch.setattr(os.path, 'exists', mock_exists)
    monkeypatch.setattr(pd, 'read_csv', mock_read_csv)
    return YourClass()

# Pytest test cases
def test_save_data_to_csv_new_item(your_class_instance, monkeypatch):
    item = {'item_id': 123, 'name': 'Test Item'}
    your_class_instance.save_data_to_csv(item)

    # Assertion to check if the save_data_to_csv method behaves as expected
    # You need to add your own assertions based on the expected behavior
    assert os.path.exists("scraped.csv") == True


def test_save_data_to_csv_existing_item(your_class_instance, monkeypatch):
    item = {'item_id': 123, 'name': 'Test Item'}
    monkeypatch.setattr(MockDataFrame, 'tolist', lambda self: [[123]])
    your_class_instance.save_data_to_csv(item)

    # Assertion to check if the save_data_to_csv method behaves as expected
    # You need to add your own assertions based on the expected behavior
    assert True  # Replace this with your assertions

# Additional test cases can be added similarly




"""

    def save_data_to_csv(self, item) -> None:

        try:
            header = False
            if not os.path.exists('scraped.csv'):
                header = True
                df = pd.DataFrame([item], columns=CSV_COLUMNS)
                df.to_csv('scraped.csv', header=header, index=False, mode='a')
            else:
                header = False
                df_e = pd.read_csv('scraped.csv')
                df = pd.DataFrame([item], columns=CSV_COLUMNS)
                if df['item_id'][0] not in df_e['item_id'].tolist():
                    df.to_csv('scraped.csv', header=header, index=False, mode='a')
        except Exception as e:
            logging.warning(f"Saving data to csv failed: {e}\n Tracking: {traceback.format_exc()}")

"""