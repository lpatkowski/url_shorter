from django.urls import path, include
from mappings.urls import url_mappings_urls
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('api-auth/', include('rest_framework.urls')),
    path('api-token-auth/', obtain_auth_token),
    path('', include(url_mappings_urls)),
]