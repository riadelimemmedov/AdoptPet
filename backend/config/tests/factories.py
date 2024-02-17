import factory
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.db.models.signals import post_save
from faker import Faker

from abstract.constants import Genders, GendersPet, Status, Types
from apps.pet.models import Pet
from apps.user_profile.models import Profile

# Faker
faker = Faker()

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


# !ProfileFactory
@factory.django.mute_signals(post_save)
class ProfileFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Profile

    user = factory.SubFactory(UserFactory)

    first_name = "Joe"
    last_name = "Doe"
    profile_key = "abc123"
    account_type = Types[1][0]
    status = Status[1][0]
    gender = Genders[1][0]
    is_active = False


# !PetFactory
class PetFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Pet

    for _ in range(10):
        name = faker.name()
        age = faker.random_int(min=1, max=15)
        breed = faker.name()
        slug = faker.random_letters(length=12)
        color = faker.hex_color()
        weight = faker.random_int(min=1, max=50)
        gender = faker.random_element(["MALE", "FEMALE"])
        pet_photo_url = faker.file_extension(
            category="image",
        )
        location = faker.address()
        city = faker.city()
        status = faker.boolean(chance_of_getting_true=50)
        vaccinated = faker.boolean(chance_of_getting_true=50)
        description = faker.text(max_nb_chars=150)
