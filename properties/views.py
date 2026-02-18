# properties/views.py
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.cache import cache_page
from django.core.cache import cache
from rest_framework.decorators import api_view
from rest_framework.response import Response
import logging

from .models import Property
from .utils import get_all_properties, get_property_by_id  # Fixed import
from .serializers import PropertySerializer

logger = logging.getLogger(__name__)

@cache_page(60 * 15)
def property_list_html(request):
    """
    HTML view to display all properties with both view-level and low-level caching
    """
    # This uses the low-level caching from utils.py
    properties = get_all_properties()  # Fixed function name
    
    # Check cache status for logging
    cache_status = 'HIT' if cache.get('all_properties') else 'MISS'
    logger.info(f"Property list view - Cache {cache_status}")
    
    context = {
        'properties': properties,
        'cache_status': cache_status,
        'cache_duration': '15 minutes'
    }
    return render(request, 'properties/property_list.html', context)

@api_view(['GET'])
@cache_page(60 * 15)
def property_list(request):
    """
    DRF API view to return all properties as JSON
    """
    properties = get_all_properties()  # Fixed function name
    serializer = PropertySerializer(properties, many=True)
    
    cache_status = 'HIT' if cache.get('all_properties') else 'MISS'
    
    return Response({
        'status': 'success',
        'cache_status': cache_status,
        'count': len(serializer.data),
        'data': serializer.data
    })

def property_list_json(request):
    """
    JSON view without DRF, using low-level caching
    """
    properties = get_all_properties()  # Fixed function name
    
    # Convert to JSON serializable format
    properties_data = []
    for prop in properties:
        properties_data.append({
            'id': str(prop.id),
            'title': prop.title,
            'description': prop.description,
            'price': float(prop.price),
            'location': prop.location,
            'created_at': prop.created_at.isoformat(),
            'property_type': prop.property_type,
            'bedrooms': prop.bedrooms,
            'bathrooms': float(prop.bathrooms),
            'square_feet': prop.square_feet,
            'is_active': prop.is_active,
            'formatted_price': prop.formatted_price(),
            'is_expensive': prop.is_expensive()
        })
    
    cache_status = 'HIT' if cache.get('all_properties') else 'MISS'
    
    return JsonResponse({
        'status': 'success',
        'cache_status': cache_status,
        'count': len(properties_data),
        'data': properties_data
    })

@cache_page(60 * 10)
def property_detail(request, property_id):
    """
    View to display a single property with caching
    """
    property_obj = get_property_by_id(property_id)
    
    if not property_obj:
        return JsonResponse({
            'status': 'error',
            'message': 'Property not found'
        }, status=404)
    
    cache_status = 'HIT' if cache.get(f'property_{property_id}') else 'MISS'
    
    if request.path.endswith('/json/') or request.headers.get('Accept') == 'application/json':
        data = {
            'id': str(property_obj.id),
            'title': property_obj.title,
            'description': property_obj.description,
            'price': float(property_obj.price),
            'location': property_obj.location,
            'created_at': property_obj.created_at.isoformat(),
            'property_type': property_obj.property_type,
            'bedrooms': property_obj.bedrooms,
            'bathrooms': float(property_obj.bathrooms),
            'square_feet': property_obj.square_feet,
            'is_active': property_obj.is_active,
            'formatted_price': property_obj.formatted_price(),
            'is_expensive': property_obj.is_expensive()
        }
        return JsonResponse({
            'status': 'success',
            'cache_status': cache_status,
            'data': data
        })
    else:
        context = {
            'property': property_obj,
            'cache_status': cache_status
        }
        return render(request, 'properties/property_detail.html', context)
