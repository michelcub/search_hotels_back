
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework import status
from rest_framework.response import Response

from habitacion.models import Room, RoomType
from habitacion.api.serializer import RoomSerializer, RoomTypeSerializer
from reservation.models import Reservation
from hotel.models import Hotel


@api_view(['GET'])
@permission_classes([AllowAny])
def room_list(request):
    try:
        rooms = Room.objects.all()

        # Filtrar por tipo de habitación
        type_param = request.query_params.get('type')
        if type_param:
            rooms = rooms.filter(type__name=type_param)

        # Filtrar por disponibilidad de fechas
        init_date = request.query_params.get('init_date')
        end_date = request.query_params.get('end_date')
        if init_date and end_date:
            rooms = [room for room in rooms if room.is_available(init_date, end_date)]

        # Filtrar por nombre de hotel
        hotel_param = request.query_params.get('hotel')
        if hotel_param:
            rooms = rooms.filter(hotel__name=hotel_param)

        # Filtrar por número máximo de clientes
        customers_param = request.query_params.get('customers')
        if customers_param:
            rooms = rooms.filter(max_customers__lte=customers_param)

        # Serializar los resultados
        rooms_data = RoomSerializer(rooms, many=True).data

        if len(rooms_data) == 0:
            return Response({'error': 'No rooms available'}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({'rooms': rooms_data}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
@api_view(['GET'])
@permission_classes([AllowAny])
def room_type_available(request):
    try:
        hotel = request.query_params.get('hotel', None)
        init_date = request.query_params.get('init_date', None)
        end_date = request.query_params.get('end_date', None)
        max_customers = request.query_params.get('max_customers', None)
        
        if not hotel:
            return Response({'error': 'Hotel is required'}, status=status.HTTP_400_BAD_REQUEST)
        if not init_date:
            return Response({'error': 'init_date is required'}, status=status.HTTP_400_BAD_REQUEST)
        if not end_date:
            return Response({'error': 'end_date is required'}, status=status.HTTP_400_BAD_REQUEST)
        
       
        rooms = RoomType.objects.filter(hotel=hotel)
        
        if max_customers:
            rooms = rooms.filter(max_customers__gte=int(max_customers))
            print(rooms)
        room_list_available = []
        for room in rooms:
            if room.is_available(init_date, end_date):
                room_list_available.append(room)
                
                
        rooms = RoomTypeSerializer(room_list_available, many=True).data
        if len(rooms) == 0:
            return Response({'error': 'No rooms available'}, status=status.HTTP_200_OK)
        
        return Response({'available': rooms}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    

