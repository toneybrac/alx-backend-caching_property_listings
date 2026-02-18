from django.urls import path
from . import views

app_name = 'properties'

urlpatterns = [
    # Cached property list views
    path('', views.property_list, name='property_list'),  # DRF API view
    path('json/', views.property_list_json, name='property_list_json'),  # JSON view
    path('html/', views.property_list_html, name='property_list_html'),  # HTML view
    
    # You can also add other endpoints here
    path('<uuid:property_id>/', views.property_detail, name='property_detail'),
]
