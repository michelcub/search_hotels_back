from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Q

from hotel.api.serializer import HotelSerializer
from hotel.models import Hotel


@api_view(['GET'])
def get_hotels(request):
    query = Hotel.objects.all()
    hotels = HotelSerializer(query, many=True).data
    filter = request.query_params.get('filter')
    if filter is not None:
        hotels = hotels.filter(
            Q(name__icontains=request.query_params.get('filter')) |
            Q(description__icontains=request.query_params.get('filter')) |
            Q(address__icontains=request.query_params.get('filter')) |
            Q(city__icontains=request.query_params.get('filter')) |
            Q(state__icontains=request.query_params.get('filter')) |
            Q(country__icontains=request.query_params.get('filter'))
        )
        
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

