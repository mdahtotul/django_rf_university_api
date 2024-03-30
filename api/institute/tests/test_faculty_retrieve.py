import pytest

from rest_framework import status
from model_bakery import baker

from account.models import User
from institute.models import Faculty


@pytest.fixture
def retrieve_faculty(api_client):
    def receive_id_params(id=None, name=None, last_name=None, email=None, phone=None):
        url = "/api/faculties/"

        if id is not None:
            url += f"{id}/"
        elif name is not None:
            url += "?"
            params = []

            if name is not None:
                params.append(f"name={name}")

            url += "&".join(params)

        return api_client.get(url)

    return receive_id_params


@pytest.mark.django_db
class TestRetrieveFacultyList:
    def test_if_user_is_anonymous_or_authenticated_and_has_no_data_returns_200(
        self, authenticate, retrieve_faculty
    ):
        res = retrieve_faculty()

        assert res.status_code == status.HTTP_200_OK
        assert res.data["count"] == 0

    def test_if_user_is_anonymous_or_authenticated_returns_200(
        self, authenticate, retrieve_faculty
    ):
        baker.make(Faculty)
        baker.make(Faculty)
        baker.make(Faculty)

        res = retrieve_faculty()

        assert res.status_code == status.HTTP_200_OK
        assert res.data["count"] == 3

    def test_if_faculty_name_filter_working_returns_200(
        self, authenticate, retrieve_faculty
    ):
        baker.make(Faculty, name="John")
        baker.make(Faculty, name="Alice")
        baker.make(Faculty, name="Bob")

        res = retrieve_faculty(name="Bob")

        assert res.status_code == status.HTTP_200_OK
        assert res.data["count"] == 1
        result = res.data["results"][0]
        assert result["name"] == "Bob"


@pytest.mark.django_db
class TestRetrieveSingleFaculty:
    def test_if_user_is_anonymous_or_authenticated_and_has_no_data_returns_404(
        self, authenticate, retrieve_faculty
    ):
        res = retrieve_faculty(2)

        assert res.status_code == status.HTTP_404_NOT_FOUND

    def test_if_user_is_anonymous_or_authenticated_and_has_data_returns_200(
        self, authenticate, retrieve_faculty
    ):
        item1 = baker.make(Faculty)
        item2 = baker.make(Faculty)
        item3 = baker.make(Faculty)

        res = retrieve_faculty(item2.id)

        assert res.status_code == status.HTTP_200_OK
        assert res.data["id"] == item2.id
