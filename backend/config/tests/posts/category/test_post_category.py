import factories
import pytest
from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import SimpleUploadedFile
from django.db import IntegrityError

from abstract.constants import GendersPet, ImageExtension
from apps.pet.models import Pet
from infrastructure.test_data_clear import TruncateTestData

# *If you don't declare pytestmark our test class model don't accsess to database table
pytestmark = pytest.mark.django_db


# !TestPostsCategory
class TestPostsCategory:
    def test_str_method(self, category_factory):
        obj = category_factory()
        assert obj.__str__() == obj.name

    def test_slug(self, category_factory):
        obj = category_factory(name="category_1")
        assert obj.slug == obj.name.lower()

    def test_unique_name(self, category_factory):
        category_factory(name="category_1")
        with pytest.raises(IntegrityError):
            category_factory(name="category_1")

    def test_unique_slug(self, category_factory):
        obj = category_factory(name="category_1")
        with pytest.raises(IntegrityError):
            category_factory(name=obj.slug)

    def test_name_max_length(self, category_factory):
        name = "x" * 220
        slug = "y" * 240
        obj = category_factory(name=name, slug=slug)
        if len(name) > 100 or len(slug) > 100:
            with pytest.raises(ValidationError):
                obj.full_clean()
        else:
            assert len(name) <= 100
            assert len(slug) <= 100
