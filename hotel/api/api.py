from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from django.db.models import Q


from hotel.api.serializer import HotelSerializer, ServicesSerializer
from hotel.models import Hotel, Services


@api_view(['GET'])
@permission_classes([AllowAny])
def get_hotels(request):
    query = Hotel.objects.all()
    hotels = HotelSerializer(query, many=True).data
    print(hotels)
    if len(hotels) == 0:
        return Response({'message': 'No hotels found'}, status=status.HTTP_404_NOT_FOUND)
    
    return Response(hotels, status=status.HTTP_200_OK)


def create_hotel(request):
    data = request.data
    serializer = HotelSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def get_hotel(request, id):
    try:
        hotel = Hotel.objects.get(pk=id)
        return Response(HotelSerializer(hotel).data, status=status.HTTP_200_OK)
    except Hotel.DoesNotExist:
        return Response({'message': 'Hotel not found'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
@permission_classes([AllowAny])
def get_services(request, hotel_id):
    print(hotel_id, '>>>>>>>>')
    query = Services.objects.filter(hotel=hotel_id)
    services = ServicesSerializer(query, many=True).data
    
    if len(services) == 0:
        return Response({'message': 'No services found'}, status=status.HTTP_404_NOT_FOUND)
    
    return Response(services, status=status.HTTP_200_OK)