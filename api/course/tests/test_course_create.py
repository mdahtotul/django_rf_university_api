import tempfile
import pytest
from PIL import Image
from rest_framework import status
from model_bakery import baker

from core.constants import ROLE_ADMIN, ROLE_STAFF, ROLE_USER, SEM_1, YEAR_1ST
from institute.models import Department


@pytest.fixture
def create_course(api_client):
    def receive_course_instance(instance):
        return api_client.post("/api/courses/", instance)

    return receive_course_instance


@pytest.mark.django_db
class TestCreateCourse:
    def setUp(self):
        department = baker.make(Department)
        self.course = {
            "name": "test course",
            "code": "TEST-101",
            "description": "test course description",
            "year": YEAR_1ST,
            "department": department.id,
        }

    def test_if_user_is_anonymous_returns_401(self, authenticate, create_course):
        self.setUp()
        res = create_course(self.course)

        assert res.status_code == status.HTTP_401_UNAUTHORIZED

    def test_if_user_is_authenticated_returns_403(self, authenticate, create_course):
        self.setUp()
        authenticate()
        res = create_course(self.course)

        assert res.status_code == status.HTTP_403_FORBIDDEN

    def test_if_user_is_user_returns_403(self, authenticate, create_course):
        self.setUp()
        authenticate(is_staff=True, role=ROLE_USER)
        res = create_course(self.course)

        assert res.status_code == status.HTTP_403_FORBIDDEN

    def test_if_user_is_staff_returns_403(self, authenticate, create_course):
        self.setUp()
        authenticate(is_staff=True, role=ROLE_STAFF)
        res = create_course(self.course)

        assert res.status_code == status.HTTP_403_FORBIDDEN

    def test_if_user_is_admin_with_no_name_returns_400(
        self, authenticate, create_course
    ):
        self.setUp()
        authenticate(is_staff=True, role=ROLE_ADMIN)
        del self.course["name"]
        res = create_course(self.course)

        assert res.status_code == status.HTTP_400_BAD_REQUEST

    def test_if_user_is_admin_with_no_code_returns_400(
        self, authenticate, create_course
    ):
        self.setUp()
        authenticate(is_staff=True, role=ROLE_ADMIN)
        del self.course["code"]
        res = create_course(self.course)

        assert res.status_code == status.HTTP_400_BAD_REQUEST

    def test_if_user_is_admin_with_no_department_returns_400(
        self, authenticate, create_course
    ):
        self.setUp()
        authenticate(is_staff=True, role=ROLE_ADMIN)
        del self.course["department"]
        res = create_course(self.course)

        assert res.status_code == status.HTTP_400_BAD_REQUEST

    def test_if_user_is_admin_has_invalid_image_returns_400(
        self, authenticate, create_course
    ):
        self.setUp()
        authenticate(is_staff=True, role=ROLE_ADMIN)

        with tempfile.NamedTemporaryFile(suffix=".jpg") as image:
            image.write(b"invalid file content")
            image.seek(0)

            payload = {
                "name": self.course["name"],
                "code": self.course["code"],
                "description": self.course["description"],
                "year": self.course["year"],
                "department": self.course["department"],
                "thumbnail": image,
            }
            res = create_course(payload)

            assert res.status_code == status.HTTP_400_BAD_REQUEST

    def test_if_user_is_admin_has_valid_image_returns_201(
        self, authenticate, create_course, remove_image
    ):
        self.setUp()
        authenticate(is_staff=True, role=ROLE_ADMIN)

        with tempfile.NamedTemporaryFile(suffix=".jpg") as image:
            img = Image.new("RGB", (100, 100), "white")
            img.save(image, "JPEG")
            image.seek(0)

            payload = {
                "name": self.course["name"],
                "code": self.course["code"],
                "description": self.course["description"],
                "year": self.course["year"],
                "department": self.course["department"],
                "thumbnail": image,
            }
            res = create_course(payload)

            assert res.status_code == status.HTTP_201_CREATED
            image_path = res.data["thumbnail"]
            assert image_path is not None
            stored_path = image_path.replace("http://testserver", "")

            remove_image(stored_path)

    def test_if_user_is_admin_returns_201(self, authenticate, create_course):
        self.setUp()
        authenticate(is_staff=True, role=ROLE_ADMIN)
        res = create_course(self.course)

        assert res.status_code == status.HTTP_201_CREATED
