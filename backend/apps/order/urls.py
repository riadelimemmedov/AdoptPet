from django.urls import path

from .views import OrderView

app_name = "order"
urlpatterns = [
    path("create-checkout-session/", OrderView.as_view(), name="orders"),
]
