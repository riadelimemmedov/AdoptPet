from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import CategoryViewSet, CommentViewSet, LikePostAPIView, PostViewSet

# app name
app_name = "post"

# router
router = DefaultRouter()
router.register(r"categories", CategoryViewSet)
router.register(r"^(?P<post_slug>[-\w]+)/comment", CommentViewSet)
router.register(r"", PostViewSet)

# urlpatterns
urlpatterns = [
    path("", include(router.urls)),
    path("like/<str:slug>/", LikePostAPIView.as_view(), name="list_post"),
]
