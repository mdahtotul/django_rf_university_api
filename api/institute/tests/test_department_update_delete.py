import tempfile
import pytest
from PIL import Image
from rest_framework import status
from model_bakery import baker

from core.constants import ROLE_ADMIN, ROLE_STAFF
from institute.models import Department, Faculty


@pytest.fixture
def update_department(api_client):
    def receive_instance(
        instance,
        id=None,
    ):
        return api_client.patch(f"/api/departments/{id}/", instance)

    return receive_instance


@pytest.mark.django_db
class TestUpdateDepartment:
    def test_if_user_is_anonymous_returns_401(self, authenticate, update_department):
        item = baker.make(Department)

        payload = {"name": "test department"}

        res = update_department(payload, item.id)

        assert res.status_code == status.HTTP_401_UNAUTHORIZED

    def test_if_user_is_authenticated_returns_403(
        self, authenticate, update_department
    ):
        item = baker.make(Department)
        authenticate()

        payload = {"name": "test department"}

        res = update_department(payload, item.id)

        assert res.status_code == status.HTTP_403_FORBIDDEN

    def test_if_user_is_staff_returns_403(self, authenticate, update_department):
        item = baker.make(Department)
        authenticate(is_staff=True, role=ROLE_STAFF)

        payload = {"name": "test department"}

        res = update_department(payload, item.id)

        assert res.status_code == status.HTTP_403_FORBIDDEN

    def test_if_user_is_admin_item_not_exists_returns_404(
        self, authenticate, update_department
    ):
        item = baker.make(Department)
        authenticate(is_staff=True, role=ROLE_ADMIN)

        payload = {"name": "test department"}

        res = update_department(payload, item.id + 5)

        assert res.status_code == status.HTTP_404_NOT_FOUND

    def test_if_user_is_admin_returns_200(self, authenticate, update_department):
        item = baker.make(Department)
        authenticate(is_staff=True, role=ROLE_ADMIN)

        payload = {"name": "test department"}

        res = update_department(payload, item.id)

        assert res.status_code == status.HTTP_200_OK

    def test_if_user_is_admin_faculty_updated_returns_200(
        self, authenticate, update_department
    ):
        faculty = baker.make(Faculty)
        item = baker.make(Department)
        authenticate(is_staff=True, role=ROLE_ADMIN)

        payload = {"faculty": faculty.id}

        res = update_department(payload, item.id)

        assert res.status_code == status.HTTP_200_OK
        assert res.data["faculty"] == faculty.id

    def test_if_user_is_admin_has_valid_image_returns_200(
        self, authenticate, update_department, remove_image
    ):
        item = baker.make(Department)
        authenticate(is_staff=True, role=ROLE_ADMIN)

        with tempfile.NamedTemporaryFile(suffix=".jpg") as image:
            img = Image.new("RGB", (100, 100), "white")
            img.save(image, "JPEG")
            image.seek(0)

            payload = {
                "name": "test department",
                "description": "test department description",
                "image": image,
            }
            res = update_department(payload, item.id)

            assert res.status_code == status.HTTP_200_OK
            image_path = res.data["image"]
            assert image_path is not None
            stored_path = image_path.replace("http://testserver", "")

            remove_image(stored_path)

    def test_if_user_is_admin_has_invalid_image_returns_400(
        self, authenticate, update_department
    ):
        item = baker.make(Department)
        authenticate(is_staff=True, role=ROLE_ADMIN)

        with tempfile.NamedTemporaryFile(suffix=".jpg") as image:
            image.write(b"invalid file content")
            image.seek(0)

            payload = {
                "name": "test department",
                "description": "test department description",
                "image": image,
            }
            res = update_department(payload, item.id)

            assert res.status_code == status.HTTP_400_BAD_REQUEST


@pytest.fixture
def delete_department(api_client):
    def receive_id(id=None):
        return api_client.delete(f"/api/departments/{id}/")

    return receive_id


@pytest.mark.django_db
class TestDeleteDepartment:
    def test_if_user_is_anonymous_returns_401(self, authenticate, delete_department):
        item = baker.make(Department)

        res = delete_department(item.id)

        assert res.status_code == status.HTTP_401_UNAUTHORIZED

    def test_if_user_is_authenticated_returns_403(
        self, authenticate, delete_department
    ):
        item = baker.make(Department)
        authenticate()

        res = delete_department(item.id)

        assert res.status_code == status.HTTP_403_FORBIDDEN

    def test_if_user_is_staff_returns_403(self, authenticate, delete_department):
        item = baker.make(Department)
        authenticate(is_staff=True, role=ROLE_STAFF)

        res = delete_department(item.id)

        assert res.status_code == status.HTTP_403_FORBIDDEN

    def test_if_user_is_admin_item_not_exists_returns_404(
        self, authenticate, delete_department
    ):
        item = baker.make(Department)
        authenticate(is_staff=True, role=ROLE_ADMIN)

        res = delete_department(item.id + 5)

        assert res.status_code == status.HTTP_404_NOT_FOUND

    def test_if_user_is_admin_returns_200(self, authenticate, delete_department):
        item = baker.make(Department)
        authenticate(is_staff=True, role=ROLE_ADMIN)

        res = delete_department(item.id)

        assert res.status_code == status.HTTP_204_NO_CONTENT
