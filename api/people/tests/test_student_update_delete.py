import pytest
from rest_framework import status
from model_bakery import baker

from core.constants import ROLE_ADMIN, ROLE_STAFF
from ..models import Student


@pytest.fixture
def update_student(api_client):
    def receive_instance(
        instance,
        id=None,
    ):
        return api_client.patch(f"/api/students/{id}/", instance)

    return receive_instance


@pytest.mark.django_db
class TestUpdateStudent:
    def test_if_user_is_anonymous_returns_401(self, authenticate, update_student):
        item = baker.make(Student)

        payload = {
            "occupation": "marine",
        }

        res = update_student(payload, item.id)

        assert res.status_code == status.HTTP_401_UNAUTHORIZED

    def test_if_user_is_authenticated_returns_403(self, authenticate, update_student):
        item = baker.make(Student)
        authenticate()

        payload = {
            "occupation": "marine",
        }

        res = update_student(payload, item.id)

        assert res.status_code == status.HTTP_403_FORBIDDEN

    def test_if_user_is_admin_item_not_exists_returns_404(
        self, authenticate, update_student
    ):
        item = baker.make(Student)
        authenticate(is_staff=True, role=ROLE_ADMIN)

        payload = {
            "occupation": "marine",
        }

        res = update_student(payload, item.id + 5)

        assert res.status_code == status.HTTP_404_NOT_FOUND

    def test_if_user_is_staff_returns_200(self, authenticate, update_student):
        item = baker.make(Student)
        authenticate(is_staff=True, role=ROLE_STAFF)

        payload = {
            "occupation": "marine",
        }

        res = update_student(payload, item.id)

        assert res.status_code == status.HTTP_200_OK

    def test_if_user_is_admin_returns_200(self, authenticate, update_student):
        item = baker.make(Student)
        authenticate(is_staff=True, role=ROLE_ADMIN)

        payload = {
            "occupation": "marine",
        }

        res = update_student(payload, item.id)

        assert res.status_code == status.HTTP_200_OK


@pytest.fixture
def delete_student(api_client):
    def receive_id(id=None):
        return api_client.delete(f"/api/students/{id}/")

    return receive_id


@pytest.mark.django_db
class TestDeleteStudent:
    def test_if_user_is_anonymous_returns_401(self, authenticate, delete_student):
        item = baker.make(Student)

        res = delete_student(item.id)

        assert res.status_code == status.HTTP_401_UNAUTHORIZED

    def test_if_user_is_authenticated_returns_403(self, authenticate, delete_student):
        item = baker.make(Student)
        authenticate()

        res = delete_student(item.id)

        assert res.status_code == status.HTTP_403_FORBIDDEN

    def test_if_user_is_admin_item_not_exists_returns_404(
        self, authenticate, delete_student
    ):
        item = baker.make(Student)
        authenticate(is_staff=True, role=ROLE_ADMIN)

        res = delete_student(item.id + 5)

        assert res.status_code == status.HTTP_404_NOT_FOUND

    def test_if_user_is_staff_returns_204(self, authenticate, delete_student):
        item = baker.make(Student)
        authenticate(is_staff=True, role=ROLE_STAFF)

        res = delete_student(item.id)

        assert res.status_code == status.HTTP_204_NO_CONTENT

    def test_if_user_is_admin_returns_200(self, authenticate, delete_student):
        item = baker.make(Student)
        authenticate(is_staff=True, role=ROLE_ADMIN)

        res = delete_student(item.id)

        assert res.status_code == status.HTTP_204_NO_CONTENT
