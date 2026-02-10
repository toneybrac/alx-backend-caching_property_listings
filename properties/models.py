# properties/models.py
from django.db import models
from django.utils import timezone
from decimal import Decimal
import uuid

class Property(models.Model):
    """
    Property model for real estate listings
    """
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        help_text="Unique identifier for the property"
    )
    title = models.CharField(
        max_length=200,
        help_text="Title of the property listing"
    )
    description = models.TextField(
        help_text="Detailed description of the property"
    )
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        help_text="Price of the property in USD"
    )
    location = models.CharField(
        max_length=100,
        help_text="Location of the property (e.g., 'New York, NY')"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text="Timestamp when the property was created"
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        help_text="Timestamp when the property was last updated"
    )
    is_active = models.BooleanField(
        default=True,
        help_text="Whether the property listing is active"
    )
    bedrooms = models.IntegerField(
        default=1,
        help_text="Number of bedrooms"
    )
    bathrooms = models.DecimalField(
        max_digits=3,
        decimal_places=1,
        default=1.0,
        help_text="Number of bathrooms"
    )
    square_feet = models.IntegerField(
        null=True,
        blank=True,
        help_text="Square footage of the property"
    )
    property_type = models.CharField(
        max_length=50,
        choices=[
            ('house', 'House'),
            ('apartment', 'Apartment'),
            ('condo', 'Condo'),
            ('townhouse', 'Townhouse'),
            ('land', 'Land'),
            ('commercial', 'Commercial'),
        ],
        default='house',
        help_text="Type of property"
    )
    
    class Meta:
        verbose_name = "Property"
        verbose_name_plural = "Properties"
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['price']),
            models.Index(fields=['location']),
            models.Index(fields=['created_at']),
            models.Index(fields=['property_type']),
        ]
    
    def __str__(self):
        return f"{self.title} - ${self.price} - {self.location}"
    
    def formatted_price(self):
        """Return formatted price with commas"""
        return f"${self.price:,.2f}"
    
    def is_expensive(self):
        """Check if property is expensive (over $500,000)"""
        return self.price > Decimal('500000.00')
    
    def short_description(self, length=100):
        """Return truncated description"""
        if len(self.description) > length:
            return self.description[:length] + '...'
        return self.description
