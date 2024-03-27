import pytest
from rest_framework import status
from model_bakery import baker

from core.constants import ROLE_ADMIN, ROLE_STAFF
from ..models import Teacher


@pytest.fixture
def update_teacher(api_client):
    def receive_instance(
        instance,
        id=None,
    ):
        return api_client.patch(f"/api/teachers/{id}/", instance)

    return receive_instance


@pytest.mark.django_db
class TestUpdateTeacher:
    def test_if_user_is_anonymous_returns_401(self, authenticate, update_teacher):
        item = baker.make(Teacher)

        payload = {
            "occupation": "marine",
        }

        res = update_teacher(payload, item.id)

        assert res.status_code == status.HTTP_401_UNAUTHORIZED

    def test_if_user_is_staff_returns_403(self, authenticate, update_teacher):
        item = baker.make(Teacher)
        authenticate(is_staff=True, role=ROLE_STAFF)

        payload = {
            "occupation": "marine",
        }

        res = update_teacher(payload, item.id)

        assert res.status_code == status.HTTP_403_FORBIDDEN

    def test_if_user_is_authenticated_returns_403(self, authenticate, update_teacher):
        item = baker.make(Teacher)
        authenticate()

        payload = {
            "occupation": "marine",
        }

        res = update_teacher(payload, item.id)

        assert res.status_code == status.HTTP_403_FORBIDDEN

    def test_if_user_is_admin_item_not_exists_returns_404(
        self, authenticate, update_teacher
    ):
        item = baker.make(Teacher)
        authenticate(is_staff=True, role=ROLE_ADMIN)

        payload = {
            "occupation": "marine",
        }

        res = update_teacher(payload, item.id + 5)

        assert res.status_code == status.HTTP_404_NOT_FOUND

    def test_if_user_is_admin_returns_200(self, authenticate, update_teacher):
        item = baker.make(Teacher)
        authenticate(is_staff=True, role=ROLE_ADMIN)

        payload = {
            "occupation": "marine",
        }

        res = update_teacher(payload, item.id)

        assert res.status_code == status.HTTP_200_OK


@pytest.fixture
def delete_teacher(api_client):
    def receive_id(id=None):
        return api_client.delete(f"/api/teachers/{id}/")

    return receive_id


@pytest.mark.django_db
class TestDeleteTeacher:
    def test_if_user_is_anonymous_returns_401(self, authenticate, delete_teacher):
        item = baker.make(Teacher)

        res = delete_teacher(item.id)

        assert res.status_code == status.HTTP_401_UNAUTHORIZED

    def test_if_user_is_authenticated_returns_403(self, authenticate, delete_teacher):
        item = baker.make(Teacher)
        authenticate()

        res = delete_teacher(item.id)

        assert res.status_code == status.HTTP_403_FORBIDDEN

    def test_if_user_is_staff_returns_403(self, authenticate, delete_teacher):
        item = baker.make(Teacher)
        authenticate(is_staff=True, role=ROLE_STAFF)

        res = delete_teacher(item.id)

        assert res.status_code == status.HTTP_403_FORBIDDEN

    def test_if_user_is_admin_item_not_exists_returns_404(
        self, authenticate, delete_teacher
    ):
        item = baker.make(Teacher)
        authenticate(is_staff=True, role=ROLE_ADMIN)

        res = delete_teacher(item.id + 5)

        assert res.status_code == status.HTTP_404_NOT_FOUND

    def test_if_user_is_admin_returns_200(self, authenticate, delete_teacher):
        item = baker.make(Teacher)
        authenticate(is_staff=True, role=ROLE_ADMIN)

        res = delete_teacher(item.id)

        assert res.status_code == status.HTTP_204_NO_CONTENT
