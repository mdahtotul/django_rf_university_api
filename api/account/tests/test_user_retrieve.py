import pytest
from rest_framework import status
from model_bakery import baker

from account.models import User
from core.constants import ROLE_ADMIN, ROLE_STAFF


@pytest.fixture
def retrieve_user(api_client):
    def receive_instance(id=None):
        if id is not None:
            return api_client.get(f"/api/accounts/details/{id}/")
        else:
            return api_client.get(f"/api/accounts/all/")

    return receive_instance


@pytest.mark.django_db
class TestRetrieveListUsers:

    def test_if_user_is_anonymous_returns_401(
        self, api_client, authenticate, retrieve_user
    ):
        baker.make(User)
        baker.make(User)

        res = retrieve_user()

        assert res.status_code == status.HTTP_401_UNAUTHORIZED

    def test_if_user_is_not_admin_returns_403(
        self, api_client, authenticate, retrieve_user
    ):
        authenticate(is_staff=True, role=ROLE_STAFF)

        baker.make(User)
        baker.make(User)

        res = retrieve_user()

        assert res.status_code == status.HTTP_403_FORBIDDEN

    def test_if_user_is_admin_returns_200(
        self, api_client, authenticate, retrieve_user
    ):
        authenticate(is_staff=True, role=ROLE_ADMIN)

        user1 = baker.make(User)
        user2 = baker.make(User)

        res = retrieve_user()

        assert res.status_code == status.HTTP_200_OK
        assert res.data[0]["email"] == user2.email
        assert res.data[1]["email"] == user1.email
        assert len(res.data) == 2


@pytest.mark.django_db
class TestRetrieveSingleUser:

    def test_if_user_is_anonymous_returns_401(
        self, api_client, authenticate, retrieve_user
    ):
        user1 = baker.make(User)
        baker.make(User)

        res = retrieve_user(user1.id)

        assert res.status_code == status.HTTP_401_UNAUTHORIZED

    def test_if_user_is_not_admin_returns_403(
        self, api_client, authenticate, retrieve_user
    ):
        authenticate(is_staff=True, role=ROLE_STAFF)

        user1 = baker.make(User)
        baker.make(User)

        res = retrieve_user(user1.id)

        assert res.status_code == status.HTTP_403_FORBIDDEN

    def test_if_user_is_admin_item_not_exist_returns_404(
        self, api_client, authenticate, retrieve_user
    ):
        authenticate(is_staff=True, role=ROLE_ADMIN)

        user1 = baker.make(User)
        dummy_id = user1.id + 10

        res = retrieve_user(dummy_id)
        assert res.status_code == status.HTTP_404_NOT_FOUND

    def test_if_user_is_admin_returns_200(
        self, api_client, authenticate, retrieve_user
    ):
        authenticate(is_staff=True, role=ROLE_ADMIN)

        user1 = baker.make(User)
        user2 = baker.make(User)

        res = retrieve_user(user1.id)
        assert res.status_code == status.HTTP_200_OK
        assert res.data["id"] == user1.id
        assert res.data["email"] == user1.email
