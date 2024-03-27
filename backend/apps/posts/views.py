from django.shortcuts import get_object_or_404, render
from rest_framework import permissions, status, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Category, Comment, Post
from .permissions import IsAuthorOrReadOnly
from .serializers import (
    CategoryReadSerializer,
    CategoryWriteSerializer,
    CommentReadSerializer,
    CommentWriteSerializer,
    PostReadSerializer,
    PostWriteSerializer,
)

# Create your views here.


# !CategoryViewSet
class CategoryViewSet(viewsets.ModelViewSet):
    """
    List,Retrieve and Create post categories
    """

    queryset = Category.objects.all()
    permission_classes = [permissions.AllowAny]
    lookup_field = "slug"

    def get_serializer_class(self):
        if self.action in ("create", "update", "partial_update", "destroy"):
            return CategoryWriteSerializer
        return CategoryReadSerializer

    def get_permissions(self):
        if self.action in ("create", "update", "partial_update", "destroy"):
            self.permission_classes = [permissions.IsAdminUser]
        return super().get_permissions()


# !PostViewSet
class PostViewSet(viewsets.ModelViewSet):
    """
    CRUD posts
    """

    queryset = Post.objects.all()
    lookup_field = "slug"

    # In order to use different serializers for different
    # actions, you can override the
    # get_serializer_class(self) method
    def get_serializer_class(self):
        if self.action in ("create", "update", "partial_update", "destroy"):
            return PostWriteSerializer
        return PostReadSerializer

    # get_permissions(self) method helps you separate
    # permissions for different actions inside the same view.
    def get_permissions(self):
        if self.action in ("create",):
            self.permission_classes = [permissions.IsAuthenticated]
        elif self.action in ("update", "partial_update", "destroy"):
            self.permission_classes = [IsAuthorOrReadOnly]
        else:
            self.permission_classes = [permissions.AllowAny]
        return super().get_permissions()


# !CommentViewSet
class CommentViewSet(viewsets.ModelViewSet):
    """
    CRUD comments for a particular post
    """

    queryset = Comment.objects.all()
    # lookup_field = "slug"

    def get_queryset(self):
        response = super().get_queryset()
        post_slug = self.kwargs.get("post_slug")
        return response.filter(post__slug=post_slug)

    def create(self, request, *args, **kwargs):
        post_slug = self.kwargs.get("post_slug")
        post = Post.objects.get(slug=post_slug)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(post=post)
        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED,
        )

    def get_serializer_class(self):
        if self.action in ("create", "update", "partial_update", "destroy"):
            return CommentWriteSerializer
        return CommentReadSerializer

    def get_permissions(self):
        if self.action in ("create",):
            self.permission_classes = (permissions.IsAuthenticated,)
        elif self.action in ("update", "partial_update", "destroy"):
            self.permission_classes = (IsAuthorOrReadOnly,)
        else:
            self.permission_classes = (permissions.AllowAny,)
        return super().get_permissions()


# Here, we are using the normal APIView class
# !LikePostAPIView
class LikePostAPIView(APIView):
    """
    Like, Dislike a post
    """

    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, slug):
        user = request.user
        post = get_object_or_404(Post, slug=slug)

        if user in post.likes.all():
            post.likes.remove(user)
        else:
            post.likes.add(user)
        return Response(status=status.HTTP_200_OK)
