import tempfile

# External imports
from rest_framework import status
from PIL import Image
from model_bakery import baker
import pytest

# Internal imports
from core.constants import ROLE_ADMIN, ROLE_STAFF
from accounts.models import User


@pytest.fixture
def retrieve_and_update_user(api_client):
    def receive_instance(instance, id=None):
        return api_client.patch(f"/api/accounts/details/{id}/", instance)

    return receive_instance


@pytest.mark.django_db
class TestUserRetrieveAndUpdate:
    def test_if_user_is_anonymous_returns_401(
        self, api_client, authenticate, retrieve_and_update_user
    ):
        user = baker.make(User)
        payload = {
            "first_name": "John",
            "last_name": "Doe",
        }

        res = retrieve_and_update_user(payload, user.id)

        assert res.status_code == status.HTTP_401_UNAUTHORIZED

    def test_if_user_is_not_admin_returns_403(
        self, api_client, authenticate, retrieve_and_update_user
    ):
        authenticate(is_staff=True, role=ROLE_STAFF)
        user = baker.make(User)
        payload = {
            "first_name": "John",
            "last_name": "Doe",
        }

        res = retrieve_and_update_user(payload, user.id)

        assert res.status_code == status.HTTP_403_FORBIDDEN

    def test_if_user_is_admin__has_valid_data_returns_200(
        self, api_client, authenticate, retrieve_and_update_user
    ):
        authenticate(is_staff=True, role=ROLE_ADMIN)
        user = baker.make(User)
        payload = {
            "first_name": "John",
            "last_name": "Doe",
        }

        res = retrieve_and_update_user(payload, user.id)

        assert res.status_code == status.HTTP_200_OK
        assert res.data["first_name"] == payload["first_name"]
        assert res.data["last_name"] == payload["last_name"]

    def test_if_user_is_admin_upload_image_returns_200(
        self,
        api_client,
        authenticate,
        create_user_db,
        retrieve_and_update_user,
        remove_image,
    ):
        user_data = {"email": "test@example.com", "password": "1234"}
        user = create_user_db(user_data)
        authenticate(is_staff=True, role=ROLE_ADMIN)

        with tempfile.NamedTemporaryFile(suffix=".jpg", delete=False) as avatar:
            img = Image.new("RGB", (100, 100), "white")
            img.save(avatar, "JPEG")
            avatar.seek(0)

            payload = {
                "email": user_data["email"],
                "password": user_data["password"],
                "avatar": avatar,
            }
            res = retrieve_and_update_user(payload, user.id)
            assert res.status_code == status.HTTP_200_OK
            assert res.data["avatar"] is not None

            remove_image(res.data["avatar"])

    def test_if_user_is_admin_upload_image_returns_400(
        self,
        api_client,
        authenticate,
        create_user_db,
        retrieve_and_update_user,
    ):
        user_data = {"email": "test@example.com", "password": "1234"}
        user = create_user_db(user_data)
        authenticate(is_staff=True, role=ROLE_ADMIN)

        with tempfile.NamedTemporaryFile(suffix=".jpg") as avatar:
            avatar.write(b"invalid file content")
            avatar.seek(0)

            payload = {
                "email": user_data["email"],
                "password": user_data["password"],
                "avatar": avatar,
            }
            res = retrieve_and_update_user(payload, user.id)

            assert res.status_code == status.HTTP_400_BAD_REQUEST
            assert res.data.get("avatar") is None


@pytest.fixture
def delete_user(api_client):
    def receive_id(id=None):
        return api_client.delete(f"/api/accounts/details/{id}/")

    return receive_id


@pytest.mark.django_db
class TestUserDelete:
    def test_if_user_is_anonymous_returns_401(
        self, api_client, authenticate, delete_user
    ):
        user = baker.make(User)

        res = delete_user(user.id)

        assert res.status_code == status.HTTP_401_UNAUTHORIZED

    def test_if_user_is_not_admin_returns_403(
        self, api_client, authenticate, delete_user
    ):
        authenticate(is_staff=True, role=ROLE_STAFF)
        user = baker.make(User)

        res = delete_user(user.id)

        assert res.status_code == status.HTTP_403_FORBIDDEN

    def test_if_user_is_admin_returns_204(self, api_client, authenticate, delete_user):
        authenticate(is_staff=True, role=ROLE_ADMIN)
        user = baker.make(User)

        res = delete_user(user.id)

        user = User.objects.filter(id=user.id).first()

        assert res.status_code == status.HTTP_204_NO_CONTENT
        assert user is None
