import pytest
from django.core.exceptions import ValidationError
from django.db import IntegrityError

# *If you don't declare pytestmark our test class model don't accsess to database table
pytestmark = pytest.mark.django_db


# !TestPostsCategory
class TestPostsCategory:
    def test_str_method(self, category_factory):
        """
        Test the __str__ method of the Category model.

        Args:
            category_factory: A factory function to create a Category instance.

        Raises:
            AssertionError: If the __str__ method does not return the expected value.

        Returns:
            None.
        """
        obj = category_factory()
        assert obj.__str__() == obj.name

    def test_slug(self, category_factory):
        """
        Test the 'slug' attribute of the Category model.

        Args:
            category_factory: A factory function to create a Category instance.

        Raises:
            AssertionError: If the 'slug' attribute does not match the expected value.

        Returns:
            None.

        """
        obj = category_factory(name="category_1")
        assert obj.slug == obj.name.lower()

    def test_unique_name(self, category_factory):
        """
        Test the uniqueness constraint of the 'name' field in the Category model.

        Args:
            category_factory: A factory function to create a Category instance.

        Raises:
            IntegrityError: If attempting to create a Category with a non-unique name raises an IntegrityError.

        Returns:
            None.

        """
        category_factory(name="category_1")
        with pytest.raises(IntegrityError):
            category_factory(name="category_1")

    def test_unique_slug(self, category_factory):
        """
        Test the uniqueness constraint of the 'slug' field in the Category model.

        Args:
            category_factory: A factory function to create a Category instance.

        Raises:
            IntegrityError: If attempting to create a Category with a non-unique slug raises an IntegrityError.

        Returns:
            None.

        """
        obj = category_factory(name="category_1")
        with pytest.raises(IntegrityError):
            category_factory(name=obj.slug)

    def test_name_max_length(self, category_factory):
        """
        Test the maximum length constraint of the 'name' and 'slug' fields in the Category model.

        Args:
            category_factory: A factory function to create a Category instance.

        Raises:
            ValidationError: If the length of 'name' or 'slug' exceeds the maximum allowed length.

        Returns:
            None.

        """
        name = "x" * 220
        slug = "y" * 240
        obj = category_factory(name=name, slug=slug)
        if len(name) > 100 or len(slug) > 100:
            with pytest.raises(ValidationError):
                obj.full_clean()
        else:
            assert len(name) <= 100
            assert len(slug) <= 100
