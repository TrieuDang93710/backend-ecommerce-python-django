from . import models
from rest_framework import serializers


class PhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Photo
        fields = "__all__"
