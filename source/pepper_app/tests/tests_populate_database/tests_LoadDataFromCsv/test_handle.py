from pathlib import Path
import html5lib
import pytest
from datetime import datetime
from pepper_app.models import PepperArticle
from pepper_app.populate_database import LoadDataFromCsv

@pytest.fixture
def loaddatafromcsv():
    return LoadDataFromCsv()

def test_handle_1():


""" 
    def handle(self, *args, **options) -> None:
        path = options["input"]
        logging.info(f"Preparing data from {path}...")
        df = self.read_csv(path)
        self.load_to_db(df)
"""