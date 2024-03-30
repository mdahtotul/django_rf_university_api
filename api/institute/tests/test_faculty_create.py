import tempfile
import pytest
from PIL import Image
from rest_framework import status

from core.constants import ROLE_ADMIN, ROLE_STAFF, ROLE_USER


@pytest.fixture
def create_faculty(api_client):
    def receive_faculty_instance(instance):
        return api_client.post("/api/faculties/", instance)

    return receive_faculty_instance


@pytest.mark.django_db
class TestCreateStudent:
    def setUp(self):
        self.faculty = {
            "name": "test faculty",
            "description": "test faculty description",
        }

    def test_if_user_is_anonymous_returns_401(self, authenticate, create_faculty):
        self.setUp()
        res = create_faculty(self.faculty)

        assert res.status_code == status.HTTP_401_UNAUTHORIZED

    def test_if_user_is_authenticated_returns_403(self, authenticate, create_faculty):
        self.setUp()
        authenticate()
        res = create_faculty(self.faculty)
        # cannot create faculty twice with same user
        assert res.status_code == status.HTTP_403_FORBIDDEN

    def test_if_user_is_user_returns_403(self, authenticate, create_faculty):
        self.setUp()
        authenticate(is_staff=True, role=ROLE_USER)
        res = create_faculty(self.faculty)

        assert res.status_code == status.HTTP_403_FORBIDDEN

    def test_if_user_is_staff_has_valid_data_returns_403(
        self, authenticate, create_faculty
    ):
        self.setUp()
        authenticate(is_staff=True, role=ROLE_STAFF)
        res = create_faculty(self.faculty)

        assert res.status_code == status.HTTP_403_FORBIDDEN

    def test_if_user_is_admin_has_valid_data_returns_201(
        self, authenticate, create_faculty
    ):
        self.setUp()
        authenticate(is_staff=True, role=ROLE_ADMIN)
        res = create_faculty(self.faculty)

        assert res.status_code == status.HTTP_201_CREATED

    def test_if_user_is_admin_has_valid_image_returns_201(
        self, authenticate, create_faculty, remove_image
    ):
        self.setUp()
        authenticate(is_staff=True, role=ROLE_ADMIN)

        with tempfile.NamedTemporaryFile(suffix=".jpg") as image:
            img = Image.new("RGB", (100, 100), "white")
            img.save(image, "JPEG")
            image.seek(0)

            payload = {
                "name": "test faculty",
                "description": "test faculty description",
                "image": image,
            }
            res = create_faculty(payload)

            assert res.status_code == status.HTTP_201_CREATED
            image_path = res.data["image"]
            assert image_path is not None
            stored_path = image_path.replace("http://testserver", "")

            remove_image(stored_path)

    def test_if_user_is_admin_has_invalid_image_returns_400(
        self, authenticate, create_faculty
    ):
        self.setUp()
        authenticate(is_staff=True, role=ROLE_ADMIN)

        with tempfile.NamedTemporaryFile(suffix=".jpg") as image:
            image.write(b"invalid file content")
            image.seek(0)

            payload = {
                "name": "test faculty",
                "description": "test faculty description",
                "image": image,
            }
            res = create_faculty(payload)

            assert res.status_code == status.HTTP_400_BAD_REQUEST

    def test_if_user_is_admin_has_invalid_data_returns_400(
        self, authenticate, create_faculty
    ):
        self.setUp()
        authenticate(is_staff=True, role=ROLE_ADMIN)

        payload = {
            "description": "test faculty description",
        }

        res = create_faculty(payload)

        assert res.status_code == status.HTTP_400_BAD_REQUEST
