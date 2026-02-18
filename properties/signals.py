# properties/signals.py
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.core.cache import cache
import logging

from .models import Property
from .utils import invalidate_property_cache

logger = logging.getLogger(__name__)

@receiver(post_save, sender=Property)
def property_saved_handler(sender, instance, created, **kwargs):
    """
    Invalidate cache when a Property is created or updated
    """
    action = "created" if created else "updated"
    logger.info(f"Property {instance.id} {action} - Invalidating cache")
    
    # Invalidate both list cache and this specific property cache
    invalidate_property_cache(instance.id)
    
    # Also invalidate location-based caches if location changed
    if not created and hasattr(instance, '_original_location'):
        if instance._original_location != instance.location:
            old_location_key = f'properties_location_{instance._original_location.lower().replace(" ", "_")}'
            cache.delete(old_location_key)
            logger.info(f"Location changed - Invalidated cache: {old_location_key}")

@receiver(post_delete, sender=Property)
def property_deleted_handler(sender, instance, **kwargs):
    """
    Invalidate cache when a Property is deleted
    """
    logger.info(f"Property {instance.id} deleted - Invalidating cache")
    invalidate_property_cache(instance.id)
