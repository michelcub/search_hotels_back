from django.urls import path
from hotel.api.api import *


urlpatterns = [
    path('', get_hotels, name='get_hotels'),
    path("<int:hotel_id>/services/", get_services, name="get_services_by_hotel_id"),
    path('create/', create_hotel, name='create_hotel'),
    path("<int:id>/", get_hotel, name="get_hotel_by_id"),
    
]