from rest_framework import serializers

from .models import Pet


# !PetSerializer
class PetSerializer(serializers.ModelSerializer):
    # created = serializers.DateTimeField(format="%Y-%m-%d")
    # modified = serializers.DateTimeField(format="%Y-%m-%d")
    # obj_count = serializers.SerializerMethodField()

    class Meta:
        model = Pet
        exclude = ["created", "modified", "pet_key"]
