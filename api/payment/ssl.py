import os
import string
import random

from sslcommerz_lib import SSLCOMMERZ


class PaymentGatewayService:
    def unique_trx_id_generator(
        self, size=10, chars=string.ascii_uppercase + string.digits
    ):
        return "".join(random.choice(chars) for _ in range(size))

    def get_name(self, request):
        name = ""
        if request.user.first_name and request.user.last_name:
            name = f"{request.user.first_name} {request.user.last_name}"
        elif request.user.first_name:
            name = request.user.first_name
        elif request.user.last_name:
            name = request.user.last_name
        return name

    def ssl_payment_gateway(
        self,
        request,
        user_id,
        product_id,
        amount,
        email,
        phone,
        product,
    ):
        try:
            settings = {
                "store_id": os.environ.get("SSL_STORE_ID"),
                "store_pass": os.environ.get("SSL_STORE_PASS"),
                "issandbox": os.environ.get("SSL_TEST_MODE"),
            }
            domain = os.environ.get("BACKEND_DOMAIN")

            sslcz = SSLCOMMERZ(settings)
            post_body = {
                "total_amount": amount,
                "currency": "BDT",
                "tran_id": self.unique_trx_id_generator(),  # tran_id must be unique
                "success_url": f"{domain}/payment/submit/",
                "fail_url": f"{domain}/payment/submit/",
                "cancel_url": f"{domain}/",
                "emi_option": 0,
                "cus_name": (
                    self.get_name(request) if self.get_name(request) else email
                ),
                "cus_email": email,
                "cus_phone": phone,
                "cus_add1": "N/A",
                "cus_city": "N/A",
                "cus_country": "N/A",
                "shipping_method": "NO",
                "multi_card_name": "",
                "num_of_item": 1,
                "product_name": product,
                "product_category": "University Admission",
                "product_profile": "general",
                # optional parameters (store additional data that can be used later in status query)
                "value_a": user_id,  # store customer id here
                "value_b": product_id,  # store order/product id here
                "value_c": email,
            }

            response = sslcz.createSession(post_body)

            if response.get("status") == "SUCCESS":
                url = (
                    "https://sandbox.sslcommerz.com/gwprocess/v4/gw.php?Q=pay&SESSIONKEY="
                    + response.get("sessionkey")
                )
                result = {
                    "status": response.get("status"),
                    "tran_id": post_body.get("tran_id"),
                    "redirect_url": url,
                    "redirect_gateway_url": response.get("redirectGatewayURL"),
                    "gateway_page_url": response.get("GatewayPageURL"),
                }

                return result
            elif response.get("status") == "FAILED":
                raise Exception(response.get("failedreason"))

        except Exception as e:
            raise e
