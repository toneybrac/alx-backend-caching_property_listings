# properties/signals.py
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.core.cache import cache
import logging

from .models import Property

logger = logging.getLogger(__name__)

@receiver(post_save, sender=Property)
def property_saved_handler(sender, instance, created, **kwargs):
    """
    Invalidate cache when a Property is created or updated
    """
    cache_key = 'all_properties'
    cache.delete(cache_key)
    action = "created" if created else "updated"
    logger.info(f"Property {instance.id} {action} - Cache invalidated: {cache_key}")

@receiver(post_delete, sender=Property)
def property_deleted_handler(sender, instance, **kwargs):
    """
    Invalidate cache when a Property is deleted
    """
    cache_key = 'all_properties'
    cache.delete(cache_key)
    logger.info(f"Property {instance.id} deleted - Cache invalidated: {cache_key}")
