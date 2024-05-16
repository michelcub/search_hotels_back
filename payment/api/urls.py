from django.urls import path
from payment.api.api import *


urlpatterns = [
    path('create/', create_payment, name='payment-list-create'),
]
