from django.urls import path
from habitacion.api.api import *

urlpatterns = [
    path('', room_list, name='room_list'),
    path('availables/', room_type_available, name='room_type_available')
]
