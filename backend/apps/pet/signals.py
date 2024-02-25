import logging

from django.core.cache import cache
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver

from .models import Pet

logger = logging.getLogger("debug")


# ?object_post_delete_handler
@receiver(post_delete, sender=Pet, dispatch_uid="pet_deleted")
def object_post_delete_handler(sender, **kwargs):
    logger.info("Cache delete signal")
    cache.delete("pet_objects")


# ?object_post_save_handler
@receiver(post_save, sender=Pet, dispatch_uid="pet_updated")
def object_post_save_handler(sender, **kwargs):
    logger.info("Cache save signal")
    cache.delete("pet_objects")
