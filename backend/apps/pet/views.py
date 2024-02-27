from django.conf import settings
from django.core.cache import cache
from django.core.files.storage import FileSystemStorage
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Pet
from .pagination import PetPagination
from .serializers import PetSerializer

# Create your views here.


# !PetView
class PetView(APIView):
    """PetView"""

    serializer_class = PetSerializer
    pagination_class = PetPagination

    # @method_decorator(cache_page(60 * 60 * 2, key_prefix="pet_objects"))
    def get(self, request):
        """
        Retrieve a list of all pets.

        Parameters:
            request (HttpRequest): The HTTP request object.

        Returns:
            Response: A response object containing the serialized data of all pets and the HTTP status code.
        """
        pet_objects = cache.get("pet_objects")
        paginator = self.pagination_class()  # Use the desired pagination class

        page_number = request.query_params.get("page")
        print("Page number ", page_number)

        if pet_objects is None:
            pet_objects = paginator.paginate_queryset(Pet.objects.all(), request)
            cache.set("pet_objects", pet_objects, 60 * 3)

        # pet_objects = Pet.objects.all()
        serializer = self.serializer_class(pet_objects, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, format=None):
        """
        Create a new pet.

        Parameters:
            request (HttpRequest): The HTTP request object.
            format (str): The format of the request data (optional).

        Returns:
            Response: A response object containing the serialized data of the created pet and the HTTP status code.
        """
        pet_photo_url = request.FILES.get("pet_photo_url")
        print("Pet photo url: ", pet_photo_url)
        serializer = self.serializer_class(data=request.data)
        if settings.USE_S3:
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=201)
        else:
            if serializer.is_valid():
                if pet_photo_url:
                    fs = FileSystemStorage()
                    filename = fs.save(pet_photo_url.name, pet_photo_url)
                    image_url = fs.url(filename)
                    print("Image url: ", image_url)
                else:
                    error_data = {"error": "No file uploaded"}
                    return Response(error_data, status=status.HTTP_400_BAD_REQUEST)
                serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete(self, request):
        """
        Delete all pets.

        Parameters:
            request (HttpRequest): The HTTP request object.

        Returns:
            Response: A response object with no content and the HTTP status code indicating success.
        """
        Pet.objects.all().delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# !PetDetailAPIView
class PetDetailAPIView(APIView):
    """PetDetailView"""

    serializer_class = PetSerializer

    def get_object(self, slug):
        """
        Retrieve a pet object based on its slug.

        Parameters:
            slug (str): The slug of the pet.

        Returns:
            Pet or None: The pet object if found, or None if not found.
        """
        try:
            return Pet.objects.get(slug=slug)
        except Pet.DoesNotExist:
            return None

    def get(self, request, slug):
        """
        Retrieve details of a specific pet.

        Parameters:
            request (HttpRequest): The HTTP request object.
            slug (str): The slug of the pet.

        Returns:
            Response: A response object containing the serialized data of the pet if found, or an HTTP status code indicating not found.
        """
        pet = self.get_object(slug)
        if pet is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = self.serializer_class(pet)
        return Response(serializer.data)

    def put(self, request, slug):
        """
        Update the details of a specific pet.

        Parameters:
            request (HttpRequest): The HTTP request object.
            slug (str): The slug of the pet.

        Returns:
            Response: A response object containing the serialized data of the updated pet if successful, or an HTTP status code indicating an error.
        """
        pet = self.get_object(slug)
        if pet is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = self.serializer_class(pet, data=request.data)
        if serializer.is_valid():
            pet = serializer.save()
            return Response(self.serializer_class(pet).data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, slug):
        """
        Delete a specific pet.

        Parameters:
            request (HttpRequest): The HTTP request object.
            slug (str): The slug of the pet.

        Returns:
            Response: A response object with no content and the HTTP status code indicating success or not found.
        """
        pet = self.get_object(slug)
        if pet is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        pet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
