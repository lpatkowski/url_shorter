from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import (
    api_view,
    authentication_classes,
    permission_classes,
)
from rest_framework.response import Response

from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse

from .models import UrlMapping
from .permissions import IsAccountAdminOrReadOnly
from .serializers import CreateUrlMappingSerializer


@api_view(["POST"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAccountAdminOrReadOnly])
def create_short_url(request):
    serializer = CreateUrlMappingSerializer(
        data=request.data,
    )
    serializer.is_valid(raise_exception=True)
    data = serializer.validated_data

    try:
        url_mapping_obj = UrlMapping.objects.get(long_url=data["long_url"])
    except UrlMapping.DoesNotExist:
        url_mapping_obj = serializer.save()

    domain = get_current_site(request).domain
    # It is only a API so we are not doing HTTP 302 redirect from short_url to long_url.
    # This is why we can create short_url var as "revert_short_url" endpoint url representation.
    # We do not have to create serializer with short_url domain validation (to filter out
    # fake short urls with other domains), endpoint domain is always our.
    # We have to check only the hash regex and can revert the short_url to long_url if UrlMapping
    # object has been found.
    short_url = "{}{}".format(domain, reverse("revert-short-url", args=[url_mapping_obj.hash]))
    data = {
        "short_url": short_url
    }
    return Response(data, status=status.HTTP_201_CREATED)


@api_view(["GET"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAccountAdminOrReadOnly])
def revert_short_url(request, hash):
    try:
        url_mapping_obj = UrlMapping.objects.get(hash=hash)
    except UrlMapping.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    data = {
        "long_url": url_mapping_obj.long_url
    }
    return Response(data, status=status.HTTP_200_OK)
