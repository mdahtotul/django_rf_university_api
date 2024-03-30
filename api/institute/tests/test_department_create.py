import tempfile
import pytest
from PIL import Image
from rest_framework import status

from core.constants import ROLE_ADMIN, ROLE_STAFF, ROLE_USER
from institute.models import Faculty


@pytest.fixture
def create_department(api_client):
    def receive_department_instance(instance):
        return api_client.post("/api/departments/", instance)

    return receive_department_instance


@pytest.mark.django_db
class TestCreateStudent:
    def setUp(self):
        self.faculty = Faculty.objects.create(name="test faculty")
        self.department = {
            "name": "test department",
            "description": "test department description",
            "faculty": self.faculty.id,
        }

    def test_if_user_is_anonymous_returns_401(self, authenticate, create_department):
        self.setUp()
        res = create_department(self.department)

        assert res.status_code == status.HTTP_401_UNAUTHORIZED

    def test_if_user_is_authenticated_returns_403(
        self, authenticate, create_department
    ):
        self.setUp()
        authenticate()
        res = create_department(self.department)
        # cannot create department twice with same user
        assert res.status_code == status.HTTP_403_FORBIDDEN

    def test_if_user_is_user_returns_403(self, authenticate, create_department):
        self.setUp()
        authenticate(is_staff=True, role=ROLE_USER)
        res = create_department(self.department)

        assert res.status_code == status.HTTP_403_FORBIDDEN

    def test_if_user_is_staff_has_valid_data_returns_403(
        self, authenticate, create_department
    ):
        self.setUp()
        authenticate(is_staff=True, role=ROLE_STAFF)
        res = create_department(self.department)

        assert res.status_code == status.HTTP_403_FORBIDDEN

    def test_if_user_is_admin_has_valid_data_returns_201(
        self, authenticate, create_department
    ):
        self.setUp()
        authenticate(is_staff=True, role=ROLE_ADMIN)
        res = create_department(self.department)

        assert res.status_code == status.HTTP_201_CREATED

    def test_if_user_is_admin_has_valid_image_returns_201(
        self, authenticate, create_department, remove_image
    ):
        self.setUp()
        authenticate(is_staff=True, role=ROLE_ADMIN)

        with tempfile.NamedTemporaryFile(suffix=".jpg") as image:
            img = Image.new("RGB", (100, 100), "white")
            img.save(image, "JPEG")
            image.seek(0)

            payload = {
                "name": self.department["name"],
                "description": self.department["description"],
                "faculty": self.faculty.id,
                "image": image,
            }
            res = create_department(payload)

            assert res.status_code == status.HTTP_201_CREATED
            image_path = res.data["image"]
            assert image_path is not None
            stored_path = image_path.replace("http://testserver", "")

            remove_image(stored_path)

    def test_if_user_is_admin_has_invalid_image_returns_400(
        self, authenticate, create_department
    ):
        self.setUp()
        authenticate(is_staff=True, role=ROLE_ADMIN)

        with tempfile.NamedTemporaryFile(suffix=".jpg") as image:
            image.write(b"invalid file content")
            image.seek(0)

            payload = {
                "name": self.department["name"],
                "description": self.department["description"],
                "faculty": self.faculty.id,
                "image": image,
            }
            res = create_department(payload)

            assert res.status_code == status.HTTP_400_BAD_REQUEST

    def test_if_user_is_admin_has_invalid_data_returns_400(
        self, authenticate, create_department
    ):
        self.setUp()
        authenticate(is_staff=True, role=ROLE_ADMIN)

        payload = {
            "description": self.department["description"],
        }

        res = create_department(payload)

        assert res.status_code == status.HTTP_400_BAD_REQUEST

    def test_if_user_is_admin_has_invalid_faculty_returns_400(
        self, authenticate, create_department
    ):
        self.setUp()
        authenticate(is_staff=True, role=ROLE_ADMIN)

        payload = {
            "name": self.department["name"],
            "description": self.department["description"],
            "faculty": self.faculty.id + 5,
        }

        res = create_department(payload)

        assert res.status_code == status.HTTP_400_BAD_REQUEST
