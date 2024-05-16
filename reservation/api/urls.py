from django.urls import path
from reservation.api.api import *

urlpatterns = [
    path('create/', create_reservation, name='room_list'),
]