from django.conf import settings
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import UploadSerializer


# Create your views here.
class UploadViewSet(APIView):
    serializer_class = UploadSerializer

    def list(self, request):
        return Response("GET API")

    def post(self, request, format=None):
        file = request.FILES.get("file")
        print("File ", file)
        serializer = self.serializer_class(data=request.data)
        if settings.USE_S3:
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=201)
        else:
            error_data = {"error": "No file uploaded"}
            return Response(error_data, status=400)
