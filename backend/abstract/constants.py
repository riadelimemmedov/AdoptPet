from enum import Enum

import stripe
from decouple import config
from django.utils.translation import gettext_lazy as _


# !AppName
class AppName(Enum):
    ADMIN = "ADMIN"
    USER = "USER"


# !Types
Types = [("ADMIN", _("admin")), ("GENERAL", _("general"))]

# !Status
Status = [("ACTIVE", _("active")), ("INACTIVE", _("inactive"))]

# !Genders
Genders = [("MALE", _("male")), ("FEMALE", _("female"))]

# !Genders Pet
GendersPet = [
    ("MALE", _("male")),
    ("FEMALE", _("female")),
    ("Neutered ", _("neutered ")),
    ("Spayed", _("spayed")),
    ("Other", _("other")),
]

# !Image Extension
ImageExtension = ["png", "jpg", "jpeg"]


# !PaymentMethods
PaymentOptions = [
    ("STRIPE", _("stripe")),
    ("ETHEREUM", _("ethereum")),
]

# !Configure stripe
stripe_keys = {
    "secret_key": config("STRIPE_SECRET_KEY"),
    "publishable_key": config("STRIPE_PUBLISHABLE_KEY"),
}
stripe.api_key = stripe_keys["secret_key"]


# session = stripe.checkout.Session.retrieve(
#     "cs_test_b1vTOtKpWL95zEGz7wg7BrsGmVZeLUGufdnarAq3BW7jWtMiScuNYkL8pV"
# )


# payment_intent = stripe.PaymentIntent.retrieve(session["payment_intent"])
# print("Payment intend value ", payment_intent)
