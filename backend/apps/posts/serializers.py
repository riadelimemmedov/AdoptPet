from django.core.exceptions import ValidationError
from rest_framework import serializers

from .models import Category, Comment, Post


# !CategoryReadSerializer
class CategoryReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"


# !CategoryWriteSerializer
class CategoryWriteSerializer(serializers.ModelSerializer):
    slug = serializers.ReadOnlyField(read_only=True)

    class Meta:
        model = Category
        fields = ["name", "slug"]


# !PostReadSerializer
class PostReadSerializer(serializers.ModelSerializer):
    author = serializers.CharField(source="author.username", read_only=True)
    categories = serializers.SerializerMethodField(read_only=True)
    likes = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Post
        fields = "__all__"

    def get_categories(self, obj):
        categories = list(
            category.name for category in obj.categories.get_queryset().only("name")
        )
        return categories

    def get_likes(self, obj):
        likes = list(
            like.username for like in obj.likes.get_queryset().only("username")
        )
        return likes


# !PostWriteSerializer
class PostWriteSerializer(serializers.ModelSerializer):
    author = serializers.HiddenField(default=serializers.CurrentUserDefault())
    post_photo_url = serializers.FileField(
        allow_empty_file=False,
        use_url=False,
        required=True,
    )

    class Meta:
        model = Post
        exclude = ["slug"]

    def validate_categories(self, categories):
        if len(categories) <= 0:
            raise serializers.ValidationError(
                "Categories cannot be empty,please add category for added post"
            )
        return categories


# !CommentReadSerializer
class CommentReadSerializer(serializers.ModelSerializer):
    author = serializers.CharField(source="author.username", read_only=True)

    class Meta:
        model = Comment
        fields = "__all__"


# !CommentWriteSerializer
class CommentWriteSerializer(serializers.ModelSerializer):
    author = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Comment
        fields = ["author", "body"]
