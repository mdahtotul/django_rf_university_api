import tempfile
import pytest
from PIL import Image
from rest_framework import status
from model_bakery import baker

from core.constants import ROLE_ADMIN, ROLE_STAFF, SEM_1, YEAR_1ST
from course.models import Course


@pytest.fixture
def update_course(api_client):
    def receive_instance(
        instance,
        id=None,
    ):
        return api_client.patch(f"/api/courses/{id}/", instance)

    return receive_instance


@pytest.mark.django_db
class TestUpdateCourse:
    def test_if_user_is_anonymous_returns_401(self, authenticate, update_course):
        item = baker.make(Course)

        payload = {"name": "test course"}

        res = update_course(payload, item.id)

        assert res.status_code == status.HTTP_401_UNAUTHORIZED

    def test_if_user_is_authenticated_returns_403(self, authenticate, update_course):
        item = baker.make(Course)
        authenticate()

        payload = {"name": "test course"}

        res = update_course(payload, item.id)

        assert res.status_code == status.HTTP_403_FORBIDDEN

    def test_if_user_is_staff_returns_403(self, authenticate, update_course):
        item = baker.make(Course)
        authenticate(is_staff=True, role=ROLE_STAFF)

        payload = {"name": "test course"}

        res = update_course(payload, item.id)

        assert res.status_code == status.HTTP_403_FORBIDDEN

    def test_if_user_is_admin_item_not_exists_returns_404(
        self, authenticate, update_course
    ):
        item = baker.make(Course)
        authenticate(is_staff=True, role=ROLE_ADMIN)

        payload = {"name": "test course"}

        res = update_course(payload, item.id + 5)

        assert res.status_code == status.HTTP_404_NOT_FOUND

    def test_if_user_is_admin_has_both_year_semester_returns_400(
        self, authenticate, update_course
    ):
        item = baker.make(Course)
        authenticate(is_staff=True, role=ROLE_ADMIN)

        payload = {
            "name": "test course",
            "year": YEAR_1ST,
            "semester": SEM_1,
        }

        res = update_course(payload, item.id)

        assert res.status_code == status.HTTP_400_BAD_REQUEST

    def test_if_user_is_admin_has_no_year_but_semester_returns_200_with_year_null(
        self, authenticate, update_course
    ):
        item = baker.make(Course, year=YEAR_1ST)
        authenticate(is_staff=True, role=ROLE_ADMIN)

        payload = {
            "name": "test course",
            "semester": SEM_1,
        }

        res = update_course(payload, item.id)

        assert res.status_code == status.HTTP_200_OK
        assert res.data["year"] is None
        assert res.data["semester"] is not None

    def test_if_user_is_admin_has_no_semester_but_year_returns_200_with_semester_null(
        self, authenticate, update_course
    ):
        item = baker.make(Course, semester=SEM_1)
        authenticate(is_staff=True, role=ROLE_ADMIN)

        payload = {
            "name": "test course",
            "year": YEAR_1ST,
        }

        res = update_course(payload, item.id)

        assert res.status_code == status.HTTP_200_OK
        assert res.data["year"] is not None
        assert res.data["semester"] is None

    def test_if_user_is_admin_returns_200(self, authenticate, update_course):
        item = baker.make(Course)
        authenticate(is_staff=True, role=ROLE_ADMIN)

        payload = {"name": "test course"}

        res = update_course(payload, item.id)

        assert res.status_code == status.HTTP_200_OK

    def test_if_user_is_admin_has_valid_image_returns_200(
        self, authenticate, update_course, remove_image
    ):
        item = baker.make(Course)
        authenticate(is_staff=True, role=ROLE_ADMIN)

        with tempfile.NamedTemporaryFile(suffix=".jpg") as image:
            img = Image.new("RGB", (100, 100), "white")
            img.save(image, "JPEG")
            image.seek(0)

            payload = {
                "name": "test course",
                "description": "test course description",
                "thumbnail": image,
            }
            res = update_course(payload, item.id)

            assert res.status_code == status.HTTP_200_OK
            image_path = res.data["thumbnail"]
            assert image_path is not None
            stored_path = image_path.replace("http://testserver", "")

            remove_image(stored_path)

    def test_if_user_is_admin_has_invalid_image_returns_400(
        self, authenticate, update_course
    ):
        item = baker.make(Course)
        authenticate(is_staff=True, role=ROLE_ADMIN)

        with tempfile.NamedTemporaryFile(suffix=".jpg") as image:
            image.write(b"invalid file content")
            image.seek(0)

            payload = {
                "name": "test course",
                "description": "test course description",
                "thumbnail": image,
            }
            res = update_course(payload, item.id)

            assert res.status_code == status.HTTP_400_BAD_REQUEST


@pytest.fixture
def delete_course(api_client):
    def receive_id(id=None):
        return api_client.delete(f"/api/courses/{id}/")

    return receive_id


@pytest.mark.django_db
class TestDeleteCourse:
    def test_if_user_is_anonymous_returns_401(self, authenticate, delete_course):
        item = baker.make(Course)

        res = delete_course(item.id)

        assert res.status_code == status.HTTP_401_UNAUTHORIZED

    def test_if_user_is_authenticated_returns_403(self, authenticate, delete_course):
        item = baker.make(Course)
        authenticate()

        res = delete_course(item.id)

        assert res.status_code == status.HTTP_403_FORBIDDEN

    def test_if_user_is_staff_returns_403(self, authenticate, delete_course):
        item = baker.make(Course)
        authenticate(is_staff=True, role=ROLE_STAFF)

        res = delete_course(item.id)

        assert res.status_code == status.HTTP_403_FORBIDDEN

    def test_if_user_is_admin_item_not_exists_returns_404(
        self, authenticate, delete_course
    ):
        item = baker.make(Course)
        authenticate(is_staff=True, role=ROLE_ADMIN)

        res = delete_course(item.id + 5)

        assert res.status_code == status.HTTP_404_NOT_FOUND

    def test_if_user_is_admin_returns_200(self, authenticate, delete_course):
        item = baker.make(Course)
        authenticate(is_staff=True, role=ROLE_ADMIN)

        res = delete_course(item.id)

        assert res.status_code == status.HTTP_204_NO_CONTENT
