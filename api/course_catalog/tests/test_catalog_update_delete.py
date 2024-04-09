import pytest
from rest_framework import status
from model_bakery import baker

from core.constants import ROLE_ADMIN, ROLE_STAFF, ROLE_USER
from course_catalog.models import Subject, Chapter, Year


# testing of subject api
@pytest.fixture
def update_subject(api_client):
    def receive_id_params(id=None, instance=None):
        url = f"/api/course_catalogs/subjects/{id}/"

        return api_client.patch(url, instance)

    return receive_id_params


@pytest.mark.django_db
class TestUpdateSubject:
    def test_if_user_is_anonymous_returns_401(self, authenticate, update_subject):
        res = update_subject()

        assert res.status_code == status.HTTP_401_UNAUTHORIZED

    def test_if_user_is_user_returns_403(self, authenticate, update_subject):
        authenticate(is_staff=True, role=ROLE_USER)
        item1 = baker.make(Subject)
        item2 = baker.make(Subject)
        item3 = baker.make(Subject)

        payload = {
            "name": "Test",
        }

        res = update_subject(item3.id, payload)

        assert res.status_code == status.HTTP_403_FORBIDDEN

    def test_if_user_is_staff_returns_403(self, authenticate, update_subject):
        authenticate(is_staff=True, role=ROLE_STAFF)
        item1 = baker.make(Subject)
        item2 = baker.make(Subject)
        item3 = baker.make(Subject)

        payload = {
            "name": "Test",
        }

        res = update_subject(item3.id, payload)

        assert res.status_code == status.HTTP_403_FORBIDDEN

    def test_if_user_is_admin_returns_200(self, authenticate, update_subject):
        authenticate(is_staff=True, role=ROLE_ADMIN)
        item1 = baker.make(Subject)
        item2 = baker.make(Subject)
        item3 = baker.make(Subject)

        payload = {
            "name": "Test",
        }

        res = update_subject(item3.id, payload)

        assert res.status_code == status.HTTP_200_OK
        assert res.data["name"] == payload["name"]


@pytest.fixture
def delete_subject(api_client):
    def receive_id_params(id=None):
        url = f"/api/course_catalogs/subjects/{id}/"

        return api_client.delete(url)

    return receive_id_params


@pytest.mark.django_db
class TestDeleteSubject:
    def test_if_user_is_anonymous_returns_401(self, authenticate, delete_subject):
        res = delete_subject()

        assert res.status_code == status.HTTP_401_UNAUTHORIZED

    def test_if_user_is_user_returns_403(self, authenticate, delete_subject):
        authenticate(is_staff=True, role=ROLE_USER)
        item1 = baker.make(Subject)
        item2 = baker.make(Subject)
        item3 = baker.make(Subject)

        res = delete_subject(item3.id)

        assert res.status_code == status.HTTP_403_FORBIDDEN

    def test_if_user_is_staff_returns_403(self, authenticate, delete_subject):
        authenticate(is_staff=True, role=ROLE_STAFF)
        item1 = baker.make(Subject)
        item2 = baker.make(Subject)
        item3 = baker.make(Subject)

        res = delete_subject(item3.id)

        assert res.status_code == status.HTTP_403_FORBIDDEN

    def test_if_user_is_admin_returns_204(self, authenticate, delete_subject):
        authenticate(is_staff=True, role=ROLE_ADMIN)
        item1 = baker.make(Subject)
        item2 = baker.make(Subject)
        item3 = baker.make(Subject)

        res = delete_subject(item3.id)

        assert res.status_code == status.HTTP_204_NO_CONTENT


# testing of chapter api
@pytest.fixture
def update_chapter(api_client):
    def receive_id_params(id=None, instance=None):
        url = f"/api/course_catalogs/chapters/{id}/"

        return api_client.patch(url, instance)

    return receive_id_params


@pytest.mark.django_db
class TestUpdateChapter:
    def test_if_user_is_anonymous_returns_401(self, authenticate, update_chapter):
        res = update_chapter()

        assert res.status_code == status.HTTP_401_UNAUTHORIZED

    def test_if_user_is_user_returns_403(self, authenticate, update_chapter):
        authenticate(is_staff=True, role=ROLE_USER)
        item1 = baker.make(Chapter)
        item2 = baker.make(Chapter)
        item3 = baker.make(Chapter)

        payload = {
            "name": "Test",
        }

        res = update_chapter(item3.id, payload)

        assert res.status_code == status.HTTP_403_FORBIDDEN

    def test_if_user_is_staff_returns_403(self, authenticate, update_chapter):
        authenticate(is_staff=True, role=ROLE_STAFF)
        item1 = baker.make(Chapter)
        item2 = baker.make(Chapter)
        item3 = baker.make(Chapter)

        payload = {
            "name": "Test",
        }

        res = update_chapter(item3.id, payload)

        assert res.status_code == status.HTTP_403_FORBIDDEN

    def test_if_user_is_admin_returns_200(self, authenticate, update_chapter):
        authenticate(is_staff=True, role=ROLE_ADMIN)
        item1 = baker.make(Chapter)
        item2 = baker.make(Chapter)
        item3 = baker.make(Chapter)

        payload = {
            "name": "Test",
        }

        res = update_chapter(item3.id, payload)

        assert res.status_code == status.HTTP_200_OK
        assert res.data["name"] == payload["name"]


