import pytest

from rest_framework import status
from model_bakery import baker

from address.models import Address


@pytest.fixture
def retrieve_address(api_client):
    def receive_id(id=None):
        if id is not None:
            return api_client.get(f"/api/addresses/{id}/")
        else:
            return api_client.get("/api/addresses/")

    return receive_id


@pytest.mark.django_db
class TestRetrieveListAddresses:
    def test_if_user_is_anonymous_or_authenticated_and_has_no_data_returns_200(
        self, authenticate, retrieve_address
    ):
        res = retrieve_address()

        assert res.status_code == status.HTTP_200_OK
        assert len(res.data) == 0

    def test_if_user_is_anonymous_or_authenticated_returns_200(
        self, authenticate, retrieve_address
    ):
        baker.make(Address)
        baker.make(Address)
        baker.make(Address)

        res = retrieve_address()

        assert res.status_code == status.HTTP_200_OK
        assert len(res.data) == 3


@pytest.mark.django_db
class TestRetrieveSingleAddress:
    def test_if_user_is_anonymous_or_authenticated_and_has_no_data_returns_404(
        self, authenticate, retrieve_address
    ):
        res = retrieve_address(2)

        assert res.status_code == status.HTTP_404_NOT_FOUND

    def test_if_user_is_anonymous_or_authenticated_returns_200(
        self, authenticate, retrieve_address
    ):
        item1 = baker.make(Address)
        item2 = baker.make(Address)
        item3 = baker.make(Address)

        res = retrieve_address(item2.id)

        assert res.status_code == status.HTTP_200_OK
        assert res.data["id"] == item2.id
        assert res.data["building_and_street"] == item2.building_and_street
