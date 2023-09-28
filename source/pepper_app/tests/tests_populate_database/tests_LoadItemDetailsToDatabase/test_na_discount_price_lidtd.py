from pathlib import Path
import html5lib
import pytest
import datetime
import pandas as pd
from pepper_app.models import PepperArticle
from pepper_app.populate_database import LoadItemDetailsToDatabase



@pytest.fixture
def loaditemdetailstodatabase():
    item = [99999, "LG A1 55 cali", 3000.0, -10.0, 3300.0, "2023-08-31", "https://www.pepper.pl/promocje/lg-a1-55-719895"]
    return LoadItemDetailsToDatabase(item)


def test_na_discount_price_1(loaditemdetailstodatabase):
    """Test if function returns None if discount price is unknown."""
    row = pd.Series(data={'discount_price': 'NA'}, index=['discount_price'])
    output = loaditemdetailstodatabase.na_discount_price(row)

    assert output == None


def test_na_discount_price_2(loaditemdetailstodatabase):
    """Test if function returns correct value if discount price is known."""
    row = pd.Series(data={'discount_price': 3000.0}, index=['discount_price'])
    output = loaditemdetailstodatabase.na_discount_price(row)

    assert output == 3000.0

