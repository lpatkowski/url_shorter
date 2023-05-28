from django.conf import settings
from django.db import models
from django.utils.crypto import get_random_string


def generate_random_hash():
    """Creates a random hash string with predetermined length.
    We have a P(62,8) = 62! / (62-8)! = 136325893334400 combinations.
    It's not a perfect solution, but risk of collision is very low.
    Tested with 1 million UrlMapping objects.
    In the future we have to add created(DateTime) field to UrlMapping model
    and create periodic Celery task to remove old UrlMapping objects every day.
    This will reduce the possibility of a collision and speed up the DB.
    """
    hash_string = get_random_string(settings.URL_HASH_LENGTH)

    # it should not happen, but we should protect ourselves from that
    if UrlMapping.objects.filter(hash=hash_string).exists():
        return generate_random_hash()

    return hash_string


class UrlMapping(models.Model):
    long_url = models.URLField(
        max_length=255,
        unique=True,
        db_index=True,
        editable=False,
    )
    # we store only hash for short url, because domain can be changed
    hash = models.CharField(
        primary_key=True,
        max_length=settings.URL_HASH_LENGTH,
        default=generate_random_hash,
        unique=True,
        db_index=True,
        editable=False,
    )
