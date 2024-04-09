import pytest
from rest_framework import status
from model_bakery import baker

from course_catalog.models import Subject, Chapter, Year


@pytest.fixture
def retrieve_subject(api_client):
    def receive_id_params(id=None, name=None, total_questions=None):
        url = "/api/course_catalogs/subjects/"

        if id is not None:
            url += f"{id}/"
        elif name is not None or total_questions is not None:
            url += "?"
            params = []

            if name is not None:
                params.append(f"name={name}")
            if total_questions is not None:
                params.append(f"total_questions={total_questions}")

            url += "&".join(params)

        return api_client.get(url)

    return receive_id_params


@pytest.mark.django_db
class TestRetrieveSubjectList:
    def test_if_user_is_anonymous_has_no_data_returns_200(
        self, authenticate, retrieve_subject
    ):
        res = retrieve_subject()

        assert res.status_code == status.HTTP_200_OK
        assert res.data["count"] == 0

    def test_if_user_is_anonymous_has_data_returns_200(
        self, authenticate, retrieve_subject
    ):
        baker.make(Subject)
        baker.make(Subject)
        baker.make(Subject)

        res = retrieve_subject()

        assert res.status_code == status.HTTP_200_OK
        assert res.data["count"] == 3

    def test_if_user_is_anonymous_has_data_filter_by_name_returns_200(
        self, authenticate, retrieve_subject
    ):
        item1 = baker.make(Subject, name="Fisheries")
        item2 = baker.make(Subject, name="Marine")
        item3 = baker.make(Subject, name="Ocean")

        res = retrieve_subject(name=item2.name)

        assert res.status_code == status.HTTP_200_OK
        assert res.data["count"] == 1
        assert res.data["results"][0]["name"] == item2.name


@pytest.mark.django_db
class TestRetrieveSingleSubject:
    def test_if_user_is_anonymous_has_no_data_returns_404(
        self, authenticate, retrieve_subject
    ):
        res = retrieve_subject(5)

        assert res.status_code == status.HTTP_404_NOT_FOUND

    def test_if_user_is_anonymous_has_data_retrieve_by_id_returns_200(
        self, authenticate, retrieve_subject
    ):
        item1 = baker.make(Subject, name="Fisheries")
        item2 = baker.make(Subject, name="Marine")
        item3 = baker.make(Subject, name="Ocean")

        res = retrieve_subject(item2.id)

        assert res.status_code == status.HTTP_200_OK
        assert res.data["name"] == item2.name


@pytest.fixture
def retrieve_chapter(api_client):
    def receive_id_params(id=None, name=None, total_questions=None):
        url = "/api/course_catalogs/chapters/"

        if id is not None:
            url += f"{id}/"
        elif name is not None or total_questions is not None:
            url += "?"
            params = []

            if name is not None:
                params.append(f"name={name}")
            if total_questions is not None:
                params.append(f"total_questions={total_questions}")

            url += "&".join(params)

        return api_client.get(url)

    return receive_id_params


@pytest.mark.django_db
class TestRetrieveChapterList:
    def test_if_user_is_anonymous_has_no_data_returns_200(
        self, authenticate, retrieve_chapter
    ):
        res = retrieve_chapter()

        assert res.status_code == status.HTTP_200_OK
        assert res.data["count"] == 0

    def test_if_user_is_anonymous_has_data_returns_200(
        self, authenticate, retrieve_chapter
    ):
        baker.make(Chapter)
        baker.make(Chapter)
        baker.make(Chapter)

        res = retrieve_chapter()

        assert res.status_code == status.HTTP_200_OK
        assert res.data["count"] == 3

    def test_if_user_is_anonymous_has_data_filter_by_name_returns_200(
        self, authenticate, retrieve_chapter
    ):
        item1 = baker.make(Chapter, name="Wetland")
        item2 = baker.make(Chapter, name="Biodiversity")
        item3 = baker.make(Chapter, name="Aquaculture")

        res = retrieve_chapter(name=item2.name)

        assert res.status_code == status.HTTP_200_OK
        assert res.data["count"] == 1
        assert res.data["results"][0]["name"] == item2.name


@pytest.mark.django_db
class TestRetrieveSingleChapter:
    def test_if_user_is_anonymous_has_no_data_returns_404(
        self, authenticate, retrieve_chapter
    ):
        res = retrieve_chapter(5)

        assert res.status_code == status.HTTP_404_NOT_FOUND

    def test_if_user_is_anonymous_has_data_retrieve_by_id_returns_200(
        self, authenticate, retrieve_chapter
    ):
        item1 = baker.make(Chapter, name="Wetland")
        item2 = baker.make(Chapter, name="Biodiversity")
        item3 = baker.make(Chapter, name="Aquaculture")

        res = retrieve_chapter(item2.id)

        assert res.status_code == status.HTTP_200_OK
        assert res.data["name"] == item2.name


@pytest.fixture
def retrieve_year(api_client):
    def receive_id_params(id=None):
        url = f"/api/course_catalogs/years/"

        if id is not None:
            url += f"{id}/"

        return api_client.get(url)

    return receive_id_params


@pytest.mark.django_db
class TestRetrieveYearList:
    def test_if_user_is_anonymous_has_no_data_returns_200(
        self, authenticate, retrieve_year
    ):
        res = retrieve_year()

        assert res.status_code == status.HTTP_200_OK

    def test_if_user_is_anonymous_has_data_returns_200(
        self, authenticate, retrieve_year
    ):
        baker.make(Year)
        baker.make(Year)
        baker.make(Year)

        res = retrieve_year()

        assert res.status_code == status.HTTP_200_OK
        assert len(res.data) == 3


@pytest.mark.django_db
class TestRetrieveSingleYear:
    def test_if_user_is_anonymous_has_no_data_returns_404(
        self, authenticate, retrieve_year
    ):
        res = retrieve_year(5)

        assert res.status_code == status.HTTP_404_NOT_FOUND

    def test_if_user_is_anonymous_has_data_retrieve_by_id_returns_200(
        self, authenticate, retrieve_year
    ):
        item1 = baker.make(Year, year="2021")
        item2 = baker.make(Year, year="2022")
        item3 = baker.make(Year, year="2023")

        res = retrieve_year(item2.id)

        assert res.status_code == status.HTTP_200_OK
        assert res.data["year"] == item2.year
