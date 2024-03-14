import pytest
from rest_framework import status
from model_bakery import baker

from address.constants import DIST_BARISHAL, DIST_DHAKA
from address.models import Address
from core.constants import ROLE_ADMIN, ROLE_STAFF


@pytest.fixture
def retrieve_and_update_address(api_client):
    def receive_instance(instance, id=None):
        return api_client.patch(f"/api/addresses/{id}/", instance)

    return receive_instance


@pytest.mark.django_db
class TestUpdateAddress:
    def test_if_user_is_anonymous_returns_401(
        self, api_client, retrieve_and_update_address
    ):
        item = baker.make(Address)

        payload = {
            "building_and_street": "test",
        }

        res = retrieve_and_update_address(payload, item.id)

        assert res.status_code == status.HTTP_401_UNAUTHORIZED

    def test_if_user_is_not_admin_returns_403(
        self, authenticate, retrieve_and_update_address
    ):
        item = baker.make(Address)
        authenticate(is_staff=True, role=ROLE_STAFF)

        payload = {
            "building_and_street": "test",
        }

        res = retrieve_and_update_address(payload, item.id)

        assert res.status_code == status.HTTP_403_FORBIDDEN

    def test_if_user_is_admin_item_not_exist_returns_404(
        self, authenticate, retrieve_and_update_address
    ):
        item = baker.make(Address)
        authenticate(is_staff=True, role=ROLE_ADMIN)

        payload = {
            "building_and_street": "test",
        }

        res = retrieve_and_update_address(payload, item.id + 5)

        assert res.status_code == status.HTTP_404_NOT_FOUND

    def test_if_user_is_admin_has_invalid_data_returns_400(
        self, authenticate, retrieve_and_update_address
    ):
        item = baker.make(Address)
        authenticate(is_staff=True, role=ROLE_ADMIN)

        payload = {
            "building_and_street": "test",
            "district": "test",  # invalid data
        }

        res = retrieve_and_update_address(payload, item.id)

        assert res.status_code == status.HTTP_400_BAD_REQUEST

    def test_if_user_is_admin_has_valid_data_returns_200(
        self, authenticate, retrieve_and_update_address
    ):
        item = baker.make(Address, district=DIST_DHAKA)
        authenticate(is_staff=True, role=ROLE_ADMIN)

        payload = {
            "building_and_street": "test",
            "district": DIST_BARISHAL,  # invalid data
        }

        res = retrieve_and_update_address(payload, item.id)

        assert res.status_code == status.HTTP_200_OK
        assert res.data["id"] == item.id
        assert res.data["building_and_street"] == payload["building_and_street"]
        assert res.data["district"] == payload["district"]


@pytest.fixture
def delete_address(api_client):
    def receive_id(id=None):
        return api_client.delete(f"/api/addresses/{id}/")

    return receive_id


@pytest.mark.django_db
class TestDeleteAddress:
    def test_if_user_is_anonymous_returns_401(self, authenticate, delete_address):
        item = baker.make(Address)
        baker.make(Address)

        res = delete_address(item.id)

        assert res.status_code == status.HTTP_401_UNAUTHORIZED

    def test_if_user_is_not_admin_returns_403(self, authenticate, delete_address):
        item = baker.make(Address)
        baker.make(Address)
        authenticate(is_staff=True, role=ROLE_STAFF)

        res = delete_address(item.id)

        assert res.status_code == status.HTTP_403_FORBIDDEN

    def test_if_user_is_admin_item_not_exist_returns_404(
        self, authenticate, delete_address
    ):
        item = baker.make(Address)
        baker.make(Address)
        authenticate(is_staff=True, role=ROLE_ADMIN)

        res = delete_address(item.id + 5)

        assert res.status_code == status.HTTP_404_NOT_FOUND

    def test_if_user_is_admin_item_not_exist_returns_204(
        self, authenticate, delete_address
    ):
        item = baker.make(Address)
        baker.make(Address)
        authenticate(is_staff=True, role=ROLE_ADMIN)

        res = delete_address(item.id)

        address = Address.objects.filter(id=item.id).first()

        assert res.status_code == status.HTTP_204_NO_CONTENT
        assert res.data is None
        assert address is None
