import pytest
import os
from rest_framework.test import APIClient

from core.constants import BASE_DIR, ROLE_USER
from accounts.models import User


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def authenticate(api_client):
    def do_authenticate(is_staff=False, role=ROLE_USER):
        return api_client.force_authenticate(user=User(is_staff=is_staff, role=role))

    return do_authenticate


@pytest.fixture()
def remove_image():
    def remove_file(file_path):
        path = f"{BASE_DIR}{file_path}"
        os.remove(path)

    return remove_file
