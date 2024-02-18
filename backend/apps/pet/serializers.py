from rest_framework import serializers

from .models import Pet


# !PetSerializer
class PetSerializer(serializers.ModelSerializer):
    # created = serializers.DateTimeField(format="%Y-%m-%d")
    # modified = serializers.DateTimeField(format="%Y-%m-%d")

    class Meta:
        model = Pet
        exclude = ["id", "created", "modified", "pet_key"]
