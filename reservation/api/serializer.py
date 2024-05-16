from rest_framework import serializers

from reservation.models import Reservation

from habitacion.api.serializer import RoomSerializer
from hotel.api.serializer import HotelSerializer, ServicesSerializer
from user.api.serializer import UserSerializer

class ReservationSerializer(serializers.ModelSerializer):
    hotel = HotelSerializer()
    services = ServicesSerializer(many=True)
    customers = UserSerializer(many=True)
    class Meta:
        model = Reservation
        fields = '__all__'
        