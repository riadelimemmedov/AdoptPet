from django.urls import path

from .views import hello_world

app_name = "users"
urlpatterns = [path("sayhello/", hello_world, name="hello_world")]
