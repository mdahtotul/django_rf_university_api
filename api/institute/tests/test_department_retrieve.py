import pytest

from rest_framework import status
from model_bakery import baker

from institute.models import Faculty, Department


@pytest.fixture
def retrieve_department(api_client):
    def receive_id_params(id=None, name=None):
        url = "/api/departments/"

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
class TestRetrieveDepartmentList:
    def test_if_user_is_anonymous_or_authenticated_and_has_no_data_returns_200(
        self, authenticate, retrieve_department
    ):
        res = retrieve_department()

        assert res.status_code == status.HTTP_200_OK
        assert res.data["count"] == 0

    def test_if_user_is_anonymous_or_authenticated_returns_200(
        self, authenticate, retrieve_department
    ):

        faculty1 = baker.make(Faculty)
        faculty2 = baker.make(Faculty)
        faculty3 = baker.make(Faculty)

        baker.make(Department, faculty=faculty1)
        baker.make(Department, faculty=faculty2)
        baker.make(Department, faculty=faculty3)

        res = retrieve_department()

        assert res.status_code == status.HTTP_200_OK
        assert res.data["count"] == 3

    def test_if_department_name_filter_working_returns_200(
        self, authenticate, retrieve_department
    ):
        faculty1 = baker.make(Faculty)
        faculty2 = baker.make(Faculty)
        faculty3 = baker.make(Faculty)

        baker.make(Department, faculty=faculty1, name="John")
        baker.make(Department, faculty=faculty2, name="Alice")
        baker.make(Department, faculty=faculty3, name="Bob")

        res = retrieve_department(name="Bob")

        assert res.status_code == status.HTTP_200_OK
        assert res.data["count"] == 1
        result = res.data["results"][0]
        assert result["name"] == "Bob"


@pytest.mark.django_db
class TestRetrieveSingleDepartment:
    def test_if_user_is_anonymous_or_authenticated_and_has_no_data_returns_404(
        self, authenticate, retrieve_department
    ):
        res = retrieve_department(2)

        assert res.status_code == status.HTTP_404_NOT_FOUND

    def test_if_user_is_anonymous_or_authenticated_and_has_data_returns_200(
        self, authenticate, retrieve_department
    ):
        item1 = baker.make(Department)
        item2 = baker.make(Department)
        item3 = baker.make(Department)

        res = retrieve_department(item2.id)

        assert res.status_code == status.HTTP_200_OK
        assert res.data["id"] == item2.id
