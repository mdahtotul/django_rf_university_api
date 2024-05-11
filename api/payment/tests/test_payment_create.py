import pytest
from rest_framework import status
from model_bakery import baker

from institute.models import Department
from people.models import Student
from account.models import User


@pytest.fixture
def create_payment(api_client):
    def receive_payment_instance(instance):
        return api_client.post("/api/payment/", data=instance, format="multipart")

    return receive_payment_instance


@pytest.mark.django_db
class TestPaymentCreate:
    def setup_method(self):
        self.user = baker.make(User, password="12345", email="test@example.com")
        self.student = baker.make(Student, user=self.user)
        self.department = baker.make(Department)
        self.payload = {
            "user_id": self.student.id,
            "amount": 100,
            "email": self.user.email,
            "phone": "01611759902",
            "product_id": self.department.id,
            "product_name": self.department.name,
        }

    def test_initiate_payment_success_returns_200(
        self, api_client, create_payment, monkeypatch
    ):
        def mock_create_session(*args, **kwargs):
            return {
                "status": "SUCCESS",
                "sessionkey": "dummy_session_key",
                "redirectGatewayURL": "dummy_redirect_url",
                "GatewayPageURL": "dummy_gateway_url",
            }

        monkeypatch.setattr("payment.ssl.SSLCOMMERZ.createSession", mock_create_session)

        api_client.force_authenticate(user=self.user)

        res = create_payment(self.payload)

        assert res.status_code == status.HTTP_200_OK
        data = res.json()
        assert data.get("status") == "SUCCESS"
        assert data.get("tran_id") is not None
        assert data.get("redirect_url") is not None

    def test_initiate_payment_failed_for_no_amount_returns_400(
        self, api_client, create_payment, monkeypatch
    ):
        def mock_create_session(*args, **kwargs):
            return {
                "status": "FAILED",
                "failedreason": "dummy_failed_reason",
            }

        monkeypatch.setattr("payment.ssl.SSLCOMMERZ.createSession", mock_create_session)

        api_client.force_authenticate(user=self.user)

        del self.payload["amount"]
        res = create_payment(self.payload)

        assert res.status_code == status.HTTP_400_BAD_REQUEST

    def test_initiate_payment_failed_for_no_phone_returns_400(
        self, api_client, create_payment, monkeypatch
    ):
        def mock_create_session(*args, **kwargs):
            return {
                "status": "FAILED",
                "failedreason": "dummy_failed_reason",
            }

        monkeypatch.setattr("payment.ssl.SSLCOMMERZ.createSession", mock_create_session)

        api_client.force_authenticate(user=self.user)

        del self.payload["phone"]
        res = create_payment(self.payload)

        assert res.status_code == status.HTTP_400_BAD_REQUEST

    def test_initiate_payment_failed_for_no_product_id_returns_400(
        self, api_client, create_payment, monkeypatch
    ):
        def mock_create_session(*args, **kwargs):
            return {
                "status": "FAILED",
                "failedreason": "dummy_failed_reason",
            }

        monkeypatch.setattr("payment.ssl.SSLCOMMERZ.createSession", mock_create_session)

        api_client.force_authenticate(user=self.user)

        del self.payload["product_id"]
        res = create_payment(self.payload)

        assert res.status_code == status.HTTP_400_BAD_REQUEST

    def test_initiate_payment_failed_for_no_user_id_returns_500(
        self, api_client, create_payment, monkeypatch
    ):
        def mock_create_session(*args, **kwargs):
            return {
                "status": "FAILED",
                "failedreason": "dummy_failed_reason",
            }

        monkeypatch.setattr("payment.ssl.SSLCOMMERZ.createSession", mock_create_session)

        api_client.force_authenticate(user=self.user)

        del self.payload["user_id"]
        res = create_payment(self.payload)

        assert res.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
        assert res.json()["details"] == mock_create_session().get("failedreason")

    def test_initiate_payment_failed_for_no_user_email_returns_500(
        self, api_client, create_payment, monkeypatch
    ):
        def mock_create_session(*args, **kwargs):
            return {
                "status": "FAILED",
                "failedreason": "dummy_failed_reason",
            }

        monkeypatch.setattr("payment.ssl.SSLCOMMERZ.createSession", mock_create_session)

        api_client.force_authenticate(user=self.user)

        del self.payload["email"]
        res = create_payment(self.payload)

        assert res.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
        assert res.json()["details"] == mock_create_session().get("failedreason")


@pytest.fixture
def submit_payment(api_client):
    def receive_payment_instance(instance):
        return api_client.post(
            "/api/payment/submit/", data=instance, format="multipart"
        )

    return receive_payment_instance


@pytest.mark.django_db
class TestPaymentSubmit:

    def setup_method(self):
        self.student = baker.make(Student)
        self.department = baker.make(Department)
        self.payload = {
            "status": "VALID",
            "value_a": str(self.student.id),
            "value_b": str(self.department.id),
            "value_c": "test@example.com",
            "tran_id": "123456789",
            "card_issuer": "VISA",
            "amount": "100.00",
            "store_amount": "95.00",
        }

    def test_payment_submit_status_valid(self, submit_payment):
        res = submit_payment(self.payload)

        assert res.status_code == status.HTTP_200_OK
        assert "payment" in res.data["data"]
        assert "enroll" in res.data["data"]

    def test_payment_submit_status_failed(self, submit_payment):
        self.payload["status"] = "FAILED"
        self.payload["error"] = "test error message"
        del self.payload["store_amount"]

        res = submit_payment(self.payload)

        assert res.status_code == status.HTTP_200_OK
        assert "payment" not in res.data["data"]
        assert "enroll" not in res.data["data"]

    def test_payment_submit_status_not_success_or_failed(self, submit_payment):
        self.payload["status"] = "SUCCESS"

        res = submit_payment(self.payload)

        assert res.status_code == status.HTTP_400_BAD_REQUEST
