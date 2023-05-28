from rest_framework import serializers

from .models import UrlMapping


class CreateUrlMappingSerializer(serializers.ModelSerializer):
    long_url = serializers.URLField(min_length=10, max_length=255)

    class Meta:
        model = UrlMapping
        exclude = ["hash", ]
