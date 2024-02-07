import factory
from django.contrib.auth import get_user_model

# *User

User = get_user_model()


# !UserFactory
class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    email = factory.Sequence(lambda n: "normal_user{}@gmail.com".format(n))
    password = "foo12345"
    is_active = True

    @classmethod
    def create_user(cls, **kwargs):
        kwargs["is_staff"] = False
        kwargs["is_superuser"] = False
        return super().create(**kwargs)

    @classmethod
    def create_superuser(cls, **kwargs):
        if not kwargs["is_superuser"] or not kwargs["is_staff"]:
            raise ValueError("Superuser must have is_superuser=True and is_staff=True.")
        else:
            kwargs["is_staff"] = True
            kwargs["is_superuser"] = True
        return super().create(**kwargs)
