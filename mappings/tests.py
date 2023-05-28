from rest_framework import status
from rest_framework.exceptions import ErrorDetail
from rest_framework.test import APITestCase

from django.contrib.auth.models import User
from django.urls import reverse

from .models import UrlMapping


class UrlMappingTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='lukasz', email='lukasz@…', password='top_secret')
        self.client.force_authenticate(user=self.user)
        self.url_mapping_example = UrlMapping.objects.create(
            long_url="http://example.com/very-very/long/url/even-longer"
        )

    def test_create_short_url_user_unauthorized(self):
        self.client.logout()
        data = {
            "long_url": "https://www.wp.pl/testujemy-bardzo-mocno/1234/test/test/",
        }

        response = self.client.post(reverse("create-short-url"), data=data, headers={})

        self.assertEqual(response.data, {
            'detail': ErrorDetail(string='Authentication credentials were not provided.', code='not_authenticated')})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_short_url_invalid_data(self):
        data = {
            "invalid": "invalid",
        }

        response = self.client.post(reverse("create-short-url"), data=data)

        self.assertEqual(response.data, {'long_url': [ErrorDetail(string='This field is required.', code='required')]})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_new_short_url_invalid_data_url(self):
        data = {
            "long_url": "www.www.www",
        }

        response = self.client.post(reverse("create-short-url"), data=data)

        self.assertEqual(response.data, {'long_url': [ErrorDetail(string='Enter a valid URL.', code='invalid')]})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_the_same_short_url_twice_success(self):
        self.assertEqual(UrlMapping.objects.all().count(), 1)

        data = {
            "long_url": self.url_mapping_example.long_url,
        }

        response = self.client.post(reverse("create-short-url"), data=data)

        self.assertEqual(UrlMapping.objects.all().count(), 1)
        self.assertTrue("short_url" in response.data)
        self.assertTrue(response.data["short_url"] is not None)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_new_short_url_and_revert_it_success(self):
        data = {
            "long_url": "https://www.wp.pl/testujemy-bardzo-mocno/1234/test/test/",
        }

        response = self.client.post(reverse("create-short-url"), data=data)

        self.assertTrue("short_url" in response.data)
        self.assertTrue(response.data["short_url"] is not None)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # now try to revert
        url_mapping = UrlMapping.objects.get(long_url=data["long_url"])
        revert_response = self.client.get(reverse("revert-short-url", args=[url_mapping.hash]))
        self.assertEqual(revert_response.data["long_url"], data["long_url"])
        self.assertEqual(revert_response.status_code, status.HTTP_200_OK)

    def test_revert_short_url_hash_not_found(self):
        response = self.client.get(reverse("revert-short-url", args=["INVALIDD"]))
        self.assertEqual(response.data, None)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_revert_url_mapping_by_hash_success(self):
        response = self.client.get(reverse("revert-short-url", args=[self.url_mapping_example.hash]))
        self.assertEqual(response.data["long_url"], self.url_mapping_example.long_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
