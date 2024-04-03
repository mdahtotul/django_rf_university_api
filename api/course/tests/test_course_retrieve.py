import pytest
from rest_framework import status
from model_bakery import baker

from core.constants import SEM_1, SEM_2, SEM_3, YEAR_1ST, YEAR_2ND, YEAR_3RD
from institute.models import Department
from course.models import Course


@pytest.fixture
def retrieve_course(api_client):
    def receive_id_params(
        id=None, name=None, department_name=None, code=None, semester=None, year=None
    ):
        url = "/api/courses/"

        if id is not None:
            url += f"{id}/"
        elif (
            name is not None
            or department_name is not None
            or code is not None
            or semester is not None
            or year is not None
        ):
            url += "?"
            params = []

            if name is not None:
                params.append(f"name={name}")
            if department_name is not None:
                params.append(f"department_name={department_name}")
            if code is not None:
                params.append(f"code={code}")
            if semester is not None:
                params.append(f"semester={semester}")
            if year is not None:
                params.append(f"year={year}")

            url += "&".join(params)

        return api_client.get(url)

    return receive_id_params


@pytest.mark.django_db
class TestRetrieveCourseList:
    def test_if_user_is_anonymous_or_authenticated_and_has_no_data_returns_200(
        self, authenticate, retrieve_course
    ):
        res = retrieve_course()

        assert res.status_code == status.HTTP_200_OK
        assert res.data["count"] == 0

    def test_if_user_is_anonymous_or_authenticated_returns_200(
        self, authenticate, retrieve_course
    ):
        baker.make(Course)
        baker.make(Course)
        baker.make(Course)

        res = retrieve_course()

        assert res.status_code == status.HTTP_200_OK
        assert res.data["count"] == 3

    def test_if_name_filter_working_returns_200(self, authenticate, retrieve_course):
        item1 = baker.make(Course, name="test")
        item2 = baker.make(Course, name="biochemistry")
        item3 = baker.make(Course, name="statistics")

        res = retrieve_course(name=item1.name)

        assert res.status_code == status.HTTP_200_OK
        assert res.data["count"] == 1
        result = res.data["results"][0]
        assert result["name"] == item1.name

    def test_if_code_filter_working_returns_200(self, authenticate, retrieve_course):
        item1 = baker.make(Course, code="test")
        item2 = baker.make(Course, code="biochemistry")
        item3 = baker.make(Course, code="statistics")

        res = retrieve_course(code=item2.code)

        assert res.status_code == status.HTTP_200_OK
        assert res.data["count"] == 1
        result = res.data["results"][0]
        assert result["code"] == item2.code

    def test_if_semester_filter_working_returns_200(
        self, authenticate, retrieve_course
    ):
        item1 = baker.make(Course, semester=SEM_1)
        item2 = baker.make(Course, semester=SEM_2)
        item3 = baker.make(Course, semester=SEM_3)

        res = retrieve_course(semester=item3.semester)

        assert res.status_code == status.HTTP_200_OK
        assert res.data["count"] == 1
        result = res.data["results"][0]
        assert result["semester"] == item3.semester

    def test_if_year_filter_working_returns_200(self, authenticate, retrieve_course):
        item1 = baker.make(Course, year=YEAR_1ST)
        item2 = baker.make(Course, year=YEAR_2ND)
        item3 = baker.make(Course, year=YEAR_3RD)
        item4 = baker.make(Course, year=YEAR_3RD)

        res = retrieve_course(year=item3.year)

        assert res.status_code == status.HTTP_200_OK
        assert res.data["count"] == 2
        result = res.data["results"][0]
        assert result["year"] == item3.year

    def test_if_department_name_filter_working_returns_200(
        self, authenticate, retrieve_course
    ):
        dept1 = baker.make(Department, name="Fisheries")
        dept2 = baker.make(Department, name="Marine")
        dept3 = baker.make(Department, name="Ocean")

        baker.make(Course, department=dept1)
        baker.make(Course, department=dept2)
        baker.make(Course, department=dept3)
        baker.make(Course, department=dept1)

        res = retrieve_course(department_name=dept1.name)

        assert res.status_code == status.HTTP_200_OK
        assert res.data["count"] == 2
        result = res.data["results"][0]
        assert result["department"]["name"] == dept1.name


@pytest.mark.django_db
class TestRetrieveCourseDetail:
    def test_if_user_is_anonymous_or_authenticated_and_has_no_data_returns_404(
        self, authenticate, retrieve_course
    ):
        res = retrieve_course(1)

        assert res.status_code == status.HTTP_404_NOT_FOUND

    def test_if_user_is_anonymous_or_authenticated_and_found_no_data_returns_404(
        self, authenticate, retrieve_course
    ):
        item = baker.make(Course)
        res = retrieve_course(item.id + 5)

        assert res.status_code == status.HTTP_404_NOT_FOUND

    def test_if_user_is_anonymous_or_authenticated_returns_200(
        self, authenticate, retrieve_course
    ):
        item = baker.make(Course)
        item1 = baker.make(Course)
        res = retrieve_course(item.id)

        assert res.status_code == status.HTTP_200_OK
        assert res.data["name"] == item.name
