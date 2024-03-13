"""
  Tests for register user
  - api_client, authenticate and create_user are fixtures
  - api_client, authenticate is provided from conftest.py without any imports
"""

import tempfile

# External imports
from rest_framework import status
from PIL import Image
import pytest

# Internal imports
from core.constants import ROLE_ADMIN
from accounts.models import User


@pytest.fixture
def create_user(api_client):
    def receive_user_instance(instance):
        return api_client.post("/api/accounts/register/", instance)

    return receive_user_instance


@pytest.mark.django_db
class TestRegisterUser:
    def setUp(self):
        self.user = {"email": "test@example.com", "password": "1234"}

    def test_if_user_is_anonymous_returns_401(self, api_client, create_user):
        self.setUp()
        res = create_user(self.user)

        assert res.status_code == status.HTTP_401_UNAUTHORIZED

    def test_if_user_is_not_admin_returns_403(
        self, api_client, authenticate, create_user
    ):
        self.setUp()
        authenticate()

        res = create_user(self.user)

        assert res.status_code == status.HTTP_403_FORBIDDEN

    def test_if_user_is_admin_has_no_email_returns_400(
        self, api_client, authenticate, create_user
    ):
        authenticate(is_staff=True, role=ROLE_ADMIN)

        res = create_user({"email": "", "password": "1234"})

        assert res.status_code == status.HTTP_400_BAD_REQUEST

    def test_if_user_is_admin_has_no_password_returns_400(
        self, api_client, authenticate, create_user
    ):
        authenticate(is_staff=True, role=ROLE_ADMIN)

        res = create_user({"email": "test@example.com", "password": ""})

        assert res.status_code == status.HTTP_400_BAD_REQUEST

    def test_if_user_is_admin__has_valid_data_returns_201(
        self, api_client, authenticate, create_user
    ):
        self.setUp()
        authenticate(is_staff=True, role=ROLE_ADMIN)

        res = create_user(self.user)

        assert res.status_code == status.HTTP_201_CREATED

    def test_if_user_is_admin_upload_image_returns_201(
        self, api_client, authenticate, create_user, remove_image
    ):
        self.setUp()
        authenticate(is_staff=True, role=ROLE_ADMIN)

        with tempfile.NamedTemporaryFile(suffix=".jpg", delete=False) as avatar:
            img = Image.new("RGB", (100, 100), "white")
            img.save(avatar, "JPEG")
            avatar.seek(0)

            payload = {
                "email": self.user["email"],
                "password": self.user["password"],
                "avatar": avatar,
            }
            res = create_user(payload)
            assert res.status_code == status.HTTP_201_CREATED

            remove_image(res.data["avatar"])

    def test_if_user_is_admin_upload_invalid_image_returns_400(
        self, api_client, authenticate, create_user
    ):
        self.setUp()
        authenticate(is_staff=True, role=ROLE_ADMIN)

        with tempfile.NamedTemporaryFile(suffix=".jpg") as avatar:
            avatar.write(b"invalid file content")
            avatar.seek(0)

            payload = {
                "email": self.user["email"],
                "password": self.user["password"],
                "avatar": avatar,
            }
            res = create_user(payload)

            assert res.status_code == status.HTTP_400_BAD_REQUEST


@pytest.fixture
def verify_user(api_client):
    def receive_user_instance(instance):
        return api_client.post("/api/accounts/login/", instance)

    return receive_user_instance


@pytest.mark.django_db
class TestLoginUser:
    def setUp(self):
        self.user = {"email": "test@example.com", "password": "1234"}
        User.objects.create_user(**self.user)

    def test_if_user_email_is_null_or_empty_returns_400(self, api_client, verify_user):
        self.setUp()

        res = verify_user(
            {"email": "", "password": self.user["password"]},
        )

        assert res.status_code == status.HTTP_400_BAD_REQUEST

    def test_if_user_password_is_null_or_empty_returns_400(
        self, api_client, verify_user
    ):
        self.setUp()

        res = verify_user(
            {"email": self.user["email"], "password": ""},
        )

        assert res.status_code == status.HTTP_400_BAD_REQUEST

    def test_if_user_email_is_invalid_returns_401(self, api_client, verify_user):
        self.setUp()

        res = verify_user(
            {"email": "test1234@example.com", "password": self.user["password"]},
        )

        assert res.status_code == status.HTTP_401_UNAUTHORIZED

    def test_if_user_password_is_invalid_returns_401(self, api_client, verify_user):
        self.setUp()

        res = verify_user(
            {"email": self.user["email"], "password": "12"},
        )

        assert res.status_code == status.HTTP_401_UNAUTHORIZED

    def test_if_user_is_valid_returns_200(self, api_client, verify_user):
        self.setUp()

        res = verify_user(self.user)

        assert res.status_code == status.HTTP_200_OK
        assert res.data["email"] == self.user["email"]
        assert "refresh" in res.data["tokens"]
        assert "access" in res.data["tokens"]
