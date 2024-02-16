from django.urls import path

from .views import UploadViewSet

app_name = "upload"
urlpatterns = [path("image/", UploadViewSet.as_view(), name="image")]
