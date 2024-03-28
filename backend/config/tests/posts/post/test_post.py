import json

import pytest
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from rest_framework import status

from apps.posts.models import Post

# * If you don't declare pytestmark our test class model don't accsess to database table
pytestmark = pytest.mark.django_db

# User
User = get_user_model()


# !TestPosts
class TestPosts:
    def test_post_factory_creation(self, post_factory, category_factory):
        """
        Test the creation of a Post instance using the post_factory.

        Args:
            post_factory: A factory function to create a Post instance.
            category_factory: A factory function to create a Category instance.

        Raises:
            AssertionError: If any of the assertions fail, indicating a test failure.

        Returns:
            None.

        """
        obj = post_factory(categories=category_factory().id)
        assert isinstance(obj, Post)
        assert obj.title is not None
        assert obj.author is not None
        assert obj.post_photo_url is not None
        assert obj.body is not None
        assert len(obj.categories.all()) > 0

    def test_str_method(self, post_factory, category_factory):
        """
        Test the __str__ method of the Post model.

        Args:
            post_factory: A factory function to create a Post instance.
            category_factory: A factory function to create a Category instance.

        Raises:
            AssertionError: If the __str__ method does not return the expected value.

        Returns:
            None.

        """
        obj = post_factory(categories=category_factory().id)
        assert obj.__str__() == f"{obj.title} by {obj.author.username}"

    def test_slug(self, post_factory):
        """
        Test the 'slug' attribute of the Post model.

        Args:
            post_factory: A factory function to create a Post instance.

        Raises:
            AssertionError: If the 'slug' attribute does not match the expected value.

        Returns:
            None.

        """
        obj = post_factory(title="System design why is the so important")
        assert obj.slug.replace("-", " ") == obj.title.lower()

    def test_unique_title(self, post_factory):
        """
        Test the uniqueness constraint of the 'title' field in the Post model.

        Args:
            post_factory: A factory function to create a Post instance.

        Raises:
            IntegrityError: If attempting to create a Post with a non-unique title raises an IntegrityError.

        Returns:
            None.

        """
        post_factory(title="Python web framework")
        with pytest.raises(IntegrityError):
            post_factory(title="Python web framework")

    def test_unique_slug(self, post_factory):
        """
        Test the uniqueness constraint of the 'slug' field in the Post model.

        Args:
            post_factory: A factory function to create a Post instance.

        Raises:
            IntegrityError: If attempting to create a Post with a non-unique slug raises an IntegrityError.

        Returns:
            None.

        """
        obj = post_factory(title="Javascript vs Elixer")
        with pytest.raises(IntegrityError):
            post_factory(title=obj.slug)

    def test_name_max_length(self, post_factory):
        """
        Test the maximum length constraint of the 'title' and 'slug' fields in the Post model.

        Args:
            post_factory: A factory function to create a Post instance.

        Raises:
            ValidationError: If the length of 'title' or 'slug' exceeds the maximum allowed length.

        Returns:
            None.

        """
        title = "x" * 280
        slug = "y" * 150
        obj = post_factory(title=title, slug=slug)
        if len(title) > 250 or len(slug) > 100:
            with pytest.raises(ValidationError):
                obj.full_clean()
        else:
            assert len(title) <= 250
            assert len(slug) <= 100

    def test_post_factory_with_categories(self, post_factory, category_factory):
        """
        Test the creation of a Post instance with associated categories using the post_factory.

        Args:
            post_factory: A factory function to create a Post instance.
            category_factory: A factory function to create a Category instance.

        Raises:
            AssertionError: If any of the assertions fail, indicating a test failure.

        Returns:
            None.

        """
        category = category_factory().id
        post = post_factory(categories=category)
        assert isinstance(post, Post)
        assert post.categories.count() == 1
        assert Post.objects.filter(categories__id=category).exists()
