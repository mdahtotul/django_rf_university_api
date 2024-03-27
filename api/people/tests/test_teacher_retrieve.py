import pytest

from rest_framework import status
from model_bakery import baker

from account.models import User
from people.models import Teacher


@pytest.fixture
def retrieve_teacher(api_client):
    def receive_id_params(
        id=None, first_name=None, last_name=None, email=None, phone=None
    ):
        url = "/api/teachers/"

        if id is not None:
            url += f"{id}/"
        elif (
            first_name is not None
            or last_name is not None
            or email is not None
            or phone is not None
        ):
            url += "?"
            params = []

            if first_name is not None:
                params.append(f"first_name={first_name}")
            if last_name is not None:
                params.append(f"last_name={last_name}")
            if email is not None:
                params.append(f"email={email}")
            if phone is not None:
                params.append(f"phone={phone}")

            url += "&".join(params)

        return api_client.get(url)

    return receive_id_params


@pytest.mark.django_db
class TestRetrieveTeacherList:
    def test_if_user_is_anonymous_or_authenticated_and_has_no_data_returns_200(
        self, authenticate, retrieve_teacher
    ):
        res = retrieve_teacher()

        assert res.status_code == status.HTTP_200_OK
        assert res.data["count"] == 0

    def test_if_user_is_anonymous_or_authenticated_returns_200(
        self, authenticate, retrieve_teacher
    ):
        baker.make(Teacher)
        baker.make(Teacher)
        baker.make(Teacher)

        res = retrieve_teacher()

        assert res.status_code == status.HTTP_200_OK
        assert res.data["count"] == 3

    def test_if_first_name_filter_working_returns_200(
        self, authenticate, retrieve_teacher
    ):
        user1 = baker.make(User, first_name="John")
        user2 = baker.make(User, first_name="Alice")
        user3 = baker.make(User, first_name="Bob")

        baker.make(Teacher, user=user1)
        baker.make(Teacher, user=user2)
        baker.make(Teacher, user=user3)

        res = retrieve_teacher(first_name="Bob")

        assert res.status_code == status.HTTP_200_OK
        assert res.data["count"] == 1
        result = res.data["results"][0]
        assert result["user"]["first_name"] == "Bob"

    def test_if_last_name_filter_working_returns_200(
        self, authenticate, retrieve_teacher
    ):
        user1 = baker.make(User, last_name="Hasan")
        user2 = baker.make(User, last_name="Hossain")
        user3 = baker.make(User, last_name="Chy")

        baker.make(Teacher, user=user1)
        baker.make(Teacher, user=user2)
        baker.make(Teacher, user=user3)

        res = retrieve_teacher(last_name="Hasan")

        assert res.status_code == status.HTTP_200_OK
        assert res.data["count"] == 1
        result = res.data["results"][0]
        assert result["user"]["last_name"] == "Hasan"

    def test_if_email_filter_working_returns_200(self, authenticate, retrieve_teacher):
        user1 = baker.make(User, email="abcd@example.com")
        user2 = baker.make(User, email="test@example.com")
        user3 = baker.make(User, email="admin@example.com")

        baker.make(Teacher, user=user1)
        baker.make(Teacher, user=user2)
        baker.make(Teacher, user=user3)

        res = retrieve_teacher(email="test")

        assert res.status_code == status.HTTP_200_OK
        assert res.data["count"] == 1
        result = res.data["results"][0]
        assert result["user"]["email"] == "test@example.com"

    def test_if_phone_filter_working_returns_200(self, authenticate, retrieve_teacher):
        user1 = baker.make(User, phone="01611759900")
        user2 = baker.make(User, phone="01611759901")
        user3 = baker.make(User, phone="01611759902")

        baker.make(Teacher, user=user1)
        baker.make(Teacher, user=user2)
        baker.make(Teacher, user=user3)

        res = retrieve_teacher(phone="01611759902")

        assert res.status_code == status.HTTP_200_OK
        assert res.data["count"] == 1
        result = res.data["results"][0]
        assert result["user"]["phone"] == "01611759902"


@pytest.mark.django_db
class TestRetrieveSingleTeacher:
    def test_if_user_is_anonymous_or_authenticated_and_has_no_data_returns_404(
        self, authenticate, retrieve_teacher
    ):
        res = retrieve_teacher(2)

        assert res.status_code == status.HTTP_404_NOT_FOUND

    def test_if_user_is_anonymous_or_authenticated_and_has_data_returns_200(
        self, authenticate, retrieve_teacher
    ):
        item1 = baker.make(Teacher)
        item2 = baker.make(Teacher)
        item3 = baker.make(Teacher)

        res = retrieve_teacher(item2.id)

        assert res.status_code == status.HTTP_200_OK
        assert res.data["id"] == item2.id
