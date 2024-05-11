from decimal import Decimal
from django.db import transaction
from django.forms.models import model_to_dict

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import *

from core.constants import ENROLL_F, ENROLL_S
from core.exceptions import BadRequest
from core.utils import format_exception
from core.permissions import AdminOnly, UserOnly
from institute.models import Department
from people.models import Student

from .models import Enroll, Payment
from .ssl import PaymentGatewayService

payment_service = PaymentGatewayService()


class PaymentView(APIView):
    permission_classes = [UserOnly | AdminOnly]

    def post(self, request):
        try:
            with transaction.atomic():
                id = request.user.id
                email = request.user.email
                amount = request.data.get("amount")
                phone = request.data.get("phone") or request.user.phone
                product_id = request.data.get("product_id")

                if id is None:
                    raise BadRequest("User id not found!")
                if email is None or email == "":
                    raise BadRequest("User email not found!")
                if phone is None or phone == "":
                    raise BadRequest("User mobile number not found!")
                if amount is None or int(amount) <= 0 or amount == "":
                    raise BadRequest("Amount must be greater than 0!")
                if product_id is None or product_id == "":
                    raise BadRequest("Please provide a product id to initiate payment!")

                student = Student.objects.filter(user_id=id).first()
                if student is None:
                    raise BadRequest(
                        "This user don't belong to any student! Please create a student first with this user."
                    )

                product = Department.objects.filter(id=product_id).first()

                result = payment_service.ssl_payment_gateway(
                    request=request,
                    user_id=student.id,
                    product_id=product_id,
                    amount=Decimal(amount),
                    email=email,
                    phone=phone,
                    product=product.name,
                )
                return Response(result, status=HTTP_200_OK)
        except Exception as e:
            raise e

    def handle_exception(self, exc):
        return format_exception(exc, self.request)


class PaymentSubmitView(APIView):

    def post(self, request):
        try:
            with transaction.atomic():
                payment_data = request.POST
                customer_id = int(payment_data["value_a"])
                department_id = int(payment_data["value_b"])
                customer_email = payment_data["value_c"]
                student = Student.objects.get(id=customer_id)
                department = Department.objects.get(id=department_id)

                if payment_data["status"] == "VALID":
                    # storing data to payment table
                    payment = Payment.objects.create(
                        student=student,
                        trx_id=payment_data["tran_id"],
                        method=payment_data["card_issuer"],
                        amount=Decimal(payment_data["amount"]),
                        store_amount=Decimal(payment_data["store_amount"]),
                        status=ENROLL_S,
                    )

                    # storing data to enroll table
                    enroll = Enroll.objects.create(
                        student=student,
                        department=department,
                        payment=payment,
                        price=Decimal(
                            payment_data["amount"],
                        ),
                    )
                    return Response(
                        {
                            "data": {
                                "payment": model_to_dict(payment),
                                "enroll": model_to_dict(enroll),
                            }
                        },
                        status=HTTP_200_OK,
                    )
                if payment_data["status"] == "FAILED":
                    # storing data to payment table
                    payment = Payment.objects.create(
                        student=student,
                        trx_id=payment_data["tran_id"],
                        method=payment_data["card_issuer"],
                        amount=Decimal(payment_data["amount"]),
                        status=ENROLL_F,
                        failed_reason=payment_data["error"],
                    )
                    return Response(
                        {"data": model_to_dict(payment)}, status=HTTP_200_OK
                    )
        except Exception as e:
            raise e

    def handle_exception(self, exc):
        return format_exception(exc, self.request)
