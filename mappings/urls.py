from django.urls import include, re_path

from .views import create_short_url, revert_short_url

HASH_FORMAT = r"[0-9a-zA-Z]{8}"

url_mappings_urls = [
    re_path(r"^create/$", view=create_short_url, name="create-short-url"),
    re_path(r"^(?P<hash>{})/$".format(HASH_FORMAT), view=revert_short_url, name="revert-short-url"),
]



