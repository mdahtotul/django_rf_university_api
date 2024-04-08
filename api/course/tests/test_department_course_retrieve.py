import pytest
from rest_framework import status
from model_bakery import baker

from institute.models import Department
from course.models import Course


@pytest.fixture
def retrieve_department_course(api_client):
    def receive_id(department_id=None):
        url = f"/api/courses/department/{department_id}/"
        return api_client.get(url)

    return receive_id


@pytest.mark.django_db
class TestRetrieveDepartmentCourseList:
    def test_if_user_is_anonymous_or_authenticated_and_has_no_data_returns_404(
        self, authenticate, retrieve_department_course
    ):
        res = retrieve_department_course()

        assert res.status_code == status.HTTP_404_NOT_FOUND

    def test_if_user_is_anonymous_or_authenticated_returns_200(
        self, authenticate, retrieve_department_course
    ):
        dept1 = baker.make(Department)
        dept2 = baker.make(Department)

        baker.make(Course, department=dept1)
        baker.make(Course, department=dept1)
        baker.make(Course, department=dept1)

        baker.make(Course, department=dept2)
        baker.make(Course, department=dept2)

        res = retrieve_department_course(department_id=dept1.id)

        assert res.status_code == status.HTTP_200_OK
        assert res.data["count"] == 3
        assert res.data["results"][0]["department_id"] == dept1.id
