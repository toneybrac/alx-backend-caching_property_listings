
# properties/utils.py
from django.core.cache import cache
from django.db.models import QuerySet
from .models import Property
import logging
from typing import Union, Optional

logger = logging.getLogger(__name__)

def get_all_properties() -> QuerySet:
    """
    Retrieve all properties using low-level caching.
    Checks Redis cache first, falls back to database if not found.
    Cache key: 'all_properties'
    Cache timeout: 3600 seconds (1 hour)
    
    Returns:
        QuerySet of Property objects
    """
    cache_key = 'all_properties'
    
    # Try to get from cache
    properties = cache.get(cache_key)
    
    if properties is None:
        # Cache miss - fetch from database
        logger.info(f"CACHE MISS: {cache_key} - Fetching all properties from database")
        
        # Fetch from database
        properties = list(Property.objects.all())
        
        # Store in cache for 1 hour (3600 seconds)
        cache.set(cache_key, properties, 3600)
        
        logger.info(f"CACHE SET: {cache_key} - Stored {len(properties)} properties in cache for 3600 seconds")
        
        # Return queryset
        return Property.objects.all()
    else:
        # Cache hit
        logger.info(f"CACHE HIT: {cache_key} - Retrieved {len(properties)} properties from cache")
        
        # Return queryset with the cached IDs
        property_ids = [p.id for p in properties]
        return Property.objects.filter(id__in=property_ids)

def get_property_by_id(property_id: Union[str, int]) -> Optional[Property]:
    """
    Retrieve a single property by ID with caching.
    Cache key: 'property_{id}'
    Cache timeout: 3600 seconds (1 hour)
    
    Args:
        property_id: The UUID or ID of the property
        
    Returns:
        Property object or None if not found
    """
    cache_key = f'property_{property_id}'
    
    # Try to get from cache
    property_obj = cache.get(cache_key)
    
    if property_obj is None:
        # Cache miss
        logger.info(f"CACHE MISS: {cache_key} - Fetching property {property_id} from database")
        
        try:
            property_obj = Property.objects.get(id=property_id)
            # Store in cache for 1 hour
            cache.set(cache_key, property_obj, 3600)
            logger.info(f"CACHE SET: {cache_key} - Stored property in cache")
        except Property.DoesNotExist:
            logger.warning(f"Property {property_id} not found in database")
            return None
    else:
        logger.info(f"CACHE HIT: {cache_key} - Retrieved property from cache")
    
    return property_obj

def invalidate_property_cache(property_id: Optional[Union[str, int]] = None):
    """
    Invalidate property caches.
    If property_id is provided, invalidates both the specific property cache
    and the list cache. Otherwise, only invalidates the list cache.
    
    Args:
        property_id: Optional specific property ID to invalidate
    """
    # Always invalidate the list cache
    list_cache_key = 'all_properties'
    cache.delete(list_cache_key)
    logger.info(f"CACHE INVALIDATED: {list_cache_key}")
    
    # Invalidate specific property cache if ID provided
    if property_id:
        property_cache_key = f'property_{property_id}'
        cache.delete(property_cache_key)
        logger.info(f"CACHE INVALIDATED: {property_cache_key}")

def get_active_properties() -> QuerySet:
    """
    Get only active properties with caching
    """
    cache_key = 'active_properties'
    properties = cache.get(cache_key)
    
    if properties is None:
        logger.info(f"CACHE MISS: {cache_key} - Fetching active properties")
        properties = list(Property.objects.filter(is_active=True))
        cache.set(cache_key, properties, 1800)  # 30 minutes cache
        logger.info(f"CACHE SET: {cache_key} - Stored {len(properties)} active properties")
        return Property.objects.filter(id__in=[p.id for p in properties])
    else:
        logger.info(f"CACHE HIT: {cache_key} - Retrieved {len(properties)} active properties")
        return Property.objects.filter(id__in=[p.id for p in properties])

def get_properties_by_location(location: str) -> QuerySet:
    """
    Get properties filtered by location with caching
    """
    cache_key = f'properties_location_{location.lower().replace(" ", "_")}'
    properties = cache.get(cache_key)
    
    if properties is None:
        logger.info(f"CACHE MISS: {cache_key} - Fetching properties in {location}")
        properties = list(Property.objects.filter(location__icontains=location))
        cache.set(cache_key, properties, 1800)  # 30 minutes
        logger.info(f"CACHE SET: {cache_key} - Stored {len(properties)} properties")
        return Property.objects.filter(id__in=[p.id for p in properties])
    else:
        logger.info(f"CACHE HIT: {cache_key} - Retrieved {len(properties)} properties")
        return Property.objects.filter(id__in=[p.id for p in properties])
