import pytest
from rest_framework.test import APIClient

from core.constants import ROLE_USER
from account.models import User


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def authenticate(api_client):
    def do_authenticate(is_staff=False, role=ROLE_USER):

        return api_client.force_authenticate(user=User(is_staff=is_staff, role=role))

    return do_authenticate
