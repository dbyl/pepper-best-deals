from pathlib import Path
import html5lib
import pytest
import datetime
from pytest_mock import mocker
from datetime import datetime, timedelta, date, timezone
from pepper_app.models import ScrapingStatistic
from pepper_app.populate_database import LoadScrapingStatisticsToDatabase


@pytest.fixture
def mock_utcnow(mocker):
    """Mocking datetime.utcnow()"""
    mock_datetime = mocker.patch("pepper_app.scrap.datetime")
    mock_datetime.utcnow.return_value.replace.return_value = datetime(2023, 8, 25, 12, 0, tzinfo=timezone.utc)
    return mock_datetime

@pytest.fixture
def loadscrapingstatisticstodatabase():
    stats_info = ["nowe", 1, 50, datetime(2023, 8, 25, 12, 0, tzinfo=timezone.utc),
                100, "NA", False, False, False, False]
    return LoadScrapingStatisticsToDatabase(stats_info)

@pytest.mark.django_db
def test_load_to_db_1(mocker, mock_utcnow, loadscrapingstatisticstodatabase):
    """Test loading stats_info into ScrapingStatistic table."""
    loadscrapingstatisticstodatabase.load_to_db()

    object_1 = ScrapingStatistic.objects.get(id=1)

    assert object_1.scrap_continuously == False
    assert object_1.category_type == "nowe"
    assert object_1.articles_to_retrieve == 50
    assert object_1.to_database == False
    assert object_1.to_csv == False
    assert object_1.to_statistics == False
    assert object_1.action_execution_datetime == 100

