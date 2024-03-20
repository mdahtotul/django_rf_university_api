import pytest
from rest_framework import status

from core.constants import ROLE_ADMIN, ROLE_STAFF, ROLE_USER
from account.models import User
from address.models import Address


@pytest.fixture
def create_parent(api_client):
    def receive_parent_instance(instance):
        return api_client.post("/api/parents/", instance)

    return receive_parent_instance


@pytest.mark.django_db
class TestCreateParent:
    def setUp(self):
        user = User.objects.create_user(email="test@example", password="1234")
        address = Address.objects.create(
            building_and_street="Test Address 1",
            postal_code="1234",
            district="dhaka",
        )
        self.parent = {
            "user": user.id,
            "address": address.id,
            "occupation": "test-occupation",
        }

    def test_if_user_is_anonymous_returns_401(self, authenticate, create_parent):
        self.setUp()
        res = create_parent(self.parent)

        assert res.status_code == status.HTTP_401_UNAUTHORIZED

    def test_if_user_is_authenticated_has_invalid_data_returns_400(
        self, authenticate, create_parent
    ):
        self.setUp()
        authenticate()
        create_parent(self.parent)
        res = create_parent(self.parent)
        # cannot create parent twice with same user
        assert res.status_code == status.HTTP_400_BAD_REQUEST

    def test_if_user_is_authenticated_has_valid_data_returns_201(
        self, authenticate, create_parent
    ):
        self.setUp()
        authenticate()
        res = create_parent(self.parent)

        assert res.status_code == status.HTTP_201_CREATED

    def test_if_user_is_user_has_valid_data_returns_201(
        self, authenticate, create_parent
    ):
        self.setUp()
        authenticate(is_staff=True, role=ROLE_USER)
        res = create_parent(self.parent)

        assert res.status_code == status.HTTP_201_CREATED

    def test_if_user_is_staff_has_valid_data_returns_201(
        self, authenticate, create_parent
    ):
        self.setUp()
        authenticate(is_staff=True, role=ROLE_STAFF)
        res = create_parent(self.parent)

        assert res.status_code == status.HTTP_201_CREATED

    def test_if_user_is_admin_has_valid_data_returns_201(
        self, authenticate, create_parent
    ):
        self.setUp()
        authenticate(is_staff=True, role=ROLE_ADMIN)
        res = create_parent(self.parent)

        assert res.status_code == status.HTTP_201_CREATED
