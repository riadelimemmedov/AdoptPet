from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response

# Create your views here.


@api_view(["GET", "POST"])
def hello_world(request):
    if request.method == "POST":
        return Response({"message": "Got some data!", "data": request.data})
    return {"message": "Hello, world!"}
