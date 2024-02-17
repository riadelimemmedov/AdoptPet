from enum import Enum

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
