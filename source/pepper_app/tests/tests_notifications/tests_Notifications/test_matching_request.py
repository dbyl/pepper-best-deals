from pathlib import Path
from unittest.mock import Mock
import pytest
from pepper_app.models import PepperArticle, UserRequest
from pepper_app.constans import DATA_HEADER
from django.utils import timezone
import pandas as pd
from source.pepper_app.notifications import Notifications
from pepper_app.populate_database import LoadItemDetailsToDatabase, LoadUserRequestToDatabase
from django.contrib.auth.models import User
from django.test import RequestFactory


@pytest.fixture
def user_A():
    # Create a user A for testing
    return User.objects.create_user(id=1, username='user_A', password='testpassword_A')

@pytest.fixture
def user_B():
    # Create a user B for testing
    return User.objects.create_user(id=2, username='testuser_B', password='testpassword_B')

@pytest.fixture
def client_A(user_A):
    # Create a Django test client A and log in the user
    from django.test import Client
    client = Client()
    client.login(username='user_A', password='testpassword_A')
    return client

@pytest.fixture
def client_B(user_B):
    # Create a Django test client B and log in the user
    from django.test import Client
    client = Client()
    client.login(username='testuser_B', password='testpassword_B')
    return client

@pytest.fixture
def rf_A(user_A):
    # Create a RequestFactory with the logged-in user
    request_factory = RequestFactory()
    request = request_factory.get('/')
    request.user = user_A
    return request

@pytest.fixture
def rf_B(user_B):
    # Create a RequestFactory with the logged-in user
    request_factory = RequestFactory()
    request = request_factory.get('/')
    request.user = user_B
    return request


@pytest.fixture
def mock_data_1(rf_A, rf_B):

    UserRequest.objects.create(request_id=10, desired_article="LG A1", desired_price=3100.00, 
                               minimum_price=1000.00, request_time=timezone.now(), user_id=rf_A.user)

    UserRequest.objects.create(request_id=11, desired_article="LG A1", desired_price=3200.00, 
                               minimum_price=0.00, request_time=timezone.now(), user_id=rf_B.user)


@pytest.mark.django_db
def test_matching_request(mock_data_1):
    """Comm."""

    data = [99999, "telewizor LG A1 55 cali", 3000.0, -10.0, 3300.0, "2023-08-31", "https://www.pepper.pl/promocje/lg-a1-55-719895"]
    item_df = pd.DataFrame([data], columns=DATA_HEADER)

    successful_responses = Notifications(item_df).matching_request()

    assert successful_responses.count() == 2


    successful_responses.delete()
