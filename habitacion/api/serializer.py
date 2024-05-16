from rest_framework import serializers

from habitacion.models import Room
from habitacion.models import RoomType
from hotel.api.serializer import HotelSerializer

class RoomTypeSerializer(serializers.ModelSerializer):
    hotel = HotelSerializer()
    class Meta:
        model = RoomType
        fields = '__all__'

class RoomSerializer(serializers.ModelSerializer):
    type = RoomTypeSerializer()
    class Meta:
        model = Room
        fields = '__all__'

