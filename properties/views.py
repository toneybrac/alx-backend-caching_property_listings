from django.shortcuts import render
from django.views.decorators.cache import cache_page
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Property
from .serializers import PropertySerializer
import logging

# Setup logger
logger = logging.getLogger(__name__)

@api_view(['GET'])
@cache_page(60 * 15)  # Cache for 15 minutes (60 seconds * 15)
def property_list(request):
    """
    View to list all properties with Redis caching for 15 minutes.
    """
    try:
        # Log cache hit/miss (this will help with debugging)
        logger.info(f"Property list view accessed. Cache key: {request.get_full_path()}")
        
        # Get all active properties
        properties = Property.objects.filter(is_active=True).order_by('-created_at')
        
        # Serialize the data
        serializer = PropertySerializer(properties, many=True)
        
        # Log the number of properties returned
        logger.info(f"Returning {len(properties)} properties from property_list view")
        
        # Return the response (will be cached by @cache_page)
        return Response({
            'success': True,
            'count': len(properties),
            'data': serializer.data,
            'message': 'Properties retrieved successfully',
            'cache_info': 'This response is cached for 15 minutes'
        }, status=status.HTTP_200_OK)
        
    except Exception as e:
        logger.error(f"Error in property_list view: {str(e)}")
        return Response({
            'success': False,
            'error': str(e),
            'message': 'Failed to retrieve properties'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# Alternative view without DRF (if you're not using Django REST Framework)
from django.http import JsonResponse
import json

@cache_page(60 * 15)  # Cache for 15 minutes
def property_list_json(request):
    """
    Alternative view using Django's JsonResponse (without DRF)
    """
    try:
        # Get all active properties
        properties = Property.objects.filter(is_active=True).order_by('-created_at')
        
        # Prepare data for JSON response
        properties_data = []
        for property in properties:
            properties_data.append({
                'id': str(property.id),
                'title': property.title,
                'description': property.description,
                'price': str(property.price),
                'location': property.location,
                'bedrooms': property.bedrooms,
                'bathrooms': str(property.bathrooms),
                'property_type': property.property_type,
                'square_feet': property.square_feet,
                'created_at': property.created_at.isoformat(),
                'is_active': property.is_active,
            })
        
        # Create response data
        response_data = {
            'success': True,
            'count': len(properties_data),
            'properties': properties_data,
            'cache_info': 'This response is cached for 15 minutes'
        }
        
        return JsonResponse(response_data, safe=False)
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e),
            'message': 'Failed to retrieve properties'
        }, status=500)


# Simple HTML view (if you want a template-based view)
@cache_page(60 * 15)
def property_list_html(request):
    """
    Template-based view for property listing
    """
    properties = Property.objects.filter(is_active=True).order_by('-created_at')
    return render(request, 'properties/list.html', {
        'properties': properties,
        'cache_duration': '15 minutes'
    })
