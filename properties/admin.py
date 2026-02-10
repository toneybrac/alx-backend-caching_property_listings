# properties/admin.py
from django.contrib import admin
from .models import Property

@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):
    list_display = ('title', 'formatted_price', 'location', 'property_type', 'created_at', 'is_active')
    list_filter = ('property_type', 'is_active', 'location', 'created_at')
    search_fields = ('title', 'description', 'location')
    readonly_fields = ('id', 'created_at', 'updated_at')
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'description', 'price', 'location')
        }),
        ('Property Details', {
            'fields': ('property_type', 'bedrooms', 'bathrooms', 'square_feet')
        }),
        ('Status', {
            'fields': ('is_active',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
