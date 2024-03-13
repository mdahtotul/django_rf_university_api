import pytest
import os
from rest_framework.test import APIClient

from core.constants import ROLE_USER
from core.settings import BASE_DIR
from accounts.models import User


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def authenticate(api_client):
    def do_authenticate(is_staff=False, role=ROLE_USER):
        return api_client.force_authenticate(user=User(is_staff=is_staff, role=role))

    return do_authenticate


@pytest.fixture
def create_user_db(api_client):
    def receive_instance(instance):
        return User.objects.create_user(**instance)

    return receive_instance


@pytest.fixture()
def remove_image():
    def remove_file(file_path):
        path = f"{BASE_DIR}{file_path}"
        os.remove(path)

    return remove_file
