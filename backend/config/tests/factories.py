import factory
from django.contrib.auth import get_user_model

# *User

User = get_user_model()


#! UserFactory
class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    email = factory.Sequence(lambda n: "normal_user{}@gmail.com".format(n))
    password = "foo12345"
    is_active = True
    is_staff = False
    is_superuser = False
