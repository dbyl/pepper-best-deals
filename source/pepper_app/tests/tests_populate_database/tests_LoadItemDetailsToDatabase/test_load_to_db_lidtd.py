from pathlib import Path
import html5lib
import pytest
import datetime
from pepper_app.models import PepperArticle
from pepper_app.populate_database import LoadItemDetailsToDatabase


@pytest.fixture
def loaditemdetailstodatabase():
    item = [99999, "LG A1 55 cali", 3000.0, -10.0, 3300.0, "2023-08-31", "https://www.pepper.pl/promocje/lg-a1-55-719895"]
    return LoadItemDetailsToDatabase(item)

@pytest.mark.django_db
def test_load_to_db_1(loaditemdetailstodatabase):
    """Test loading item into PepperArticle table."""
    loaditemdetailstodatabase.load_to_db()

    object_1 = PepperArticle.objects.get(item_id=99999)

    assert object_1.name == "LG A1 55 cali"
    assert object_1.discount_price == 3000.0
    assert object_1.percentage_discount == -10.0
    assert object_1.regular_price == 3300.0
    assert object_1.date_added == datetime.date(2023, 8, 31)
    assert object_1.url == "https://www.pepper.pl/promocje/lg-a1-55-719895"

    object_1.delete()
