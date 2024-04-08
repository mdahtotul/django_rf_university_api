import pytest
from rest_framework import status
from model_bakery import baker

from core.constants import ROLE_ADMIN, ROLE_STAFF, SEM_1, YEAR_1ST
from account.models import User
from institute.models import Department
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

    def test_if_user_is_admin_has_both_year_semester_returns_400(
        self, authenticate, update_student
    ):
        item = baker.make(Student)
        authenticate(is_staff=True, role=ROLE_ADMIN)

        payload = {"year": YEAR_1ST, "semester": SEM_1}

        res = update_student(payload, item.id)

        assert res.status_code == status.HTTP_400_BAD_REQUEST

    def test_if_user_is_admin_has_semester_returns_200_with_year_null(
        self, authenticate, update_student
    ):
        item = baker.make(Student, year=YEAR_1ST)
        authenticate(is_staff=True, role=ROLE_ADMIN)

        payload = {"semester": SEM_1}

        res = update_student(payload, item.id)

        assert res.status_code == status.HTTP_200_OK
        assert res.data["semester"] is not None
        assert res.data["year"] is None

    def test_if_user_is_admin_has_year_returns_200_with_semester_null(
        self, authenticate, update_student
    ):
        item = baker.make(Student, semester=SEM_1)
        authenticate(is_staff=True, role=ROLE_ADMIN)

        payload = {"year": YEAR_1ST}

        res = update_student(payload, item.id)

        assert res.status_code == status.HTTP_200_OK
        assert res.data["semester"] is None
        assert res.data["year"] is not None

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

    def test_if_user_is_admin_can_change_department_returns_200(
        self, authenticate, update_student
    ):
        item = baker.make(Student)
        department = baker.make(Department)
        authenticate(is_staff=True, role=ROLE_ADMIN)

        payload = {"department": department.id}

        res = update_student(payload, item.id)

        assert res.status_code == status.HTTP_200_OK
        assert res.data["department"] == department.id

    def test_if_user_is_admin_can_change_user_returns_200(
        self, authenticate, update_student
    ):
        item = baker.make(Student)
        user = baker.make(User)
        authenticate(is_staff=True, role=ROLE_ADMIN)

        payload = {"user": user.id}

        res = update_student(payload, item.id)

        assert res.status_code == status.HTTP_200_OK
        assert res.data["user"] == user.id


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
