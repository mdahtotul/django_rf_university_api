import pytest
from rest_framework import status

from core.constants import ROLE_ADMIN, ROLE_STAFF, ROLE_USER


@pytest.fixture
def create_address(api_client):
    def receive_address_instance(instance):
        return api_client.post("/api/addresses/", instance)

    return receive_address_instance


@pytest.mark.django_db
class TestCreateAddress:
    def setUp(self):
        self.address = {
            "building_and_street": "Test Address 1",
            "postal_code": "1234",
            "district": "dhaka",
        }

    def test_if_user_is_anonymous_returns_401(self, authenticate, create_address):
        self.setUp()
        res = create_address(self.address)

        assert res.status_code == status.HTTP_401_UNAUTHORIZED

    def test_if_user_is_authenticated_has_invalid_building_and_street_returns_400(
        self, authenticate, create_address
    ):
        self.setUp()
        authenticate()

        self.address["building_and_street"] = ""
        res = create_address(self.address)

        assert res.status_code == status.HTTP_400_BAD_REQUEST

    def test_if_user_is_authenticated_has_invalid_postal_code_returns_400(
        self, authenticate, create_address
    ):
        self.setUp()
        authenticate()

        self.address["postal_code"] = ""
        res = create_address(self.address)

        assert res.status_code == status.HTTP_400_BAD_REQUEST

    def test_if_user_is_authenticated_has_invalid_district_returns_400(
        self, authenticate, create_address
    ):
        self.setUp()
        authenticate()

        self.address["district"] = "Dhaka"  # invalid district because valid is dhaka
        res = create_address(self.address)

        assert res.status_code == status.HTTP_400_BAD_REQUEST

    def test_if_user_is_authenticated_has_valid_data_returns_200(
        self, authenticate, create_address
    ):
        self.setUp()
        authenticate()

        res = create_address(self.address)

        assert res.status_code == status.HTTP_201_CREATED

    def test_if_user_is_user_has_valid_data_returns_200(
        self, authenticate, create_address
    ):
        self.setUp()
        authenticate(is_staff=True, role=ROLE_USER)

        res = create_address(self.address)

        assert res.status_code == status.HTTP_201_CREATED

    def test_if_user_is_staff_has_valid_data_returns_200(
        self, authenticate, create_address
    ):
        self.setUp()
        authenticate(is_staff=True, role=ROLE_STAFF)

        res = create_address(self.address)

        assert res.status_code == status.HTTP_201_CREATED

    def test_if_user_is_admin_has_valid_data_returns_200(
        self, authenticate, create_address
    ):
        self.setUp()
        authenticate(is_staff=True, role=ROLE_ADMIN)

        res = create_address(self.address)

        assert res.status_code == status.HTTP_201_CREATED
