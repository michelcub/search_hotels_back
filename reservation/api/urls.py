from django.urls import path
from reservation.api.api import *

urlpatterns = [
    path('create/', create_reservation, name='create_reservation'),
    path("delete/<int:id>/", delete_reservation, name="delete_reservation"),
    path('', reservation_list, name='reservation_list'),
    path('<int:id>/', get_reservation_by_user, name='reservationget_reservation_by_user_list'),
]