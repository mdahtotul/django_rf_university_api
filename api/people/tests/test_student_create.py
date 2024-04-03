import pytest
from rest_framework import status

from institute.models import Department, Faculty
from people.models import Parent
from core.constants import ROLE_ADMIN, ROLE_STAFF, ROLE_USER
from account.models import User
from address.models import Address


@pytest.fixture
def create_student(api_client):
    def receive_student_instance(instance):
        return api_client.post("/api/students/", instance)

    return receive_student_instance


@pytest.mark.django_db
class TestCreateStudent:
    def setUp(self):
        user = User.objects.create_user(email="test@example", password="1234")
        user2 = User.objects.create_user(email="test1234@example", password="1234")
        address = Address.objects.create(
            building_and_street="Test Address 1",
            postal_code="1234",
            district="dhaka",
        )
        parent = Parent.objects.create(user=user2, address=address, occupation="test")
        faculty = Faculty.objects.create(name="Test Faculty")
        department = Department.objects.create(name="Test Department", faculty=faculty)
        self.student = {
            "student_id": "18207003",
            "user": user.id,
            "parent": parent.id,
            "address": address.id,
            "cgpa": "3.62",
            "credits": 28,
            "session": "2017-2018",
            "semester": "1st semester",
            "year": "1st year",
            "department": department.id,
            "relationship_to_parent": "Sister",
        }

    def test_if_user_is_anonymous_returns_401(self, authenticate, create_student):
        self.setUp()
        res = create_student(self.student)

        assert res.status_code == status.HTTP_401_UNAUTHORIZED

    def test_if_user_is_authenticated_returns_403(self, authenticate, create_student):
        self.setUp()
        authenticate()
        res = create_student(self.student)
        # cannot create student twice with same user
        assert res.status_code == status.HTTP_403_FORBIDDEN

    def test_if_user_is_user_returns_403(self, authenticate, create_student):
        self.setUp()
        authenticate(is_staff=True, role=ROLE_USER)
        res = create_student(self.student)

        assert res.status_code == status.HTTP_403_FORBIDDEN

    def test_if_user_is_staff_has_invalid_student_id_returns_400(
        self, authenticate, create_student
    ):
        self.setUp()
        authenticate(is_staff=True, role=ROLE_STAFF)
        self.student["student_id"] = "test"
        res = create_student(self.student)

        assert res.status_code == status.HTTP_400_BAD_REQUEST

    def test_if_user_is_staff_has_invalid_user_returns_400(
        self, authenticate, create_student
    ):
        self.setUp()
        authenticate(is_staff=True, role=ROLE_STAFF)
        self.student["user"] = "test"
        res = create_student(self.student)

        assert res.status_code == status.HTTP_400_BAD_REQUEST

    def test_if_user_is_staff_has_invalid_parent_returns_400(
        self, authenticate, create_student
    ):
        self.setUp()
        authenticate(is_staff=True, role=ROLE_STAFF)
        self.student["parent"] = "test"
        res = create_student(self.student)

        assert res.status_code == status.HTTP_400_BAD_REQUEST

    def test_if_user_is_staff_has_invalid_address_returns_400(
        self, authenticate, create_student
    ):
        self.setUp()
        authenticate(is_staff=True, role=ROLE_STAFF)
        self.student["address"] = "test"
        res = create_student(self.student)

        assert res.status_code == status.HTTP_400_BAD_REQUEST

    def test_if_user_is_staff_has_invalid_cgpa_returns_400(
        self, authenticate, create_student
    ):
        self.setUp()
        authenticate(is_staff=True, role=ROLE_STAFF)
        self.student["cgpa"] = "test"
        res = create_student(self.student)

        assert res.status_code == status.HTTP_400_BAD_REQUEST

    def test_if_user_is_staff_has_invalid_degree_returns_400(
        self, authenticate, create_student
    ):
        self.setUp()
        authenticate(is_staff=True, role=ROLE_STAFF)
        self.student["degree"] = "test"
        res = create_student(self.student)

        assert res.status_code == status.HTTP_400_BAD_REQUEST

    def test_if_user_is_staff_has_invalid_department_returns_400(
        self, authenticate, create_student
    ):
        self.setUp()
        authenticate(is_staff=True, role=ROLE_STAFF)
        self.student["department"] = "test"
        res = create_student(self.student)

        assert res.status_code == status.HTTP_400_BAD_REQUEST

    def test_if_user_is_staff_has_valid_data_returns_201(
        self, authenticate, create_student
    ):
        self.setUp()
        authenticate(is_staff=True, role=ROLE_STAFF)
        res = create_student(self.student)

        assert res.status_code == status.HTTP_201_CREATED

    def test_if_user_is_admin_has_valid_data_returns_201(
        self, authenticate, create_student
    ):
        self.setUp()
        authenticate(is_staff=True, role=ROLE_ADMIN)
        res = create_student(self.student)

        assert res.status_code == status.HTTP_201_CREATED
