from django.urls import path
from hotel.api.api import *


urlpatterns = [
    path('', get_hotels, name='get_hotels'),
    path('create/', create_hotel, name='create_hotel')
]