@pytest.fixture
def delete_chapter(api_client):
    def receive_id_params(id=None):
        url = f"/api/course_catalogs/chapters/{id}/"

        return api_client.delete(url)

    return receive_id_params


@pytest.mark.django_db
class TestDeleteChapter:
    def test_if_user_is_anonymous_returns_401(self, authenticate, delete_chapter):
        res = delete_chapter()

        assert res.status_code == status.HTTP_401_UNAUTHORIZED

    def test_if_user_is_user_returns_403(self, authenticate, delete_chapter):
        authenticate(is_staff=True, role=ROLE_USER)
        item1 = baker.make(Chapter)
        item2 = baker.make(Chapter)
        item3 = baker.make(Chapter)

        res = delete_chapter(item3.id)

        assert res.status_code == status.HTTP_403_FORBIDDEN

    def test_if_user_is_staff_returns_403(self, authenticate, delete_chapter):
        authenticate(is_staff=True, role=ROLE_STAFF)
        item1 = baker.make(Chapter)
        item2 = baker.make(Chapter)
        item3 = baker.make(Chapter)

        res = delete_chapter(item3.id)

        assert res.status_code == status.HTTP_403_FORBIDDEN

    def test_if_user_is_admin_returns_204(self, authenticate, delete_chapter):
        authenticate(is_staff=True, role=ROLE_ADMIN)
        item1 = baker.make(Chapter)
        item2 = baker.make(Chapter)
        item3 = baker.make(Chapter)

        res = delete_chapter(item3.id)

        assert res.status_code == status.HTTP_204_NO_CONTENT


# testing of year api
@pytest.fixture
def update_year(api_client):
    def receive_id_params(id=None, instance=None):
        url = f"/api/course_catalogs/years/{id}/"

        return api_client.patch(url, instance)

    return receive_id_params


@pytest.mark.django_db
class TestUpdateYear:
    def test_if_user_is_anonymous_returns_401(self, authenticate, update_year):
        res = update_year()

        assert res.status_code == status.HTTP_401_UNAUTHORIZED

    def test_if_user_is_user_returns_403(self, authenticate, update_year):
        authenticate(is_staff=True, role=ROLE_USER)
        item1 = baker.make(Year)
        item2 = baker.make(Year)
        item3 = baker.make(Year)

        payload = {"year": "2024"}

        res = update_year(item3.id, payload)

        assert res.status_code == status.HTTP_403_FORBIDDEN

    def test_if_user_is_staff_returns_403(self, authenticate, update_year):
        authenticate(is_staff=True, role=ROLE_STAFF)
        item1 = baker.make(Year)
        item2 = baker.make(Year)
        item3 = baker.make(Year)

        payload = {"year": "2024"}

        res = update_year(item3.id, payload)

        assert res.status_code == status.HTTP_403_FORBIDDEN

    def test_if_user_is_admin_returns_200(self, authenticate, update_year):
        authenticate(is_staff=True, role=ROLE_ADMIN)
        item1 = baker.make(Year)
        item2 = baker.make(Year)
        item3 = baker.make(Year)

        payload = {"year": "2024"}

        res = update_year(item3.id, payload)

        assert res.status_code == status.HTTP_200_OK
        assert res.data["year"] == payload["year"]


@pytest.fixture
def delete_year(api_client):
    def receive_id_params(id=None):
        url = f"/api/course_catalogs/years/{id}/"

        return api_client.delete(url)

    return receive_id_params


@pytest.mark.django_db
class TestDeleteYear:
    def test_if_user_is_anonymous_returns_401(self, authenticate, delete_year):
        res = delete_year()

        assert res.status_code == status.HTTP_401_UNAUTHORIZED

    def test_if_user_is_user_returns_403(self, authenticate, delete_year):
        authenticate(is_staff=True, role=ROLE_USER)
        item1 = baker.make(Year)
        item2 = baker.make(Year)
        item3 = baker.make(Year)

        res = delete_year(item3.id)

        assert res.status_code == status.HTTP_403_FORBIDDEN

    def test_if_user_is_staff_returns_403(self, authenticate, delete_year):
        authenticate(is_staff=True, role=ROLE_STAFF)
        item1 = baker.make(Year)
        item2 = baker.make(Year)
        item3 = baker.make(Year)

        res = delete_year(item3.id)

        assert res.status_code == status.HTTP_403_FORBIDDEN

    def test_if_user_is_admin_returns_204(self, authenticate, delete_year):
        authenticate(is_staff=True, role=ROLE_ADMIN)
        item1 = baker.make(Year)
        item2 = baker.make(Year)
        item3 = baker.make(Year)

        res = delete_year(item3.id)

        assert res.status_code == status.HTTP_204_NO_CONTENT
