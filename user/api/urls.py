from django.urls import path
from user.api.api import *

urlpatterns = [
    path("<int:id>/", get_data_user, name="get_data_user")
]
