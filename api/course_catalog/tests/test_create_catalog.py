import pytest
from rest_framework import status
from model_bakery import baker


from core.constants import ROLE_ADMIN, ROLE_STAFF, ROLE_USER
from course_catalog.models import Subject


@pytest.fixture
def create_subject(api_client):
    def receive_subject_instance(instance):
        return api_client.post("/api/course_catalogs/subjects/", instance)

    return receive_subject_instance


@pytest.mark.django_db
class TestCreateSubject:
    def setUp(self):
        self.subject = {"name": "test subject"}

    def test_if_user_is_anonymous_returns_401(self, authenticate, create_subject):
        self.setUp()
        res = create_subject(self.subject)

        assert res.status_code == status.HTTP_401_UNAUTHORIZED

    def test_if_user_is_user_returns_403(self, authenticate, create_subject):
        self.setUp()
        authenticate(is_staff=True, role=ROLE_USER)
        res = create_subject(self.subject)

        assert res.status_code == status.HTTP_403_FORBIDDEN

    def test_if_user_is_staff_returns_403(self, authenticate, create_subject):
        self.setUp()
        authenticate(is_staff=True, role=ROLE_STAFF)
        res = create_subject(self.subject)

        assert res.status_code == status.HTTP_403_FORBIDDEN

    def test_if_user_is_admin_returns_403(self, authenticate, create_subject):
        self.setUp()
        authenticate(is_staff=True, role=ROLE_ADMIN)
        res = create_subject(self.subject)

        assert res.status_code == status.HTTP_201_CREATED


@pytest.fixture
def create_chapter(api_client):
    def receive_chapter_instance(instance):
        return api_client.post("/api/course_catalogs/chapters/", instance)

    return receive_chapter_instance


@pytest.mark.django_db
class TestCreateChapter:
    def setUp(self):
        subject = baker.make(Subject)
        self.chapter = {"name": "test chapter", "subject": subject.id}

    def test_if_user_is_anonymous_returns_401(self, authenticate, create_chapter):
        self.setUp()
        res = create_chapter(self.chapter)

        assert res.status_code == status.HTTP_401_UNAUTHORIZED

    def test_if_user_is_user_returns_403(self, authenticate, create_chapter):
        self.setUp()
        authenticate(is_staff=True, role=ROLE_USER)
        res = create_chapter(self.chapter)

        assert res.status_code == status.HTTP_403_FORBIDDEN

    def test_if_user_is_staff_returns_403(self, authenticate, create_chapter):
        self.setUp()
        authenticate(is_staff=True, role=ROLE_STAFF)
        res = create_chapter(self.chapter)

        assert res.status_code == status.HTTP_403_FORBIDDEN

    def test_if_user_is_admin_returns_403(self, authenticate, create_chapter):
        self.setUp()
        authenticate(is_staff=True, role=ROLE_ADMIN)
        res = create_chapter(self.chapter)

        assert res.status_code == status.HTTP_201_CREATED
