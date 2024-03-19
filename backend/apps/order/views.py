import json

from django.contrib.auth.models import User
from rest_framework import authentication, permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from abstract.constants import stripe, stripe_keys
from apps.transaction.helpers import save_transaction


# !OrderView
class OrderView(APIView):
    """
    Order
    """

    # def get(self, request, format=None):
    #     return Response({"message": "GET order"})

    def post(self, request, format=None):
        domain_url = "http://localhost:8001/"
        body = json.loads(request.body.decode("utf-8"))
        line_items = []
        pet_data = []
        for pet in body["pets"]:
            item = {
                "name": str(pet[2]),
                "quantity": 1,
                "currency": "usd",
                "amount": round(int(pet[4]["hex"], 16) * 100),
            }
            pet_data.append(
                {
                    "adopted_pet_slug": str(pet[1]),
                    "value": round(int(pet[4]["hex"], 16) * 100),
                }
            )
            line_items.append(item)
        try:
            # create new checkout session for payment
            checkout_session = stripe.checkout.Session.create(
                success_url=domain_url + "success?session_id={CHECKOUT_SESSION_ID}",
                cancel_url=domain_url + "canceled",
                payment_method_types=["card"],
                mode="payment",
                line_items=line_items,
            )
            save_transaction(
                checkout_session["id"], pet_data, body["from_user"], "STRIPE"
            )
            return Response({"sessionId": checkout_session["id"]})
        except Exception:
            return Response({"message": "Please try again"})
