from django.contrib.auth import get_user_model
from django.test import TestCase

# Create your tests here.


# !UsersManagersTests
class UsersManagersTests(TestCase):
    def test_create_user(self):
        User = get_user_model()
        user = User.objects.create_user(email="normal_user@gmail.com", password="foo")
        self.assertEqual(user.email, "normal_user@gmail.com")
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)
        try:
            # username is None for the AbstractUser option
            # username does not exist for the AbstractBaseUser option
            self.assertIsNone(user.username)
        except (
            AttributeError
        ):  # Raised when an attribute reference (see Attribute references) or assignment fails
            pass
        with self.assertRaises(
            TypeError
        ):  # Raised when an operation or function is applied to an object of inappropriate type
            User.objects.create_user()
        with self.assertRaises(TypeError):
            User.objects.create_user(email="")
        with self.assertRaises(
            ValueError
        ):  # Raised when a built-in operation or function receives an argument that has the right type but, an inappropriate value
            User.objects.create_user(email="", password="foo")

    def test_create_superuser(self):
        User = get_user_model()
        admin_user = User.objects.create_superuser("super_user@gmail.com", "foo")
        self.assertEqual(admin_user.email, "super_user@gmail.com")
        self.assertTrue(admin_user.is_active)
        self.assertTrue(admin_user.is_staff)
        self.assertTrue(admin_user.is_superuser)
        try:
            # username is None for the AbstractUser option
            # username does not exist for the AbstractBaseUser option
            self.assertIsNone(admin_user.username)
        except (
            AttributeError
        ):  # Raised when an attribute reference (see Attribute references) or assignment fails
            pass
        with self.assertRaises(ValueError):
            User.objects.create_superuser(
                email="super_user@gmail.com", password="foo", is_superuser=False
            )
