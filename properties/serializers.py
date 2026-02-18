from rest_framework import serializers
from .models import Property

class PropertySerializer(serializers.ModelSerializer):
    """
    Serializer for Property model
    """
    formatted_price = serializers.SerializerMethodField()
    short_description = serializers.SerializerMethodField()
    
    class Meta:
        model = Property
        fields = [
            'id', 'title', 'description', 'price', 'formatted_price',
            'location', 'created_at', 'updated_at', 'is_active',
            'bedrooms', 'bathrooms', 'square_feet', 'property_type',
            'short_description'
        ]
        read_only_fields = ['created_at', 'updated_at']
    
    def get_formatted_price(self, obj):
        """Return formatted price with dollar sign and commas"""
        return f"${obj.price:,.2f}"
    
    def get_short_description(self, obj):
        """Return truncated description"""
        if len(obj.description) > 100:
            return obj.description[:100] + '...'
        return obj.description
