from django.urls import path

from .views import PetDetailAPIView, PetView

app_name = "pet"
urlpatterns = [
    path("", PetView.as_view(), name="pets"),
    path("<str:slug>/", PetDetailAPIView.as_view(), name="pet"),
]
