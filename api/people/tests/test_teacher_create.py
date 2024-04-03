import pytest
from rest_framework import status

from institute.models import Department, Faculty
from people.models import Parent
from core.constants import (
    DEPT_FISH,
    DESIGNATION_ASSOCIATE_PROFESSOR,
    ROLE_ADMIN,
    ROLE_STAFF,
    ROLE_USER,
)
from account.models import User
from address.models import Address


@pytest.fixture
def create_teacher(api_client):
    def receive_teacher_instance(instance):
        return api_client.post("/api/teachers/", instance)

    return receive_teacher_instance


@pytest.mark.django_db
class TestCreateTeacher:
    def setUp(self):
        user = User.objects.create_user(email="test@example", password="1234")
        address = Address.objects.create(
            building_and_street="Test Address 1",
            postal_code="1234",
            district="dhaka",
        )
        faculty = Faculty.objects.create(name="Test Faculty")
        department = Department.objects.create(name="Test Department", faculty=faculty)
        self.teacher = {
            "user": user.id,
            "address": address.id,
            "department": department.id,
        }

    def test_if_user_is_anonymous_returns_401(self, authenticate, create_teacher):
        self.setUp()
        res = create_teacher(self.teacher)

        assert res.status_code == status.HTTP_401_UNAUTHORIZED

    def test_if_user_is_authenticated_returns_403(self, authenticate, create_teacher):
        self.setUp()
        authenticate()
        res = create_teacher(self.teacher)
        # cannot create teacher twice with same user
        assert res.status_code == status.HTTP_403_FORBIDDEN

    def test_if_user_is_user_returns_403(self, authenticate, create_teacher):
        self.setUp()
        authenticate(is_staff=True, role=ROLE_USER)
        res = create_teacher(self.teacher)

        assert res.status_code == status.HTTP_403_FORBIDDEN

    def test_if_user_is_staff_returns_403(self, authenticate, create_teacher):
        self.setUp()
        authenticate(is_staff=True, role=ROLE_STAFF)
        res = create_teacher(self.teacher)

        assert res.status_code == status.HTTP_403_FORBIDDEN

    def test_if_user_is_admin_has_invalid_user_returns_400(
        self, authenticate, create_teacher
    ):
        self.setUp()
        authenticate(is_staff=True, role=ROLE_ADMIN)
        self.teacher["user"] = self.teacher["user"] + 5
        print(self.teacher)
        res = create_teacher(self.teacher)

        assert res.status_code == status.HTTP_400_BAD_REQUEST

    def test_if_user_is_admin_has_valid_data_returns_201(
        self, authenticate, create_teacher
    ):
        self.setUp()
        authenticate(is_staff=True, role=ROLE_ADMIN)
        res = create_teacher(self.teacher)

        assert res.status_code == status.HTTP_201_CREATED
