import factory
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.db.models.signals import post_save
from faker import Faker

from abstract.constants import Genders, GendersPet, Status, Types
from apps.pet.models import Pet
from apps.transaction.models import Transaction
from apps.user_profile.models import Profile
from config.helpers import generate_metamask_address, generate_session_id

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
        pet_photo_link = faker.url()
        location = faker.address()
        city = faker.city()
        status = faker.boolean(chance_of_getting_true=50)
        vaccinated = faker.boolean(chance_of_getting_true=50)
        price = faker.pyfloat(
            positive=True, right_digits=2, left_digits=4, min_value=25, max_value=9999
        )
        description = faker.text(max_nb_chars=150)


# !PetFactoryEndToEnd
class PetFactoryEndToEnd(factory.django.DjangoModelFactory):
    class Meta:
        model = Pet

    name = factory.LazyAttribute(lambda _: faker.name())
    age = factory.LazyAttribute(lambda _: faker.random_int(min=1, max=15))
    breed = factory.LazyAttribute(lambda _: faker.name())
    slug = factory.LazyAttribute(lambda _: faker.random_letters(length=12))
    color = factory.LazyAttribute(lambda _: faker.hex_color())
    weight = factory.LazyAttribute(lambda _: faker.random_int(min=1, max=50))
    gender = factory.LazyAttribute(lambda _: faker.random_element(["MALE", "FEMALE"]))
    pet_photo_url = factory.LazyAttribute(
        lambda _: faker.file_extension(category="image")
    )
    pet_photo_url = factory.LazyAttribute(lambda _: faker.url())
    location = factory.LazyAttribute(lambda _: faker.address())
    city = factory.LazyAttribute(lambda _: faker.city())
    status = factory.LazyAttribute(lambda _: faker.boolean(chance_of_getting_true=50))
    vaccinated = factory.LazyAttribute(
        lambda _: faker.boolean(chance_of_getting_true=50)
    )
    description = factory.LazyAttribute(lambda _: faker.text(max_nb_chars=150))


# !TransactionFactory
class TransactionFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Transaction

    from_user = factory.LazyAttribute(lambda _: generate_metamask_address())
    confirmations = factory.LazyAttribute(lambda _: faker.random_int(min=0, max=1))
    value = factory.LazyAttribute(
        lambda _: str(
            faker.pyfloat(
                positive=True,
                right_digits=2,
                left_digits=4,
                min_value=25,
                max_value=9999,
            )
        )
    )
    adopted_pet_slug = factory.LazyAttribute(lambda _: faker.slug())
    payment_options = factory.LazyAttribute(
        lambda _: faker.random_element(["STRIPE", "ETHEREUM"])
    )
    session_id = factory.LazyAttribute(lambda _: generate_session_id())
