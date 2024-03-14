from django.contrib.auth.models import User
from rest_framework import authentication, permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from abstract.constants import stripe, stripe_keys


# !OrderView
class OrderView(APIView):
    """
    Order
    """

    # def get(self, request, format=None):
    #     return Response({"message": "GET order"})

    def post(self, request, format=None):
        domain_url = "http://localhost:8001/"

        try:
            # create new checkout session for payment
            checkout_session = stripe.checkout.Session.create(
                success_url=domain_url + "success?session_id={CHECKOUT_SESSION_ID}",
                cancel_url=domain_url + "canceled",
                payment_method_types=["card"],
                mode="payment",
                line_items=[
                    {
                        "name": "Sherlock Holmes",
                        "quantity": 1,
                        "currency": "usd",
                        "amount": round(float(5) * 100),
                    }
                ],
            )
            print("checkout_session ", checkout_session)
            return Response({"sessionId": checkout_session["id"]})
        except Exception as e:
            print("e ", e)
            return Response({"message": "Please try again"})
