import pytest
from django.contrib.auth import get_user_model

from apps.posts.models import Comment

# * If you don't declare pytestmark our test class model don't accsess to database table
pytestmark = pytest.mark.django_db

# User
User = get_user_model()


# !TestPostComment
class TestPostComment:
    def test_comment_factory_creation(
        self, comment_factory, post_factory, user_factory
    ):
        """
        Test the creation of a Comment object using the CommentFactory.

        Args:
            comment_factory: A fixture that provides a CommentFactory instance.
            post_factory: A fixture that provides a PostFactory instance.
            user_factory: A fixture that provides a UserFactory instance.

        Returns:
            None

        Raises:
            AssertionError: If any of the assertions fail.
        """
        obj = comment_factory(post=post_factory(), author=user_factory())
        assert isinstance(obj, Comment)
        assert obj.post is not None
        assert obj.author is not None
        assert obj.body is not None

    def test_str_method(self, comment_factory):
        """
        Test the __str__ method of the Comment model.

        Args:
            comment_factory: A fixture that provides a CommentFactory instance.

        Returns:
            None

        Raises:
            AssertionError: If the string representation does not match the expected format.
        """
        obj = comment_factory()
        assert obj.__str__() == f"{obj.body[:20]} by {obj.author.username}"

    def test_comment_body(self, comment_factory):
        """
        Test the body attribute of the Comment model.

        Args:
            comment_factory: A fixture that provides a CommentFactory instance.

        Returns:
            None

        Raises:
            AssertionError: If the body attribute does not contain at least one paragraph.
        """
        body = comment_factory().body.split("\n\n")
        assert len(body) >= 1
